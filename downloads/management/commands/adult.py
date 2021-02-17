import sys
import traceback

from django.core.management.base import BaseCommand
import time

from downloads.models import Adult
from downloads.view.adult.youjizz import get_all_ids_ujz, get_single_movie_ujz


def set_sleep(seconds):
    time.sleep(seconds)


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        for page_number in range(1, 1000):
            set_sleep(5)
            all_ids = get_all_ids_ujz(page_number=str(page_number))
            for movie_id in all_ids:
                ujz_single_movie = get_single_movie_ujz(movie_id)
                try:
                    # using url because movie_id is not reliable (just a random slug)
                    existing_video = Adult.objects.filter(url__exact=ujz_single_movie['url'])
                    if existing_video.count() > 0:
                        existing_video.update(
                            views=ujz_single_movie['views'],
                            rating=ujz_single_movie['rating'],
                            download_links=[ujz_single_movie['download_links']],
                        )
                    else:
                        Adult.objects.create(**{'name': ujz_single_movie['name'],
                                                'farsi_name': ujz_single_movie['farsi_name'],
                                                'description': ujz_single_movie['description'],
                                                'url': ujz_single_movie['url'],
                                                'views': ujz_single_movie['views'],
                                                'rating': ujz_single_movie['rating'],
                                                'movie_id': ujz_single_movie['movie_id'],
                                                'tags': ujz_single_movie['tags'],
                                                'image': ujz_single_movie['image'],
                                                'download_links': [ujz_single_movie['download_links']],
                                                }

                                             )


                except BaseException as _:
                    ex_type, ex_value, ex_traceback = sys.exc_info()
                    trace_back = traceback.extract_tb(ex_traceback)
                    stack_trace = list()
                    for trace in trace_back:
                        stack_trace.append(
                            "File : %s , Line : %d, Func.Name : %s, Message : %s" % (
                                trace[0], trace[1], trace[2], trace[3]))
                    print("\n Exception type : %s " % ex_type.__name__)
                    print("\n Exception message : %s" % ex_value)
                    print("\n Stack trace : %s" % stack_trace)
                    print("\n URL ADULT : %s" % ujz_single_movie)
