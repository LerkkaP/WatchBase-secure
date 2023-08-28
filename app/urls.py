from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login_user", views.login_user, name="login"),
    path('logout_user', views.logout_user, name='logout'),
    path('watches', views.watches, name="watches"),
    path('details/<int:id>', views.details, name='details'),
    path('watch/<int:id>/handle_description/', views.handle_description, name='handle_description'),
    path('add_watch/', views.add_watch, name='add_watch'),
    path('details/<int:id>/delete_watch/', views.delete_watch, name='delete_watch')

]