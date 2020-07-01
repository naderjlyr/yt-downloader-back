import youtube_dl
from http.client import HTTPResponse

from django.shortcuts import render


def get_link(request):
    return render(request, 'get_link.html')


def download_links(request):
    video_link = request.POST['video_link']
    # ydl_opts = {
    #     'format': 'bestaudio/best',
    #     'postprocessors': [{
    #         'key': 'FFmpegExtractAudio',
    #         'preferredcodec': 'mp3',
    #         'preferredquality': '192',
    #     }],
    #     'logger': MyLogger(),
    #     'progress_hooks': [my_hook],
    # }
    # with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    #     ydl.download(['https://www.youtube.com/watch?v=BaW_jenozKc'])
    # 'outtmpl': '%(id)s%(ext)s',
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
    return render(request, 'download_links.html', context={"urls":video_urls})
