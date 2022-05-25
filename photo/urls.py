from django.urls import path, re_path
from . import views


app_name = "photo"


urlpatterns = [

    re_path(r'^$', views.home, name='home'),
    path('download/', views.download, name='download'),
    path('download_app', views.export, name='download_app'),
    path('group/create/', views.GroupCreate.as_view(), name='create_group'),
    path('groups', views.GroupsView.as_view(), name='groups'),
    path('groups/<int:pk>', views.GroupsDetail.as_view(), name='groups_detail'),
    path('groups/update/<int:pk>', views.GroupsUpdate.as_view(), name='group_update'),
    path('groups/<int:pk>/delete', views.GroupsDelete.as_view(), name='group_delete'),
    path('api/', views.api_overview),
    path('api/login', views.LoginView.as_view()),
    path('api/groups', views.groups_list),
    path('api/places', views.places_list),
    path('api/images', views.images_list),
    path('api/photos', views.photos_list),
    path('api/groups/<int:pk>/', views.group_detail),
    path('api/places/<int:pk>/', views.place_detail),
    path('api/images/<int:pk>/', views.image_detail),
    path('api/photos/<int:pk>/', views.photo_detail),


]