from django.http import HttpResponse
from django.views import View


class IndexView(View):
    def get(self, request):
        return HttpResponse("WIP: Index page", content_type="text/plain")
