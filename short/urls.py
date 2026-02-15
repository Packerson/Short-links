from django.urls import path

from short import views

urlpatterns = [
    path('to_shorten/', views.ToShortenView.as_view(), name='to_shorten'),
    path('to_read/<str:code>/', views.ToReadView.as_view(), name='to_read'),
]