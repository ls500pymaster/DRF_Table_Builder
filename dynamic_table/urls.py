from django.urls import path
from dynamic_table import views

urlpatterns = [
    path('api/table/', views.DynamicTableViewSet.as_view({'post': 'create'}), name='dynamic_table_create'),
]