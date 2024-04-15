from django.core.management.base import BaseCommand
from movierecommendation.views import weibobuildindex, weiboSearchIndex
from django.http import HttpRequest


class Command(BaseCommand):
    help = 'Builds the weibo index'

    def handle(self, *args, **options):
        # Create a fake POST request
        request = HttpRequest()
        request.method = 'GET'
        request.GET['id'] = 'weibosubmit2search'
        request.GET['keyword'] = "我们是好朋友"
        # Call the function
        response = weiboSearchIndex(request)

        # Print the response content
        self.stdout.write(response.content.decode())