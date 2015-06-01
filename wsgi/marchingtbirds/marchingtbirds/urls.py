from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.views.generic.base import RedirectView
from marchingtbirds.sitemaps import HomeSitemap, StaticViewsSitemap, PostSitemap, StaffSitemap

sitemaps = {
    'home': HomeSitemap,
    'pages': StaticViewsSitemap,
    'posts': PostSitemap,
    'staff': StaffSitemap
}

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'marchingtbirds.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', 'marchingtbirds.views.home', name='home'),
    url(r'^index.html', RedirectView.as_view(url='/')),
    url(r'^about/$', RedirectView.as_view(url='/')),
    url(r'^program/$', RedirectView.as_view(url='/')),
    url(r'^season/$', RedirectView.as_view(url='/')),

    url(r'^posts/$', 'marchingtbirds.views.morenews', name='posts'),
    url(r'^posts/(?P<url>\S+)/$', 'marchingtbirds.views.detail', name='detail'),

    url(r'^about/tradition-and-philosophy/$', 'marchingtbirds.views.tradition', name='tradition'),
    url(r'^about/staff/$', 'marchingtbirds.views.staff', name='staff'),
    url(r'^about/history/$', 'marchingtbirds.views.hist', name='hist'),

    url(r'^program/marching-band-faqs/$', 'marchingtbirds.views.faq', name='faq'),
    url(r'^program/about-band-camp/$', 'marchingtbirds.views.bandcamp', name='bandcamp'),

    url(r'^season/current-field-show/$', 'marchingtbirds.views.fieldshow', name='fieldshow'),
    url(r'^season/full-season-calendar/$', 'marchingtbirds.views.calendar', name='calendar'),
    url(r'^season/memorial-day/$', 'marchingtbirds.views.memorialday', name='memorialday'),

    url(r'^nest/', include('nest.urls')),
    url(r'^privacy/$', 'nest.views.privacy', name='privacy'),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    url(r'^tinymce/', include('tinymce.urls')),
)
