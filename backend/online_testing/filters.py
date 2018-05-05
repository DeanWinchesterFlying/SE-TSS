from django.db.models import Q
from rest_framework import filters


class QuestionFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        tag_list = request.data.get('tag_list')
        if not tag_list or len(tag_list) == 0:
            return queryset
        q = Q()
        for tag in tag_list:
            q = q | Q(tag=tag)
        return queryset.filter(q)