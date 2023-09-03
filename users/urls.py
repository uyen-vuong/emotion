from django.conf.urls import url
from django.urls import include
from users import views
from django.urls import path
app_name = 'account'

urlpatterns = [
    url(r'^login/$', views.login_view, name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^register/$', views.register, name='register'),
    url(r'^', include('django.contrib.auth.urls')),
    url(r'^profile/$', views.profile, name = 'profile'),
]
