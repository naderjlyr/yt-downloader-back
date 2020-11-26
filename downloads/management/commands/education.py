import datetime
import sys
import traceback

from django.core.management.base import BaseCommand
import time

from downloads.models import Movie, Educational
from downloads.view.educational.udemy import get_all_udemy_links, get_single_udemy
from downloads.view.movie.movie_views import get_all_genres, get_all_movie_imdb_ids, get_single_movie


def set_sleep(seconds):
    # return None
    time.sleep(seconds)


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        report_log = open('report_log.txt', 'a', encoding="utf-8")
        report_log.write(" \n" + str(datetime.datetime.now()) + " _______Crawling starts_______ \n ")
        log_counter = 0
        for page_number in range(1, 100):
            for url_slug in get_all_udemy_links(page_number=page_number):
                single_udemy = get_single_udemy(url_slug)
                print(single_udemy)
                # try:
                Educational.objects.create(**single_udemy)
                log_counter += 1
                # except BaseException as _:
                #     ex_type, ex_value, ex_traceback = sys.exc_info()
                #     trace_back = traceback.extract_tb(ex_traceback)
                #     stack_trace = list()
                #     for trace in trace_back:
                #         stack_trace.append(
                #             "File : %s , Line : %d, Func.Name : %s, Message : %s" % (
                #                 trace[0], trace[1], trace[2], trace[3]))
                #     report_log.write("\n Exception type : %s " % ex_type.__name__)
                #     report_log.write("\n Exception message : %s" % ex_value)
                #     report_log.write("\n Stack trace : %s" % stack_trace)
                #     report_log.write("\n URL UDEMY: %s" % single_udemy)
                #     report_log.write("\n" + "movie count: " + str(log_counter))
                #     report_log.close()
        report_log.write("\n" + "movie count: " + str(log_counter))
        report_log.close()
