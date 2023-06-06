from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('chatbot', views.chatbot, name='chatbot'),
    #path('chatbot', test_code.chatbot),
    #path('chatbot', views.voice_output, name='voice_output')
]
