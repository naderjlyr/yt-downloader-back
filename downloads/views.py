from __future__ import unicode_literals

import sys
from datetime import datetime
from shutil import copyfile
import youtube_dlc as youtube_dl
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
import os
from django.conf import settings


class DownloadVideo(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        video_link = data['video_link']
        if video_link.startswith("www.youtube.com"):
            video_link = "https://" + video_link
        elif video_link.startswith("youtube.com"):
            video_link = "https://www." + video_link

        format_id = None
        if "format" in data.keys():
            format_id = data['format']
        if format_id == 'mp3':
            file_path = self.get_mp3(video_link)
            response = {"status": "success", "code": status.HTTP_200_OK,
                        "data": {"formats": {"mp3": [{"format": "audio", "extension": "mp3", "url": str(file_path[0]),
                                                      "title": str(file_path[1])}]}}, "message": []}

            return Response(response, status=status.HTTP_200_OK)
        ydl = youtube_dl.YoutubeDL({})

        with ydl:
            result = ydl.extract_info(video_link, download=False)
        video_information = {}
        if video_link.__contains__("&list="):
            self.get_playlist(video_information, result, format_id)
        else:
            video_information = self.single_url(format_id, video_link)

        response = {"status": "success", "code": status.HTTP_200_OK, "data": video_information, "message": []}
        if len(video_information) == 0:
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

    def get_mp3(self, video_link):
        class MyLogger(object):
            def debug(self, msg):
                pass

            def warning(self, msg):
                pass

            def error(self, msg):
                print(msg)

        def my_hook(d):
            if d['status'] == 'finished':
                global path_name
                path_name = d['filename']
                return d
                # print(d)
                # print('Done downloading, now converting ...')

        now = datetime.now().timestamp()
        media_dir = settings.MEDIA_ROOT
        new_file_name = 'downloaded_files/' + str(now) + '.mp3'
        new_file_path = os.path.join(media_dir, new_file_name)

        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '140',
            }],
            'outtmpl': new_file_path,
            'logger': MyLogger(),
            'progress_hooks': [my_hook],
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_link])
        return ["/media/" + str(new_file_name), new_file_name]

    def get_playlist(self, playlist_links, result, format_id):
        playlist_links['playlist'] = True
        playlist_links['formats'] = {}
        for slug in result['entries']:
            single_format_ids = slug['formats']
            for single_format in single_format_ids:
                if format_id is not None:
                    if str(single_format['format_id']) != str(format_id):
                        continue
                required_info = {
                    'url': single_format['url'], 'title': slug['title'],
                    'image': slug['thumbnails'][0]['url'],

                    'extension': single_format['ext'],
                    'size': single_format['filesize'],
                    'format_id': single_format['format_id'],
                    'format': single_format['format'].split(' - ')[1]}
                if single_format['format_id'] in playlist_links['formats'].keys():
                    playlist_links['formats'][single_format['format_id']].append(required_info)
                else:
                    playlist_links['formats'][single_format['format_id']] = [required_info]

    def single_url(self, format_id, video_link):
        downloader_params = {
            "format": "bestaudio",
        }
        downloader_params["postprocessors"] = [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }]
        ydl = youtube_dl.YoutubeDL({'audioformat': "mp3",
                                    })

        with ydl:
            result = ydl.extract_info(video_link, download=False)
        if 'entries' in result:
            video = result['entries'][0]
        else:
            video = result

        video_urls = video['formats']
        formatted_file = {"playlist": False, 'formats': {'0': []}}

        for video_url in video_urls:
            output = {'title': result['title'], 'image': result['thumbnails'][0]['url'], 'url': video_url['url'],
                      'extension': video_url['ext'],
                      'size': video_url['filesize'],
                      'format_id': video_url['format_id'], 'format': video_url['format'].split(' - ')[1]}
            if format_id is not None:
                if str(video_url['format_id']) == str(format_id):
                    formatted_file['formats']['0'].append(output)
            else:
                formatted_file['formats']['0'].append(output)
        return formatted_file

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
