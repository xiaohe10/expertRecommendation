from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from web.account_views import *
from web.expert_views import *
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$',login),
    url(r'^register$',register),
    url(r'^logout$',logout),

    url(r'^experts/list/(\d+)/$',list_experts),
    url(r'^experts/search$',search_expert),
    url(r'^experts/detail/(\d+)/$',detail),
    url(r'^match/getmatch/(\d+)/$',getmatch),
    url(r'^static/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATIC_ROOT},name='static'),
    # Examples:
    # url(r'^$', 'expertRecommendation.views.home', name='home'),
    # url(r'^expertRecommendation/', include('expertRecommendation.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
