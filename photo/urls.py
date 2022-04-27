from django.urls import path, re_path
from . import views


app_name = "photo"


urlpatterns = [

    re_path(r'^$', views.home, name='home'),
    path('download/', views.download, name='download'),
    path('download_app', views.export, name='download_app'),
    path('group/create/', views.GroupCreate.as_view(), name='create_group'),
    path('groups', views.GroupsView.as_view(), name='groups')


]