from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class ShopPaginator(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):
        print(self.page)
        return Response({
            'next': self.get_next_link(),
            'peroius': self.get_previous_link(),
            'count': self.page.paginator.num_pages,
            'current': self.page.number,
            'limit': self.page_size,
            'data': data,

        })
