import sys
import traceback

from django.core.management.base import BaseCommand
import time

from downloads.models import Educational
from downloads.view.educational.udemy import get_all_udemy_links, get_single_udemy


def set_sleep(seconds):
    # return None
    time.sleep(seconds)


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        for page_number in range(1, 150):
            for url_slug in get_all_udemy_links(page_number=page_number):
                single_udemy = get_single_udemy(url_slug)
                try:
                    print(single_udemy)
                    Educational.objects.create(**single_udemy)
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
                    print("\n URL UDEMY: %s" % single_udemy)
