from django.db import models


class Article(models.Model):
    title = models.CharField(max_length=200)
    short = models.CharField(max_length=1000, blank=True)
    full = models.CharField(max_length=10000)
    url = models.URLField()
    thumbnail = models.URLField()
    pub_date = models.DateTimeField()
    section = models.CharField(max_length=200, blank=True)

    def association_factor(self, keyword):
        '''0 -> no association, 1 -> direct'''
        words = self.keywords.all()
        if any(w.matches(keyword) for w in words):
            return 1
        else:
            factor = 0
            if keyword in self.title:
                factor += 0.5
            if keyword in self.short:
                factor += 0.3
            if keyword in self.full:
                factor += 0.2
            return factor

    def __str__(self):
        return self.title


class Keyword(models.Model):
    value = models.CharField(max_length=50)
    keyword = models.ManyToManyField(Article, related_name='keywords')

    def matches(self, another_word):
        me = self.value.lower().strip()
        other = another_word.lower().strip()
        return me in other or other in me

    def __str__(self):
        return self.value
