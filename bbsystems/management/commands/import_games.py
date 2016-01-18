import datetime
from cProfile import Profile

from django.core.management.base import BaseCommand, CommandError
from bbsystems.tasks import get_games_for_range, process_games


class Command(BaseCommand):
    help = 'Import games between two dates'

    def add_arguments(self, parser):
        parser.add_argument('start_date', type=str, help='YYYY-MM-DD')
        parser.add_argument('end_date', type=str, help='YYYY-MM-DD')
        parser.add_argument(
            '--parallel',
            action='store_true',
            help='Import games using celery for concurrency'
        )
        parser.add_argument(
            '--profile',
            action='store_true',
            help='When set, runs through profiler'
        )

    def _handle(self, *args, **options):
        start_date = datetime.date(
            int(options['start_date'][0:4]),
            int(options['start_date'][5:7]),
            int(options['start_date'][8:10]),
        )
        end_date = datetime.date(
            int(options['end_date'][0:4]),
            int(options['end_date'][5:7]),
            int(options['end_date'][8:10]),
        )
        parallel = True if options['parallel'] else False
        games = get_games_for_range(start_date, end_date)
        process_games(games, parallel)

    def handle(self, *args, **options):
        if options['profile']:
            profiler = Profile()
            profiler.runcall(self._handle, *args, **options)
            profiler.dump_stats('import_games.profile')
        else:
            self._handle(*args, **options)
