from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.chat_index, name='chat_index'),
    # url used to process the xmlhttprequests done by nodejs socket.io
    url(r'^save_message/$', views.save_message, name='chat_save_message'),
]