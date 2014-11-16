from django.contrib import admin
from suggest.models import Article, Keyword


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'thumbnail', 'pub_date')
    pass


class KeywordAdmin(admin.ModelAdmin):
    list_display = ('value', )
    pass

admin.site.register(Article, ArticleAdmin)
admin.site.register(Keyword, KeywordAdmin)
