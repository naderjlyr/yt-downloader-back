from __future__ import unicode_literals
from datetime import datetime
import youtube_dlc as youtube_dl
import os
import requests
import json
from django.conf import settings


def get_single_detail(video_url):
    payload = {}
    headers = {
        'authority': 'www.youtube.com',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'x-youtube-sts': '18568',
        'x-youtube-csoc': '1',
        'x-youtube-device': 'cbr=Chrome&cbrver=86.0.4240.111&ceng=WebKit&cengver=537.36&cos=Windows&cosver=10.0',
        'x-youtube-page-label': 'youtube.ytfe.desktop_20201102_1_RC0',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/86.0.4240.111 Safari/537.36',
        'x-youtube-variants-checksum': '02834563a6e88936f92346c43af475d8',
        'x-youtube-page-cl': '340235948',
        'x-spf-referer': 'https://www.youtube.com/',
        'x-youtube-utc-offset': '180',
        'x-youtube-client-name': '1',
        'x-spf-previous': 'https://www.youtube.com/',
        'x-youtube-client-version': '2.20201102.01.00',
        'x-youtube-identity-token': 'QUFFLUhqbkliRXUyRWpQalRmV2RBQXpWYnVINHRrRktUZ3w=',
        'x-youtube-time-zone': 'Europe/Istanbul',
        'x-youtube-ad-signals': 'dt=1604516865234&flash=0&frm&u_tz=180&u_his=2&u_java&u_h=720&u_w=1280&u_ah=720&u_aw'
                                '=1209&u_cd=24&u_nplug=3&u_nmime=4&bc=31&bih=333&biw=1193&brdim=71%2C0%2C71%2C0'
                                '%2C1209%2C0%2C1209%2C720%2C1209%2C333&vis=1&wgl=true&ca_type=image',
        'accept': '*/*',
        'x-client-data': 'CIu2yQEIorbJAQjEtskBCKmdygEIlqzKAQisx8oBCPbHygEI6cjKAQi0y8oBCNzVygEImJrLARiKwcoB',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.youtube.com/',
        'accept-language': 'en-US,en;q=0.9,tr-TR;q=0.8,tr;q=0.7',
        'cookie': 'VISITOR_INFO1_LIVE=M_PN6nMYtJQ; CONSENT=YES+RU.en+20161120-18-0; HSID=ASA4agaSVCzxmIp_l; '
                  'SSID=ArKRF6rlLmKhjeyOI; APISID=6-LV23RVMG5Pvs7V/AL45IPW1hDg8b3xgr; '
                  'SAPISID=oUbIMxMt839AqcNc/A50d9Gl02LFn7lXWm; __Secure-3PAPISID=oUbIMxMt839AqcNc/A50d9Gl02LFn7lXWm; '
                  'LOGIN_INFO=AFmmF2swRQIgExA6J_3vSYW9_WHn--NLVuAWYLpFsdkBgWoSw-JLvCECIQCVdVjBqLIyOu5mnvh8Wuif_'
                  '-MkSWv1r1903zk-gHBPCQ'
                  ':QUQ3MjNmeXVfcWtwNl80S3V4OVdYWHU2c181aTlfY2h2SUlhMVllZzFOX3l5U0VwQ2Q0R0ZTMUhIV2V4Q0YtNk1DR3prUmpx'
                  'ZHFpbjVGSkdmcmdIQUNIeVE5SG9VbGNJZUxkZ2IwWjc4czU2eGVqZzlLUHdnMW9INkw2S1g3SnJNcV8zaGZtQVowZk1JZ'
                  '1ZrcnBOZGZJdVAwTk94cjlpcGI2U2R6cjZLSnFlVV83cmxZazRHZTd2akp4dXJmejVWeS16am9IX3M5c1BH; YSC=3VP91h'
                  'HycZ8; wide=0; SID=2gfh5FiTmyN_mNhXbGikhT_t43n5KM_W8BbwiLorDAbUN7hSqBaxWAtuJ3XMWnFQ4EtPAA.;'
                  '__Secure-3PSID=2gfh5FiTmyN_mNhXbGikhT_t43n5KM_W8BbwiLorDAbUN7hST-qqzkmUkDLUf8IJqKO0_w.; '
                  'PREF=f4=4000000&al=en-DE; '
                  'SIDCC=AJi4QfF4lUMl6QNVwKfTbp1W_V0VzxvDFNxMYskoN91hpPh6xSIqiY2dqtztUQzGQWk6lutROQ; '
                  '__Secure-3PSIDCC=AJi4QfF-YmnjXJe7NQWXtpSCMjyuvlXSg4L5lQiACghC7YzbOyb7xusOoAuRVFihxiadNoqzEg; '
                  'ST-a2jg19=itct'
                  '=CIQCENwwIhMI1ZDxjMvp7AIVRodVCh23TA8KMgpnLWhpZ2gtcmVjWg9GRXdoYXRfdG9fd2F0Y2iaAQYQjh4YngE%3D&csn'
                  '=MC4wNjE0MDM4OTU2OTc5OTQzMTU.&endpoint=%7B%22clickTrackingParams%22%3A'
                  '%22CIQCENwwIhMI1ZDxjMvp7AIVRodVCh23TA8KMgpnLWhpZ2gtcmVjWg9GRXdoYXRfdG9fd2F0Y2iaAQYQjh4YngE%3D%22'
                  '%2C%22commandMetadata%22%3A%7B%22webCommandMetadata%22%3A%7B%22url%22%3A%22%2Fwatch%3Fv'
                  '%3DT55UM3UQ9w4%22%2C%22webPageType%22%3A%22WEB_PAGE_TYPE_WATCH%22%2C%22rootVe%22%3A3832%7D%7D%2C'
                  '%22watchEndpoint%22%3A%7B%22videoId%22%3A%22T55UM3UQ9w4%22%7D%7D; YSC=hRT7Q_GGDZI; '
                  'VISITOR_INFO1_LIVE=Jfus1M1p49g; '
                  'SIDCC=AJi4QfFQBUcdCsL8VnCsVfrEir0TYNDuhowWeOgaMujMWsXmTSYQt68ZjY3Dqi23m1xSDolusw; '
                  '__Secure-3PSIDCC=AJi4QfEooiQA0lV8jhfq3v3QLKi9bwuyrjzOtA_vcGoq_rGXxihN2t1knXcfFNllG0QPj-E03w '
    }

    response = requests.request("GET", video_url, headers=headers, data=payload)

    video_details = json.loads(response.text)[2]['playerResponse']['videoDetails']
    return {"video_id": video_details['videoId'], "url": "https://www.youtube.com/watch?v=" + video_details['videoId'],
            "title": video_details['title'],
            'image': video_details['thumbnail']['thumbnails'][-1]['url'],
            "description": video_details['shortDescription']}




def get_mp3(video_link):
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


def get_playlist(playlist_links, result, format_id):
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


def single_url(format_id, video_link):
    downloader_params = {"format": "bestaudio", "postprocessors": [
        {
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }]}
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
        output = {
            'url': video_url['url'],
            'extension': video_url['ext'],
            'size': video_url['filesize'],
            'format_id': video_url['format_id'], 'format': video_url['format'].split(' - ')[1]}
        if format_id is not None:
            if str(video_url['format_id']) == str(format_id):
                formatted_file['formats']['0'].append(output)
        else:
            formatted_file['formats']['0'].append(output)
    return formatted_file
