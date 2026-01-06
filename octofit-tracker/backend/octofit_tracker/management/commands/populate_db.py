from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Workout, Leaderboard
from django.db import connection

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):

        self.stdout.write(self.style.WARNING('Dropping old collections...'))
        from django.conf import settings
        import pymongo
        client = pymongo.MongoClient(settings.DATABASES['default']['CLIENT']['host'], settings.DATABASES['default']['CLIENT']['port'])
        db = client[settings.DATABASES['default']['NAME']]
        for col in ['leaderboard', 'activities', 'workouts', 'users', 'teams']:
            db[col].drop()

        self.stdout.write(self.style.SUCCESS('Creating teams...'))
        marvel = Team.objects.create(name='Marvel')
        dc = Team.objects.create(name='DC')

        self.stdout.write(self.style.SUCCESS('Creating users...'))
        users = []
        users.append(User.objects.create(name='Spider-Man', email='spiderman@marvel.com', team=marvel))
        users.append(User.objects.create(name='Iron Man', email='ironman@marvel.com', team=marvel))
        users.append(User.objects.create(name='Wonder Woman', email='wonderwoman@dc.com', team=dc))
        users.append(User.objects.create(name='Batman', email='batman@dc.com', team=dc))

        self.stdout.write(self.style.SUCCESS('Creating activities...'))
        Activity.objects.create(user=users[0], type='Web Swing', duration=30, date='2024-01-01')
        Activity.objects.create(user=users[1], type='Flight', duration=45, date='2024-01-02')
        Activity.objects.create(user=users[2], type='Lasso Practice', duration=25, date='2024-01-03')
        Activity.objects.create(user=users[3], type='Martial Arts', duration=40, date='2024-01-04')

        self.stdout.write(self.style.SUCCESS('Creating workouts...'))
        w1 = Workout.objects.create(name='Hero Endurance', description='Endurance training for heroes')
        w2 = Workout.objects.create(name='Strength Circuit', description='Strength training for all')
        w1.suggested_for.set([u.id for u in users])
        w2.suggested_for.set([u.id for u in users])

        self.stdout.write(self.style.SUCCESS('Creating leaderboard...'))
        Leaderboard.objects.create(user=users[0], score=100)
        Leaderboard.objects.create(user=users[1], score=90)
        Leaderboard.objects.create(user=users[2], score=95)
        Leaderboard.objects.create(user=users[3], score=85)

        self.stdout.write(self.style.SUCCESS('Ensuring unique index on email...'))
        # Use pymongo directly for index creation
        from django.conf import settings
        import pymongo
        client = pymongo.MongoClient(settings.DATABASES['default']['CLIENT']['host'], settings.DATABASES['default']['CLIENT']['port'])
        db = client[settings.DATABASES['default']['NAME']]
        db.users.create_index([('email', 1)], unique=True)

        self.stdout.write(self.style.SUCCESS('Database populated with test data!'))
