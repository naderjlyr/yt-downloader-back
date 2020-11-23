from __future__ import unicode_literals
import json
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
import requests
import youtube_dlc as youtube_dl

from downloads.view.youtube.youtube_functions import get_mp3, get_playlist, single_url, get_single_detail


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
            url = "https://www.youtube.com/youtubei/v1/search?key=AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8"
            payload = "{\"context\":{\"client\":{\"hl\":\"en\",\"gl\":\"TR\",\"geo\":\"TR\",\"remoteHost\"" \
                      ":\"178.244.119.96\",\"isInternal\":true,\"deviceMake\":\"\",\"deviceModel\":\"\"," \
                      "\"visitorData\":\"CgstSE92QkNyMkR6dyijy4P9BQ%3D%3D\",\"userAgent\":\"Mozilla/5.0" \
                      " (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)" \
                      " Chrome/86.0.4240.111 Safari/537.36,gzip(gfe)\",\"cli" \
                      "entName\":\"WEB\",\"clientVersion\":\"2.20201101.02.00\",\"osName\":\"Windows\",\"osVersion" \
                      "\":\"10.0\",\"originalUrl\":\"https://www.youtube.com/results?search_query=ich+will\"" \
                      ",\"playerT" \
                      "ype\":\"UNIPLAYER\",\"gfeFrontlineInfo\":\"vip=172.217.169.110,server_port=443," \
                      "client_port=39909," \
                      "tcp_connection_request_count=0,header_order=HUAEL,gfe_version=2.693.1,ssl,ssl_info" \
                      "=TLSv1.3:RNA:T,tlsext=S,sni=www.youtube.com,hex_encoded_client_hello=6a6a130113021303c0" \
                      "2bc02fc02cc030cca9cca8c013c014009c009d002f0035-00-fafa00000017ff01000a000b002300100005000d00" \
                      "120033002d002b001b9a9a0015,c=1301,pn=alpn,ja3=b32309a26951912be7dba376398abc3b,rtt_source=tc" \
                      "p,rtt=34,srtt=34,client_protocol=h2,client_transport=tcp,first_request=1,ip_block_version=1,ip" \
                      "_block_index=980205,gfe=acsofg9,pzf=Linux 2.2.x-3.x [4:54+10:0:1420:65535/10:mss/sok/ts/nop" \
                      "/ws:d" \
                      "f/id+:0] [generic tos:0x20],vip_region=default,asn=16135,cc=TR,eid=o-WgX9nqK8nV8wfn7J6ACg,sch" \
                      "eme=https\",\"clientFormFactor\":\"UNKNOWN_FORM_FACTOR\",\"newVisitorCookie\":true,\"" \
                      "countryLoca" \
                      "tionInfo\":{\"countryCode\":\"TR\",\"countrySource\":\"COUNTRY_SOURCE_IPGEO_INDEX\"},\"browser" \
                      "Name\":\"Chrome\",\"browserVersion\":\"86.0.4240.111\",\"screenWidthPoints\":1209,\"scre" \
                      "enHeightPoints\":208,\"screenPixelDensity\":2,\"screenDensityFloat\":1.5,\"utcOffsetMinutes" \
                      "\":180,\"userInterfaceTheme\":\"USER_INTERFACE_THEME_LIGHT\",\"connectionType\":\"CONN_CELL" \
                      "ULAR_4G\",\"mainAppWebInfo\":{\"graftUrl\":\"/results?search_query=ich+will\"}},\"user\":{\"lo" \
                      "ckedSafetyMode\":false},\"request\":{\"useSsl\":true,\"sessionId\":6890759919261400000,\"paren" \
                      "tEventId\":{\"timeUsec\":1604380067747748,\"serverIp\":182453394,\"processId\":403055733},\"" \
                      "internalExperimentFlags\":[{\"key\":\"force_share_tooltip\",\"value\":\"false\"}],\"consist" \
                      "encyTokenJars\":[]},\"clickTracking\":{\"clickTrackingParams\":" \
                      "\"IhMIpK+XwM3l7AIVkgTgCh11JAYY\"}," \
                      "\"adSignalsInfo\":{\"consentBumpParams\":{\"consentHostnameOverride\":\"" \
                      "https://www.youtube.com\"," \
                      "\"urlOverride\":\"\"}}},\"query\":\"" + query_phrase + "\",\"consentBumpParams\":{" \
                                                                              "\"consentHostnameOverride\":\"" \
                                                                              "https://www.youtube.com\",\"url" \
                                                                              "Override\":\"\"}," \
                                                                              "\"webSearchboxStatsUrl\":\"/s" \
                                                                              "earch?oq=" + str(
                query_phrase) + \
                      "&gs_l=youtube.12...0.0.0.3454.0.0.0.0.0.0.0.0..0.0.ytdw_cc9,ytpo-bo-se=0,ytposo-bo-me=0," \
                      "cfro=1,ytpo-bo-se=1,ytposo-bo-me=1,ytpo-bo-so-dw=1,ytpo-bo-so-dwm=3,ytpo-bo-so-dwb=100-0," \
                      "ytposo-bo-so-dw=1,ytposo-bo-so-dwm=3,ytposo-bo-so-dwb=100-0" \
                      "...0...1ac..64.youtube..0.0.0....0.\"} "
            headers = {
                'authority': 'www.youtube.com',
                'pragma': 'no-cache',
                'cache-control': 'no-cache',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/86.0.4240.111 Safari/537.36',
                'x-goog-visitor-id': 'CgstSE92QkNyMkR6dyijy4P9BQ%3D%3D',
                'content-type': 'application/json',
                'accept': '*/*',
                'origin': 'https://www.youtube.com',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-mode': 'same-origin',
                'sec-fetch-dest': 'empty',
                'referer': 'https://www.youtube.com/results?search_query=ich+will',
                'accept-language': 'en-US,en;q=0.9',
                'cookie': 'YSC=42bhoyRJBxk; VISITOR_INFO1_LIVE=-HOvBCr2Dzw; PREF=f4=4000000; ST-1l9ld2b='
                          'oq=ich%20will&gs_l=youtube.12...0.0.0.3454.0.0.0.0.0.0.0.0..0.0.ytdw_cc9%2Cytpo'
                          '-bo-se%3D0%2Cytposo-bo-me%3D0%2Ccfro%3D1%2Cytpo-bo-se%3D1%2Cytposo-bo-me%3D1%'
                          '2Cytpo-bo-so-dw%3D1%2Cytpo-bo-so-dwm%3D3%2Cytpo-bo-so-dwb%3D100-0%2Cytposo-bo-'
                          'so-dw%3D1%2Cytposo-bo-so-dwm%3D3%2Cytposo-bo-so-dwb%3D100-0...0...1ac..64.youtube'
                          '..0.0.0....0.&itct=CBkQ7VAiEwjSxZjAzeXsAhVEHuAKHT8cCnI%3D&csn=MC4zOTA1ODIwMjAwNzk3MTI1NA'
                          '..&endpoint=%7B%22clickTrackingParams%22%3A%22CBkQ7VAiEwjSxZjAzeXsAhVEHuAKHT8cCnI%3D%22'
                          '%2C%22commandMetadata%22%3A%7B%22webCommandMetadata%22%3A%7B%22url%22%3A%22%2Fresults%'
                          '3Fsearch_query%3Dich%2Bwill%22%2C%22webPageType%22%3A%22WEB_PAGE_TYPE_SEARCH%22%2C%'
                          '22rootVe%22%3A4724%7D%7D%2C%22searchEndpoint%22%3A%7B%22query%22%3A%22ich%20will%22%7D%7D; '
                          'SIDCC=AJi4QfHG-7hHvSiRHFqxEFJNjaNsI38pe4qMVQP7ai5NpZ6GkZygcxt7PCsDEFVac4HDhbU3gA; '
                          '__Secure-3PSIDCC=AJi4QfElnlc41NICzjaRiqEqJ49DjtDmwBAAa0yBeq34PA3_UAQjd3WcPeTNdwXSVuKNKvTnqA '
            }

            response = requests.request("POST", url, headers=headers, data=payload.encode('utf-8'))
            query_result_items = \
                json.loads(response.text)['contents']['twoColumnSearchResultsRenderer']['primaryContents'][
                    'sectionListRenderer']['contents']
            all_items_detail = []
            for item in query_result_items:
                if 'itemSectionRenderer' in item.keys():
                    item_contents = item['itemSectionRenderer']['contents']
                    for item_content in item_contents:
                        if 'videoRenderer' in item_content.keys():
                            item_content = item_content['videoRenderer']
                            video_id = item_content['videoId']
                            image = item_content['thumbnail']['thumbnails'][0]['url']
                            title = item_content['title']['runs'][0]['text']
                            published_time_text = ""
                            if "publishedTimeText" in item_content.keys():
                                published_time_text = item_content['publishedTimeText']['simpleText']
                            video_duration = ''
                            if 'lengthText' in item_content.keys():
                                video_duration = item_content['lengthText']['simpleText']
                            view_count_text = ""
                            if "viewCountText" in item_content.keys():
                                view_count_text = item_content['viewCountText']['simpleText']
                            owner_text = item_content['ownerText']['runs'][0]['text']
                            description = ""
                            if "descriptionSnippet" in item_content.keys():
                                description = item_content['descriptionSnippet']['runs']
                                description = ' '.join([desc_item['text'] for desc_item in description])
                            video_url = "https://www.youtube.com/watch?v=" + video_id
                            all_items_detail.append(
                                {
                                    "published_time_text": published_time_text,
                                    "video_duration": video_duration,
                                    "view_count_text": view_count_text,
                                    "owner_text": owner_text,
                                    "video_id": video_id,
                                    "url": video_url,
                                    "image": image,
                                    "title": title,
                                    "description": description,
                                })
            response = {
                "status": "success",
                "data": all_items_detail
            }
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
