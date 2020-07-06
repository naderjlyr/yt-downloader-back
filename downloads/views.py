import json
import sys
import traceback

import youtube_dl
from http.client import HTTPResponse

from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


class DownloadVideo(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            data = request.data
            video_link = data['video_link']
            ydl = youtube_dl.YoutubeDL({'format': 'bestaudio/best',
                                        'postprocessors': [{
                                            'key': 'FFmpegExtractAudio',
                                            'preferredcodec': 'mp3',
                                            'preferredquality': '192',
                                        }]})

            with ydl:
                result = ydl.extract_info(
                    video_link,
                    download=False
                )

            if 'entries' in result:
                video = result['entries'][0]
            else:
                video = result

            video_urls = video['formats']
            output = {}
            formatted_file = []
            for video_url in video_urls:
                output['url'] = video_url['url']
                output['extension'] = video_url['ext']
                output['size'] = video_url['filesize']
                output['format'] = video_url['format'].split(' - ')[1]
                formatted_file.append(output)
            response = {"status": "success", "code": status.HTTP_200_OK, "data": formatted_file, "message": []}

            return Response(response, status=status.HTTP_200_OK)
        except BaseException as ex:
            ex_type, ex_value, ex_traceback = sys.exc_info()
            trace_back = traceback.extract_tb(ex_traceback)
            stack_trace = list()
            for trace in trace_back:
                stack_trace.append(
                    "File : %s , Line : %d, Func.Name : %s, Message : %s" % (trace[0], trace[1], trace[2], trace[3]))
            f = open("crawler_log.txt", 'a', encoding="utf-8")
            f.write("\n Exception type : %s " % ex_type.__name__)
            f.write("\n Exception message : %s" % ex_value)
            f.write("\n Stack trace : %s" % stack_trace)
            f.write("\n URL : %s" % video_link)
            f.close()

    def get(self, request):
        test_count = 0
        for _ in range(1000):
            video_link = "https://www.youtube.com/watch?v=ZJMHUG3bdao"
            ydl = youtube_dl.YoutubeDL({'format': 'bestaudio/best',
                                        'postprocessors': [{
                                            'key': 'FFmpegExtractAudio',
                                            'preferredcodec': 'mp3',
                                            'preferredquality': '192',
                                        }]})

            with ydl:
                result = ydl.extract_info(
                    video_link,
                    download=False
                )
            if 'entries' in result:
                video = result['entries'][0]
            else:
                video = result
            video_urls = video['formats']
            for video_url in video_urls:
                print(video_url['url'])
                test_count += 1
                break

            print(test_count)
            print("**********SUCCESS************")
