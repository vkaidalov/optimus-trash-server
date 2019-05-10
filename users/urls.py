from django.urls import path
import users.views as views

urlpatterns = [
    path('users/', views.UserList.as_view(), name='user-list'),
    path('users/<int:pk>/', views.UserDetail.as_view(), name='user-detail'),
    path('users/<int:pk>/confirmation/',
         views.UserConfirmation.as_view(), name='user-confirmation'),
]
