from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from web.account_views import *
from web.expert_views import *
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^register$',register),
    url(r'^experts$',list_experts),
    url(r'^$',login),
    url(r'^logout$',logout),
    # Examples:
    # url(r'^$', 'expertRecommendation.views.home', name='home'),
    # url(r'^expertRecommendation/', include('expertRecommendation.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
