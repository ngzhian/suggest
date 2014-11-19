import logging
import json
import re

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import render
import requests

# from .entities import ENTITIES
# from .keywords import KEYWORDS
from alchemyapi_python.alchemyapi import AlchemyAPI
from .models import Article

log = logging.getLogger(__name__)


def home(request):
    return render(request, 'index.html')


@csrf_exempt
def entity(request):
    data = json.loads(request.body)
    log.debug('got data ' + str(data))
    if not data:
        return JsonResponse(dict(err='no content'))
    if 'content' not in data:
        return JsonResponse(dict(err='no content'))
    entities = _entity(data['content'])
    log.debug('result is: ' + str(entities))
    return JsonResponse(dict(result=entities))


def _entity(content):
    alchemyapi = AlchemyAPI()
    response = alchemyapi.entities('text', content)
    list_of_entities = response['entities']
    return list_of_entities


@csrf_exempt
def suggest(request):
    data = json.loads(request.body)
    log.debug('got data ' + str(data))
    if not data:
        return JsonResponse(dict(err='no content'))
    if 'content' not in data:
        return JsonResponse(dict(err='no content'))
    result, keywords = _suggest(data['content'])
    log.debug('result is: ' + str(result))
    return JsonResponse(dict(result=result, keywords=keywords))


def _suggest(content):
    alchemyapi = AlchemyAPI()
    response = alchemyapi.keywords('text', content)
    list_of_keywords = response['keywords']
    # send entities query to NYT
    top_keyword_data = list_of_keywords[0]
    log.debug('keywords we have: ' + str(list_of_keywords))
    keyword = top_keyword_data['text']
    # call nyt api
    related_articles, keywords_map = article_search(keyword)
    return (related_articles[:10], keywords_map)


def article_search(search_term):
    '''
    Use NYT Article Search API to find articles matching a search term
    '''
    api_key = open('nyt_api_key').read().strip()
    base_url = 'http://api.nytimes.com/svc/search/v2/articlesearch.json?q={q}&api-key=' + api_key
    log.debug('searching nyt for: ' + search_term)
    r = requests.get(base_url.format(q=search_term))
    response = r.json()
    documents = response['response']['docs']
    # filter out, these aren't news
    documents = [d for d in documents if d['type_of_material'] != 'timestopic']
    # RESULTS == documents
    # we don't want too many keywords, just top 3 priority
    for doc in documents:
        doc.update({'keywords_list': _filter_nyt_keywords(doc['keywords'])[:3]})
        doc.update({'url': clean_url(doc['web_url'])})
    # get a list of all keywords
    keywords = [kw for kw in _filter_nyt_keywords(doc['keywords']) for doc in documents]
    keyword_article_map = aggregate_keywords(keywords, documents)
    time_kw_map = local_time_db_search(keywords)
    for kw, l in keyword_article_map:
        if kw in time_kw_map:
            keyword_article_map[kw].extend(time_kw_map[kw])
    return (documents, keyword_article_map)


def _filter_nyt_keywords(keywords):
    # major_kw = filter(lambda kw: kw.get('is_major', 'Y') != 'N', keywords)
    sorted_kw = sorted(keywords, lambda x, y: cmp(x.get('rank', 1), y.get('rank', 1)))
    return [kw['value'] for kw in sorted_kw]


def clean_url(nyt_url):
    p = re.compile(r'\\/')
    return p.sub('/', nyt_url)


def aggregate_keywords(keywords, articles):
    agg = {}
    for article in articles:
        for keyword in article['keywords']:
            if keyword['value'] not in agg:
                agg[keyword['value']] = []
            agg[keyword['value']].append(article)
    return [{'keyword': k, 'articles': v} for k, v in agg.iteritems()]


def local_time_db_search(keywords):
    agg = {}
    for keyword in set(keywords):
        most_relevant_first = sorted(
            Article.objects.filter(keywords__value__icontains=keyword),
            lambda a, b: cmp(a.association_factor(keyword),
                             b.association_factor(keyword)))
        if keyword not in agg:
            agg[keyword] = []
        agg[keyword].extend(most_relevant_first[:5])
    return agg


def example(request):
    return JsonResponse(dict(result=get_latest_from_time()))


def get_latest_from_time():
    response = requests.get('http://time.com/api/latest/')
    data = response.json()
    latest_article = data['articles'][0]
    html_content = latest_article['content']
    content = re.sub(r'<[^>]*>', '', html_content)
    log.debug('content is: ' + content)
    return content.strip()
