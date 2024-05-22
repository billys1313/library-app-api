from django.urls import (
    path, 
    include,
)
from library import views

from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('authors', views.AuthorViewSet)
router.register('books', views.BookViewSet)
router.register('categories', views.CategoryViewSet)

app_name = 'library'

urlpatterns = [
    path('', include(router.urls)),
    path('query', views.QueryView.as_view(), name= "Query")
]
