from django.template.response import TemplateResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView

from places_remember import forms


class IndexView(View):
    def get(self, request):
        mode = request.GET.get("mode")
        if mode == "auth":
            request.user = {"is_authenticated": True}
            mt = request.GET.get("mt")
            if not mt:
                context = {
                    "memory_list": [
                        {
                            "place": {
                                "latitude": 56.1234,
                                "longitude": 56.1234,
                                "zoom": 16,
                                "id": None,
                                "name": None
                            },
                            "title": "Lorim ipsum dolor",
                            "text": "Lorem ipsum dolor sit amet."
                        }
                    ] * 3
                }
            else:
                context = {}
            return TemplateResponse(request, "places_remember/index_authorized.html", context)
        else:
            return TemplateResponse(request, "places_remember/index_unauthorized.html")


class CreateMemoryView(FormView):
    template_name = "places_remember/memory_form.html"
    form_class = forms.MemoryForm
    success_url = reverse_lazy("places_remember:index")


class UpdateMemoryView(FormView):
    template_name = "places_remember/memory_form.html"
    form_class = forms.MemoryForm
    success_url = reverse_lazy("places_remember:index")
