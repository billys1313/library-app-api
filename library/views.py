from rest_framework import (
    viewsets,
    views,
    status,
)
from rest_framework.response import (
    Response,
    
)
import datetime

from django.db.models import (
    F,
    Count,
    Q,
)

from .models import (
    Author,
    Book, 
    Category,
)
from .serializers import ( 
    AuthorSerializer, 
    BookSerializer, 
    CategorySerializer,
)
from drf_spectacular.utils import (
    extend_schema_view, 
    extend_schema,
)

@extend_schema_view(
    list=extend_schema(
        summary="Retrieve a list of authors",
        description="Retrieve a list of all authors.",
    ),
    retrieve=extend_schema(
        summary="Retrieve an author by ID",
        description="Retrieve a specific author by its ID.",
    ),
    create=extend_schema(
        summary="Create a new author",
        description="Create a new author.",
    ),
    update=extend_schema(
        summary="Update an author",
        description="Update an existing author by its ID.",
    ),
    partial_update=extend_schema(
        summary="Partially update an author",
        description="Partially update an existing author by its ID.",
    ),
    destroy=extend_schema(
        summary="Delete an author",
        description="Delete an existing author by its ID.",
    ),
)
class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all().order_by('id')
    serializer_class = AuthorSerializer

@extend_schema_view(
    list=extend_schema(
        summary="Retrieve a list of books",
        description="Retrieve a list of all books.",
    ),
    retrieve=extend_schema(
        summary="Retrieve a book by ID",
        description="Retrieve a specific book by its ID.",
    ),
    create=extend_schema(
        summary="Create a new book",
        description="Create a new book.",
    ),
    update=extend_schema(
        summary="Update a book",
        description="Update an existing book by its ID.",
    ),
    partial_update=extend_schema(
        summary="Partially update a book",
        description="Partially update an existing book by its ID.",
    ),
    destroy=extend_schema(
        summary="Delete a book",
        description="Delete an existing book by its ID.",
    ),
)
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all().order_by('id')
    serializer_class = BookSerializer

@extend_schema_view(
    list=extend_schema(
        summary="Retrieve a list of categories",
        description="Retrieve a list of all categories.",
    ),
    retrieve=extend_schema(
        summary="Retrieve a category by ID",
        description="Retrieve a specific category by its ID.",
    ),
    create=extend_schema(
        summary="Create a new category",
        description="Create a new category.",
    ),
    update=extend_schema(
        summary="Update a category",
        description="Update an existing category by its ID.",
    ),
    partial_update=extend_schema(
        summary="Partially update a category",
        description="Partially update an existing category by its ID.",
    ),
    destroy=extend_schema(
        summary="Delete a category",
        description="Delete an existing category by its ID.",
    ),
)
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        # Get related books for each category and include them in the response
        for category in serializer.data:
            category_obj = Category.objects.get(id=category['id'])
            book_titles = category_obj.book_set.values_list('title', flat=True)
            category['book_titles'] = list(book_titles)

        return Response(serializer.data)
    
class QueryView(views.APIView):
    @extend_schema(
        summary="Retrieve a list of test query",
        description="Retrieve a list of test query.",
    )
    def get(self, request, *args, **kwargs):
        
        start_date = datetime.date(2022, 1, 1)
        end_date = datetime.date(2024, 5, 30)

        queryset = Book.objects.filter(id__gt=31, id__lt=70)
       
        queryset = queryset.filter(published_date__gt=start_date, published_date__lt=end_date)

        serializer = BookSerializer(queryset, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)

    