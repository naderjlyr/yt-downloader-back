import datetime
from django.core.management.base import BaseCommand
import time

from downloads.models import Music
from downloads.view.music.functions import get_all_music_titles, ALL_GENRES
from downloads.view.music.myfreemp3 import search_music


def set_sleep(seconds):
    # return None
    time.sleep(seconds)


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        report_log = open('report_log.txt', 'a', encoding="utf-8")
        report_log.write(" \n" + str(datetime.datetime.now()) + " _______Crawling starts_______ \n ")
        log_counter = 0
        for genre_name in ALL_GENRES.keys():
            for page_number in range(2, 1000):
                try:
                    all_music_titles = get_all_music_titles(genre_name)
                except:
                    print("broken")
                    break
                for music_title in all_music_titles:
                    musics_detail = search_music(music_title, 1)
                    for music_detail in musics_detail:
                        print(music_detail)
                        a = Music.objects.create(**music_detail, genre=ALL_GENRES[genre_name])
                        print(a)
        report_log.write("\n" + "music count: " + str(log_counter))
        report_log.close()
