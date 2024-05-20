from rest_framework import serializers
from .models import Author, Book, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']
        read_only_fields = ['id']

    def create(self, validated_data):
        
        category_name = validated_data.get('name')
        
        existing_category = Category.objects.filter(name=category_name).first()
        if existing_category:
            # Update the existing category with the new data
            existing_category.name = category_name
            existing_category.save()
            return existing_category
        
        return Category.objects.create(**validated_data)
    """
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Customize representation to include related books' IDs and titles
        representation['books'] = [{'id': book.id, 'title': book.title} for book in instance.book_set.all()]
        return representation
    """
    

class BookSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True)
    author = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all(), required=False)

    class Meta:
        model = Book
        fields = ['id', 'title', 'isbn', 'published_date', 'author', 'categories']
        read_only_fields = ['id']

    def create(self, validated_data):
        categories_data = validated_data.pop('categories')
        author_id = validated_data.pop('author', None)  # Remove author from validated_data if present
        book = Book.objects.create(author=author_id, **validated_data)
        
        # Associate the book with the author
        if author_id:
            book.author = author_id
            book.save()

        # Create categories and associate them with the book
        for category_data in categories_data:
            category_name = category_data.get('name')
            existing_category = Category.objects.filter(name=category_name).first()
            if existing_category:
                book.categories.add(existing_category)
            else:
                category = Category.objects.create(**category_data)
                book.categories.add(category)
        
        return book

    """
    def validate_isbn(self, value):
        # Check if the ISBN is unique
        if Book.objects.filter(isbn=value).exists():
            raise serializers.ValidationError("ISBN must be unique")
        return value
    """
    #Comment test
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        #instance.published_date = validated_data.get('published_date', instance.published_date)
        instance.author = validated_data.get('author', instance.author)  # Update author ID
        instance.save()

        # Update categories
        if 'categories' in validated_data:
            new_categories_data = validated_data.pop('categories')
            #existing_categories = set(instance.categories.all())
            updated_categories = set()
            
            for category_data in new_categories_data:
                category_name = category_data.get('name')
                existing_category = Category.objects.filter(name=category_name).first()

                if existing_category:
                    instance.categories.add(existing_category)
                    updated_categories.add(existing_category)
                else:
                    new_category = Category.objects.create(**category_data)
                    instance.categories.add(new_category)
                    updated_categories.add(new_category)

            # Remove categories not present in the updated data
            """
            removed_categories = existing_categories - updated_categories
            for category in removed_categories:
                instance.categories.remove(category)
            """
        return instance
    """
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        # Customize representation to include related books' IDs, titles, and categories
        representation['categories'] = [{'category_id': category.id, 'category_name': category.name} for category in instance.categories.all()]
        
        return representation
    """


class AuthorSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, required=False)

    class Meta:
        model = Author
        fields = ['id', 'name', 'books']
        read_only_fields = ['id']

    def create(self, validated_data):
        books_data = validated_data.pop('books', [])
        
        if not books_data:
            # If books data is empty, create the author without associated books
            author_instance = Author.objects.create(**validated_data)
        else:
            author_instance = Author.objects.create(**validated_data)

            for book_data in books_data:
                categories_data = book_data.pop('categories')
                book_data_without_author = {k: v for k, v in book_data.items() if k != 'author'}
                book = Book.objects.create(author=author_instance, **book_data_without_author)
                for category_data in categories_data:
                    category, _ = Category.objects.get_or_create(**category_data)
                    book.categories.add(category)

        return author_instance
    """
    def get_books(self, instance):
        books = instance.book_set.all()
        return [{'id': book.id, 'title': book.title} for book in books]
    """
    """
        if existing_author:
            raise serializers.ValidationError("Author with this name already exists.")
        
        return Author.objects.create(**validated_data)
        """
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Customize representation to include related books' IDs and titles
        representation['books'] = []
        for book in instance.book_set.all():
            book_info = {
                'title': book.title,
                'isbn': book.isbn,
                'published_date': book.published_date,
                'categories': [{'name': category.name} for category in book.categories.all()]
            }
            representation['books'].append(book_info)
        return representation
    
        

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        
        if 'books' in validated_data and validated_data['books']:
            books_data = validated_data.pop('books')
            existing_books = instance.book_set.all()  # Use book_set to access related books
            for book_data in books_data:
                categories_data = book_data.pop('categories')
                book, created = Book.objects.get_or_create(author=instance, **book_data)
                for category_data in categories_data:
                    category, _ = Category.objects.get_or_create(**category_data)
                    book.categories.add(category)
                existing_books = existing_books.exclude(pk=book.pk)
            # Delete books not present in the updated data
            #existing_books.delete()
        
        return instance
    
    
