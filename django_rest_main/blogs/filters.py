import django_filters
from .models import Blog

class BlogFilter(django_filters.FilterSet):
    blog_title = django_filters.CharFilter(field_name='blog_title', lookup_expr='iexact')
    blog_body = django_filters.CharFilter(field_name='blog_body', lookup_expr='icontains')

    class Meta:
        model = Blog
        fields = ['blog_title', 'blog_body']