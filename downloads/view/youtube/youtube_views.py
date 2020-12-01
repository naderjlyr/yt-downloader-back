from __future__ import unicode_literals
import json
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
import requests
import youtube_dlc as youtube_dl

from downloads.view.youtube.youtube_functions import get_mp3, get_playlist, single_url, get_single_detail, YOUTUBE_URL, \
    youtube_payload, YOUTUBE_HEADER, youtube_multiple_queries


class DownloadVideo(viewsets.ViewSet):
    permission_classes = [AllowAny]

    @staticmethod
    def generate_youtube_url(request):
        data = request.data
        video_link = data['video_link']
        format_id = None
        if 'format_id' in data.keys():
            format_id = data['format_id']
        if format_id == 'mp3':
            file_path = get_mp3(video_link)
            response = {"status": "success", "code": status.HTTP_200_OK,
                        "data": {
                            "formats": {"mp3": [{"format": "audio", "extension": "mp3", "url": str(file_path[0]),
                                                 "title": str(file_path[1])}]}}, "message": []}

            return Response(response, status=status.HTTP_200_OK)
        ydl = youtube_dl.YoutubeDL({})
        try:
            with ydl:
                result = ydl.extract_info(video_link, download=False)

            video_information = {}
            if video_link.__contains__("&list="):
                get_playlist(video_information, result, format_id)
            else:
                video_information = single_url(format_id, video_link)
            response = {"status": "success", "code": status.HTTP_200_OK, "data": video_information, "message": []}
            if len(video_information) == 0:
                response = {"status": "error", "code": status.HTTP_204_NO_CONTENT,
                            "data": {"message": "no content found"}, "message": []}
        except:
            response = {"status": "error", "code": status.HTTP_204_NO_CONTENT,
                        "data": {"message": "no content found"}, "message": []}

        return Response(response, status=status.HTTP_200_OK)
        # except BaseException as ex:
        #     ex_type, ex_value, ex_traceback = sys.exc_info()
        #     trace_back = traceback.extract_tb(ex_traceback)
        #     stack_trace = list()
        #     for trace in trace_back:
        #         stack_trace.append(
        #             "File : %s , Line : %d, Func.Name : %s, Message : %s" % (trace[0], trace[1], trace[2], trace[3]))
        #     f = open("crawler_log.txt", 'a', encoding="utf-8")
        #     f.write("\n Exception type : %s " % ex_type.__name__)
        #     f.write("\n Exception message : %s" % ex_value)
        #     f.write("\n Stack trace : %s" % stack_trace)
        #     f.write("\n URL : %s" % video_link)
        #     f.close()
        #     response = {"status": "error", "code": status.HTTP_204_NO_CONTENT, "data": {"message": "no content found"},
        #                 "message": []}
        #
        #     return Response(response, status=status.HTTP_204_NO_CONTENT)

    # TODO 1- if query phrase had https or youtube, just get the link
    @staticmethod
    def youtube_query(request):

        data = request.data
        query_phrase = data['query_phrase']
        if query_phrase.startswith("www.youtube.com"):
            query_phrase = "https://" + query_phrase
        elif query_phrase.startswith("youtube.com"):
            query_phrase = "https://www." + query_phrase
        if query_phrase.startswith("https://www.youtube.com"):
            video_detail = get_single_detail(query_phrase)
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
            response = youtube_multiple_queries(query_phrase)
        return Response(response)

    @staticmethod
    def youtube_auto_suggest(request):
        data = dict(request.GET)

        query_phrase = data['query_phrase'][0]
        # print(query_phrase)
        url = "https://clients1.google.com/complete/search?client=youtube&hl=en&gl=tr&sugexp=ytdw_ce8%2Cytpo.bo.se%3D1%2Cytposo.bo.me%3D1%2Cytpo.bo.so.dw%3D1%2Cytpo.bo.so.dwm%3D3%2Cytpo.bo.so.dwb%3D10.0%2Cytposo.bo.so.dw%3D1%2Cytposo.bo.so.dwm%3D3%2Cytposo.bo.so.dwb%3D10.0%2Ccfro%3D1%2Cytpo.bo.se%3D0%2Cytposo.bo.me%3D0&gs_rn=64&gs_ri=youtube&tok=amKdy-mnxoPRnW9tgI9zCA&ds=yt&cp=6&gs_id=q&q=" + query_phrase + "&callback=google.sbox.p50&gs_gbg=hrtb1SEDV5N0hD64kFUrjT0QjNVjE9O"

        payload = {}
        headers = {
            'authority': 'clients1.google.com',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
            'accept': '*/*',
            'x-client-data': 'CIu2yQEIorbJAQjEtskBCKmdygEIlqzKAQisx8oBCPbHygEI6cjKAQi0y8oBCNzVygEImJrLARiKwcoB',
            'sec-fetch-site': 'cross-site',
            'sec-fetch-mode': 'no-cors',
            'sec-fetch-dest': 'script',
            'referer': 'https://www.youtube.com/',
            'accept-language': 'en-US,en;q=0.9,tr-TR;q=0.8,tr;q=0.7',
            'cookie': 'CONSENT=YES+RU.en+20161120-18-0; __Secure-3PAPISID=oUbIMxMt839AqcNc/A50d9Gl02LFn7lXWm; __Secure-3PSID=2Afh5Nv3JLDpNlfOM4eVz2tuUSKv1Ulv9NAJQL2buPkCuoeUDPiaJylKGz5WB-NIqq8UYw.; NID=204=oSBYio-H8M_d4a0s1ASKQJ2En-1INWKL9Eq4zzZMX_xfYh5zOe2FBFkZNJy6oph2ayRWTuyDMZoZJ9_XIjdmi6KatpnoPjBl49VhRjx7jtQivtUVXciAqf4GjSzsFy8FemH3i8UYymvwcLFUHQMZoMZcKxOiyJB7kZPb9I7FlvsluIonHfKk4z6-2817D3518R_9Y34nNXBwuoNV7xaATneGrINxRmFgtWDO4OOvRllNWyT4swKO5J-EFp-lvWigzjN0evJ9M7KzKZ8ojpP1VLltFj8L-5Voeey2rXlcfsWkROV6URAi8nU7xd173330CYnLte921KHB; 1P_JAR=2020-11-03-04; __Secure-3PSIDCC=AJi4QfFLaAE8IRT_9HrxqxxrmdaOmRz6pfKDwGQ0pGem79mz78KKFJzkPGeJE0azL9oFbpHlhlu8; __Secure-3PSIDCC=AJi4QfHd0SqU_m1LJFh-jZv5iaawZeeQ5Dz8gINnYM1btsdUOMVsr2b9iPAIir0RHGjkfgnH06Rv'
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        suggestion_list = response.text.replace('\"', "").split(',0],[')[1:-1]
        return Response(suggestion_list[:5])
