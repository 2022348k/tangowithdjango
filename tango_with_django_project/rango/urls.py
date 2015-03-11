from django.conf.urls import patterns, url
from rango import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^about', views.about, name='about'),
                       url(r'^add_category/$', views.add_category, name='add_category'),
                       url(r'^category/(?P<category_name_slug>[\w\-]+)/add_page/$', views.add_page, name='add_page'),
                       url(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.category, name='category'),
                       url(r'^register/$', views.register, name='register'),
                       url(r'^login/$', views.user_login, name='login'),
                       url(r'^restricted/', views.restricted, name='restricted'),
                       url(r'^logout/$', views.user_logout, name='logout'),
                       url(r'^search/$', views.search, name='search'),
                       url(r'^goto/$', views.track_url, name='goto'),
                       url(r'^404/$', views.error_page, name='404'),
                       url(r'^accounts/password_change/$', 'django.contrib.auth.views.password_change', {'post_change_redirect' : '/rango/accounts/password_change/done/'},  name="password_change"), 
                       url(r'^accounts/password_change/done/$', 'django.contrib.auth.views.password_change_done'),
                       url(r'^profile/(?P<username>\w{0,50})/$', views.profile, name='profile'),
                       url(r'^add_profile/$', views.register_profile, name='add_profile'),
                       url(r'^profile_update/', views.profile_update, name='profile_update'),
                       url(r'^profile_all/', views.profile_all, name='profile_all'),
                    )