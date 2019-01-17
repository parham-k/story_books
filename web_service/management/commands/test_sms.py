from django.core.management import BaseCommand

from web_service import sms_api


class Command(BaseCommand):

    def handle(self, *args, **options):
        print(sms_api.send_sms('09134231834', 'تست پیامک مفتاح'))
