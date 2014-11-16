Suggest
=======
A hack for TimeIncHack2014

Suggest is a web-based tool that helps writers and editors of news/magazine
discover related articles that the organization has written previously.
For example and Time Inc editor will be able to easily discover related
articles that have been published, and can easily link to the articles.
This promotes internal cross-linking and gives the readers more context.

![A screenshot of Suggest](http://i.imgur.com/FGlk8Vo.png?1 "Get relevant articles while you're writing")

Requirements
------------
[AlchemyAPI](http://www.alchemyapi.com/)
[Django](https://pypi.python.org/pypi/Django/)
[requests](https://pypi.python.org/pypi/requests)

How it works
------------
The front-end is AngularJS, with some jQuery hack in the controllers.
The rendering of related articles are conveninently handled by Angular, and event handlers are attached to the buttons and text area.
Controller methods call REST endpoints that the Django hosts.
The role of the server is an adapter between external API (AlchemyAPI) that it relies on to do analysis of the text.
Suggest does 2 forms of text analysis:
    1. Keyword extraction
    2. Entity analysis
Entity analysis is done every 3 seconds that no keypress is registered in the textarea (because AlchemyAPI is generous about the limit for this hackathon). Keyword extraction is fired by the 'Suggest' button.
Between the click and the final rendering on the webpage, these steps follow:
    1. Call AlchemyAPI to get a list of keyword
    2. Use the most relevant keyword to look for articles on Time Inc and NYT that is relevant
    2a. Time Inc articles were crawled and lived locally in sqlite
    2b. NYT has a great API endpoint that is super flexible, I just the most simple style '?q='
    3. We do some simple filtering of irrelevant data, such as topics (we want news articles)
    4. Look at and extract certain keywords found in those articles from NYT
    5. For local Time articles we run a slightly more fine-tuned search
    6. All these data returned to the Angular Controllers, bound to scope and rendered by angular templates
