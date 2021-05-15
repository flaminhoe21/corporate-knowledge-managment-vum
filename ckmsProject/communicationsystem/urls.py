from django.urls import path
from . import views

app_name = 'communicationsystem'
urlpatterns = [
    path('socket/<int:post_id>/', views.posts_communication_system, name='posts_communication_system_chat'),
]