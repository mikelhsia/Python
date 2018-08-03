"""
urls.py for this application
"""

from django.urls import path
from . import views

app_name = 'timehutBlog'
urlpatterns = [
	path('collection/', views.collection_list),
	# path('collection/', views.CollectionView.as_view(), name='post_list'),
	path('collection/<int:collection_id>/', views.collection_detail, name='collection_detail'),
	path('collection/<int:collection_id>/share/', views.collection_share, name='collection_share')
]
