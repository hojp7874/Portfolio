from django.urls import path
from . import views

app_name = 'farm_products'
urlpatterns = [
    path('', views.show_graph, name='graph'),
    path('test/', views.test, name='test'),
]