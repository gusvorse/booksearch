from django.conf.urls import patterns, url
from django.views.generic.base import RedirectView
from books import views

urlpatterns = patterns('',
    # ex: books/search/
    #url(r'^$', views.search_form, name='searchform'),
    url(r'^$', RedirectView.as_view(url='/searchform/'), name='start'),
    url(r'^searchform/$', views.Index.as_view(), name='searchform'),
    #url(r'^searchform/result/$', views.search, name='search'),
    url(r'^searchform/detail/(?P<pk>\d+)$', views.detail, name='detail'),
    url(r'^login/$', views.Login_user.as_view(), name='login'),
    url(r'^logout/$', views.logout_user, name='logout'),
    url(r'^createuser/$', views.Create_user.as_view(), name='createuser'),
    url(r'^user/(?P<username>\w+)$', views.profile, name='profile'),
    url(r'^(?P<pk>\d+)/follow$', views.follow_book, name='follow'),
    url(r'^(?P<pk>\d+)/unfollow$', views.unfollow_book, name='unfollow'),
    url(r'^timeline/$', views.timeline, name='timeline'),
    #url(r'^detail/(?P<book_id>\d+)$', views.MyDetailView.as_view(), name='detail'),
)
