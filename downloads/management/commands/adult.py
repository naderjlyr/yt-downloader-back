import datetime
import sys
import traceback

from django.core.management.base import BaseCommand
import time

from downloads.models import Adult
from downloads.view.adult.youjizz import get_all_ids_ujz, get_single_movie_ujz


def set_sleep(seconds):
    # return None
    time.sleep(seconds)


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        report_log = open('report_log.txt', 'a', encoding="utf-8")
        report_log.write(" \n" + str(datetime.datetime.now()) + " _______Crawling starts_______ \n ")
        log_counter = 0
        for page_number in range(1, 100):
            all_ids = get_all_ids_ujz(page_number=str(page_number))
            for movie_id in all_ids:
                ujz_single_movie = get_single_movie_ujz(movie_id)
                try:
                    Adult.objects.create(**{'name': ujz_single_movie['name'],
                                            'farsi_name': ujz_single_movie['farsi_name'],
                                            'description': ujz_single_movie['description'],
                                            'movie_id': ujz_single_movie['movie_id'],
                                            'genres': ujz_single_movie['genres'],
                                            'image': ujz_single_movie['image'],
                                            'download_links': ujz_single_movie['download_links'],
                                            }

                                         )
                    log_counter += 1
                except BaseException as _:
                    ex_type, ex_value, ex_traceback = sys.exc_info()
                    trace_back = traceback.extract_tb(ex_traceback)
                    stack_trace = list()
                    for trace in trace_back:
                        stack_trace.append(
                            "File : %s , Line : %d, Func.Name : %s, Message : %s" % (
                                trace[0], trace[1], trace[2], trace[3]))
                    report_log.write("\n Exception type : %s " % ex_type.__name__)
                    report_log.write("\n Exception message : %s" % ex_value)
                    report_log.write("\n Stack trace : %s" % stack_trace)
                    report_log.write("\n URL ADULT : %s" % ujz_single_movie)
                    report_log.write("\n" + "movie count: " + str(log_counter))
                    report_log.close()
        report_log.write("\n" + "movie count: " + str(log_counter))
        report_log.close()
