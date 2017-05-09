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

from pix.views import ImagesView, ImageView, UsersView, UserView, LoginView

urlpatterns = [
    url(r'^users/?$', UsersView.as_view()),
    url(r'^users/(?P<username>\w[\w\d]{3,})/?$', UserView.as_view()),

    url(r'^images/?$', ImagesView.as_view()),
    url(r'^images/(?P<pk>\d+)/?$', ImageView.as_view()),

    url(r'^auth/?$', LoginView.as_view()),
]
