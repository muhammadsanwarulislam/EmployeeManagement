from django.urls import path
from .import views
urlpatterns = [
    path('', views.poll_list,name='polls_list'),
    path('<int:id>/details/', views.poll_details,name='poll_details'),
    path('<int:id>/',views.single_poll,name='single_poll'),
]
