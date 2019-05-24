from django.urls import path
from bins import views

urlpatterns = [
    path('bins/', views.BinList.as_view(), name='bin-list'),
    path('bins/<int:pk>/', views.BinDetail.as_view(), name='bin-detail'),
    path('bins/<int:pk>/token/', views.BinTokenDetail.as_view(), name='bin-token-detail'),
    path('bins/<int:pk>/token/refresh/', views.BinTokenRefresh.as_view(), name='bin-token-refresh'),
]
