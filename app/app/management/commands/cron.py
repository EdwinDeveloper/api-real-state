from django.core.management.base import BaseCommand
from django_crontab import CronJobBase, Schedule

class MyCronJob(CronJobBase):
    RUN_EVERY_MINS = 5

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'app.management.commands.my_custom_command'    # a unique code

    def do(self):
        # Perform your cron job task here
        print('Running my cron job...')
