from django.db import models
from rest_framework import viewsets
from rest_framework.response import Response

from downloads.models import Movie, Adult, Educational


class SearchPost(viewsets.ViewSet):
    @staticmethod
    def search(request):
        filters = request.GET
        search_query = filters['query']
        filtering_type = filters['filtering_type'].split('-')
        if 'all' in filtering_type:
            filtering_type = [
                'movies',
                'adult',
                'educational',
            ]
        all_search = {'movies': [], 'adult': [], 'educational': [], 'youtube': []}
        if 'movies' in filtering_type:
            movies = Movie.objects.filter(
                models.Q(name__contains=search_query) | models.Q(description__contains=search_query) | models.Q(
                    farsi_name__contains=search_query) |
                models.Q(genres__contains=['Action']))
            all_search['movies'] = movies.values()
        if 'adult' in filtering_type:
            adult = Adult.objects.filter(
                models.Q(name__contains=search_query) | models.Q(description__contains=search_query) | models.Q(
                    farsi_name__contains=search_query))
            all_search['adult'] = adult.values()

        if 'educational' in filtering_type:
            educational = Educational.objects.filter(
                models.Q(name__contains=search_query) | models.Q(description__contains=search_query) | models.Q(
                    farsi_name__contains=search_query))
            all_search['educational'] = educational.values()

        return Response({'status': 'success', 'code': 200, 'data': all_search, 'message': ''})
