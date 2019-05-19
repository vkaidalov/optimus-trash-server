from django.urls import path
from bins import views

urlpatterns = [
    path('bins/', views.BinList.as_view(), name='bin-list'),
    path('bins/<int:pk>/', views.BinDetail.as_view(), name='bin-detail'),
]
