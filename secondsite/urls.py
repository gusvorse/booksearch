from django.conf.urls import patterns, include, url

from books import views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url('^activity/', include('actstream.urls')),
    url(r'^', include('books.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
