import os.path, datetime
from django.contrib.sitemaps import Sitemap
from django.core.urlresolvers import reverse
from marchingtbirds.settings import BASE_DIR
from marchingtbirds.models import NewsPost, StaffMember


def getlastmod(f):
    return datetime.datetime.fromtimestamp(os.path.getmtime(f))


class HomeSitemap(Sitemap):
    priority = 1.0
    changefreq = 'monthly'

    def items(self):
        return ['home']

    def lastmod(self, obj):
        if NewsPost.objects:
            return (NewsPost.objects.order_by('-pub_date')[0]).pub_date
        else:
            return getlastmod(BASE_DIR + '/templates/marchingtbirds/home.html')

    def location(self, obj):
        return '/'


class StaticViewsSitemap(Sitemap):
    names = {
        'tradition': 'marchingtbirds/tradition.html',
        'hist': 'marchingtbirds/staffhist.html',
        'faq': 'marchingtbirds/faq.html',
        'bandcamp': 'marchingtbirds/bandcamp.html',
        'fieldshow': 'marchingtbirds/fieldshow.html',
        'calendar': 'marchingtbirds/calendar.html',
        'memorialday': 'marchingtbirds/memorialday.html',
    }
    template_dir = BASE_DIR + '/templates/'

    priority = 0.5
    changefreq = 'yearly'

    def items(self):
        return self.names.keys()

    def lastmod(self, obj):
        path = self.template_dir + self.names[obj]
        return getlastmod(path)

    def location(self, obj):
        return reverse(obj)


class PostSitemap(Sitemap):
    priority = 0.2
    changefreq = 'never'

    def items(self):
        return NewsPost.objects.all()

    def lastmod(self, obj):
        return obj.pub_date

    def location(self, obj):
        return '/posts/' + obj.getUrl() + '/'


class StaffSitemap(Sitemap):
    priority = 0.7
    changefreq = 'yearly'

    def items(self):
        return ['staff']

    def lastmod(self, obj):
        if StaffMember.objects:
            return (StaffMember.objects.order_by('-last_update')[0]).last_update
        else:
            return getlastmod(BASE_DIR + '/templates/marchingtbirds/staffhist.html')

    def location(self, obj):
        return '/about/staff/'