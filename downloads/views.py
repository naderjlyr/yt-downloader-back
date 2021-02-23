from django.db import models
from rest_framework import viewsets
from rest_framework.response import Response

from downloads.models import Movie, Adult, Educational, Music, Configs
from downloads.view.music.myfreemp3 import search_music
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
            if search_query is None or search_query == '':
                movies_query = Movie.objects.all()
            else:
                movies_query = Movie.objects.filter(
                    models.Q(name__icontains=search_query) |
                    models.Q(description__icontains=search_query) |
                    models.Q(farsi_name__icontains=search_query) |
                    models.Q(genres__icontains=[search_query])
                )
            movies_data = movies_query.values()
            movies = {'type': 'movie', 'data': movies_data[:20]}
            all_search.append(movies)
        if 'adult' in filtering_type:
            if search_query is None or search_query == '':
                adult_query = Adult.objects.all()
            else:
                adult_query = Adult.objects.filter(
                    models.Q(name__icontains=search_query) |
                    models.Q(description__icontains=search_query) |
                    models.Q(farsi_name__icontains=search_query) |
                    models.Q(tags__icontains=[search_query])
                )
            if adult_query.count() == 0:
                adult_query = Adult.objects.all()
            adult_data = adult_query.values().order_by('-created_at')
            adults = {'type': 'adult', 'data': adult_data[:40]}
            all_search.append(adults)
        if 'educational' in filtering_type:
            if search_query is None or search_query == '':
                educational_query = Educational.objects.all()
            else:
                educational_query = Educational.objects.filter(
                    models.Q(name__icontains=search_query) | models.Q(description__icontains=search_query) | models.Q(
                        farsi_name__icontains=search_query))
            educational_data = educational_query.values()
            educational = {'type': 'educational', 'data': educational_data[:20]}
            all_search.append(educational)
        if 'music' in filtering_type:
            if search_query is None or search_query == '':
                search_query = 'eminem'
            music_data = search_music(search_query)
            music = {'type': 'music', 'data': music_data[:20]}
            all_search.append(music)
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
        Configs.objects.create(
            search_name=search_query,
            search_type=filtering_type,
            result_count=len(all_search[0]['data']),
        )
        return Response({'status': 'success', 'code': 200, 'data': all_search, 'message': ''})


def test(request):
    pass
