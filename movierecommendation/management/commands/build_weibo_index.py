from django.core.management.base import BaseCommand
from movierecommendation.views import weibobuildindex
from django.http import HttpRequest


class Command(BaseCommand):
    help = 'Builds the weibo index'

    def handle(self, *args, **options):
        # Create a fake POST request
        request = HttpRequest()
        request.method = 'POST'
        request.POST['id'] = 'weibosubmit2index'

        # Call the weibobuildindex function
        response = weibobuildindex(request)

        # Print the response content
        self.stdout.write(response.content.decode())