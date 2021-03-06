import json
import requests
from downloads.view.music.functions import d, myfreemp3_header


def search_music(query_string: str, page_number: int = 0):
    url = "https://myfreemp3.vip/api/search.php?callback=jQuery21307991881983452356_1607376745847"
    payload = "q=" + query_string + "&page=" + str(page_number)
    headers = myfreemp3_header
    response = requests.request("POST", url, headers=headers, data=payload.encode('utf-8'))
    songs_details = json.loads('('.join(response.text[:-2].split("(")[1:]))
    all_musics = []
    if 'response' in songs_details.keys():
        try:
            for song_details in songs_details['response']:
                if isinstance(song_details, dict):
                    owner_id_ = song_details['owner_id']
                    details_id_ = song_details['id']
                    video_id = d(owner_id_) + ":" + d(details_id_)
                    download_link = "https://speed.idmp3s.com/" + video_id
                    single_url = "https://freemp3downloads.cc/api/get_song.php?id=" + video_id
                    all_musics.append({
                        "name": song_details['title'],
                        "artist": song_details['artist'],
                        "duration": song_details['duration'],
                        "url": single_url,
                        "download_link": download_link,
                        "image": song_details['album']['thumb'][
                            'photo_600'] if "album" in song_details.keys() else None,
                    })
        except:
            print(songs_details)
    return all_musics
