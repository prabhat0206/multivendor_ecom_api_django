from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response


class SubCategoryMetadataPagination(LimitOffsetPagination):
    def get_paginated_response(self, data):
        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.count,
            'results': data,
            'meta': {
                "subcategory": self.queryset.filter(scid=self.kwargs.get("pk")).first().name,
                "category": self.queryset.filter(scid=self.kwargs.get("pk")).first().category.name
            }
        })