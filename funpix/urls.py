"""funpix URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from pix.views import UsersView, UserView, ImagesView, ImageView, register_test, index, is_user_authenticated, \
    get_raw_image

urlpatterns = [
    url(r'^$', index),
    url(r'^admin/', admin.site.urls),

    # tests
    url(r'^register_test/?$', register_test),
    
    # REST API
    url(r'^auth/?$', is_user_authenticated),
    url(r'^users/?$', UsersView.as_view()),
    url(r'^users/(?P<username>\w[\w\d]{3,})/?$', UserView.as_view()),
    url(r'^images/?$', ImagesView.as_view()),
    url(r'^images/(?P<id>\d+)/?$', ImageView.as_view()),
    url(r'^raw/images/(?P<pk>\d+)/?$', get_raw_image),
]
