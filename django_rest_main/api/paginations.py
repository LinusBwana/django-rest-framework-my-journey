from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework.response import Response

class CustomPagination(PageNumberPagination, LimitOffsetPagination):
    page_size_query_param = 'page_size'
    page_query_param = 'page_num'
    max_page_size = 10

    def get_paginated_response(self, data):
        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count,
            'page_size': self.page_size,
            'results': data
        })