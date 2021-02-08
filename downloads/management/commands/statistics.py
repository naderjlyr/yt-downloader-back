from django.core.management.base import BaseCommand

from downloads.models import Movie, Adult, Educational, Configs


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('type', type=str, help='which filtering statistics to be shown')
        parser.add_argument('-c', '--count', action='store_true', help='which filtering statistics to be shown')

    def handle(self, *args, **kwargs):
        stat_type = kwargs['type']
        is_count = kwargs['count']
        # configs
        if stat_type == 'config':
            configs = Configs.objects.all()
            if is_count:
                print("count of all searches: ", configs.count())
            else:
                print(configs.values('search_name', 'search_type'))

        else:
            # movies
            movies = Movie.objects.all()
            print("count of all movies: ", movies.count())

            # adults
            adults = Adult.objects.all()
            print("count of all adults: ", adults.count())

            # educational
            educations = Educational.objects.all()
            print("count of all educational: ", educations.count())
