from django.db import models
from rest_framework import viewsets
from rest_framework.response import Response

from downloads.models import Movie, Adult, Educational, Music
from downloads.view.youtube.youtube_functions import get_single_detail, youtube_multiple_queries


class SearchPost(viewsets.ViewSet):
    @staticmethod
    def search(request):
        filters = request.GET
        search_query = filters['query']
        filtering_type = filters['filtering_type'].split('-')
        if 'all' in filtering_type:
            filtering_type = [
                'movie',
                'adult',
                'youtube',
                'educational',
                'music',
            ]
        all_search = []
        if 'movie' in filtering_type:
            movies_query = Movie.objects.filter(
                models.Q(name__icontains=search_query) | models.Q(description__icontains=search_query) | models.Q(
                    farsi_name__icontains=search_query) |
                models.Q(genres__icontains=['Action']))
            movies_data = movies_query.values()
            movies = {'type': 'movie', 'data': movies_data[:10]}
            all_search.append(movies)
        if 'adult' in filtering_type:
            adult_query = Adult.objects.filter(
                models.Q(name__icontains=search_query) | models.Q(description__icontains=search_query) | models.Q(
                    farsi_name__icontains=search_query))
            adult_data = adult_query.values()
            adults = {'type': 'adult', 'data': adult_data}
            all_search.append(adults)
        if 'educational' in filtering_type:
            educational_query = Educational.objects.filter(
                models.Q(name__icontains=search_query) | models.Q(description__icontains=search_query) | models.Q(
                    farsi_name__icontains=search_query))
            educational_data = educational_query.values()
            educational = {'type': 'educational', 'data': educational_data}
            all_search.append(educational)
        if 'music' in filtering_type:
            educational_query = Music.objects.filter(
                models.Q(name__icontains=search_query) |
                models.Q(description__icontains=search_query) |
                models.Q(artist__icontains=search_query) |
                models.Q(genre__icontains=search_query)
            )
            educational_data = educational_query.values()
            educational = {'type': 'educational', 'data': educational_data}
            all_search.append(educational)
        if 'youtube' in filtering_type:
            if search_query.startswith("www.youtube.com"):
                search_query = "https://" + search_query
            elif search_query.startswith("youtube.com"):
                search_query = "https://www." + search_query
            if search_query.startswith("https://www.youtube.com"):
                video_detail = get_single_detail(search_query)
                youtube_data = [{
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
            else:
                youtube_data = youtube_multiple_queries(search_query)
            youtube = {'type': 'youtube', 'data': youtube_data}
            all_search.append(youtube)
        return Response({'status': 'success', 'code': 200, 'data': all_search, 'message': ''})


def test(request):
    pass
