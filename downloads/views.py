from django.db import models
from rest_framework import viewsets
from rest_framework.response import Response

from downloads.models import Movie, Adult, Educational
from downloads.view.youtube.youtube_functions import get_single_detail, youtube_multiple_queries


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
        if 'youtube' in filtering_type:
            if search_query.startswith("www.youtube.com"):
                search_query = "https://" + search_query
            elif search_query.startswith("youtube.com"):
                search_query = "https://www." + search_query
            if search_query.startswith("https://www.youtube.com"):
                video_detail = get_single_detail(search_query)
                response = {
                    "status": "success",
                    "data": [{
                        "published_time_text": "",
                        "video_duration": "",
                        "view_count_text": "",
                        "owner_text": "",
                        "video_id": video_detail['video_id'],
                        "url": video_detail['url'],
                        "image": video_detail['image'],
                        "title": video_detail['title'],
                        "description": video_detail['description'],
                    }]
                }
            else:
                response = youtube_multiple_queries(search_query)

        return Response({'status': 'success', 'code': 200, 'data': all_search, 'message': ''})
