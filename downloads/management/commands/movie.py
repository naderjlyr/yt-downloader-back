import datetime
import sys
import traceback

from django.core.management.base import BaseCommand
import time

from downloads.choices import MoviesChoices
from downloads.models import Movie
from downloads.view.movie.movie_views import get_all_genres, get_all_movie_imdb_ids, get_single_movie


def set_sleep(seconds):
    # return None
    time.sleep(seconds)


def get_azintv_movie(movie_type: str, page_number: str):
    """

    :param page_number:
    :type movie_type: str
    """
    all_genres = get_all_genres()
    log_counter = 0
    for genre in all_genres[movie_type]:
        imdb_ids = get_all_movie_imdb_ids(genre, film_type=movie_type, page_number=page_number)
        for imdb_id in imdb_ids:
            log_counter += 1
            set_sleep(5)
            single_movie = get_single_movie(imdb_id, film_type=movie_type)
            try:
                Movie.objects.create(**{
                    'name': single_movie['name'],
                    'farsi_name': single_movie['farsi_name'],
                    'description': single_movie['description'],
                    'movie_id': single_movie['imdb_id'],
                    'genres': single_movie['genres'],
                    'image': single_movie['image'],
                    'download_links': single_movie['download_links'],
                    'country': single_movie['country'],
                    'year': single_movie['year'],
                    'movie_type': movie_type,
                    'main_language': single_movie['main_language'],
                    'subtitles': single_movie['subtitles'],
                    'duration': single_movie['duration'],
                    'imdb_rate': single_movie['imdb_rate']
                })
                set_sleep(2)
            except BaseException as _:
                ex_type, ex_value, ex_traceback = sys.exc_info()
                trace_back = traceback.extract_tb(ex_traceback)
                stack_trace = list()
                for trace in trace_back:
                    stack_trace.append(
                        "File : %s , Line : %d, Func.Name : %s, Message : %s" % (
                            trace[0], trace[1], trace[2], trace[3]))
                report_log = open('error_log.txt', 'a', encoding="utf-8")
                report_log.write("\n Exception type : %s " % ex_type.__name__)
                report_log.write("\n Exception message : %s" % ex_value)
                report_log.write("\n Stack trace : %s" % stack_trace)
                report_log.write("\n URL : %s" % single_movie)
                report_log.write("\n" + movie_type + " movie count: " + str(log_counter))
                report_log.close()


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        for p_n in range(1, 100):
            get_azintv_movie(MoviesChoices.MOVIE, page_number=str(p_n))
            set_sleep(10)
        print("********* MOVIES FINISHED *********")
        for p_n in range(1, 100):
            get_azintv_movie(MoviesChoices.SERIES, page_number=str(p_n))
            set_sleep(10)
