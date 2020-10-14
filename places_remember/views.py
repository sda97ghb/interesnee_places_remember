from django.contrib.auth.decorators import login_required
from django.template.response import TemplateResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import FormView

from places_remember import forms


class IndexView(View):
    def get(self, request):
        if request.user.is_authenticated:
            mt = request.GET.get("mt")
            if not mt:
                context = {
                    "memory_list": [
                        {
                            "place": {
                                "latitude": 56.83800773134774,
                                "longitude": 60.60362527445821,
                                "zoom": 16,
                                "id": None,
                                "name": None,
                                "ymap_url": "https://static-maps.yandex.ru/1.x/?l=map&ll=60.60362527445821,56.83800773134774&size=600,400&z=16"
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


@method_decorator(login_required, name="dispatch")
class CreateMemoryView(FormView):
    template_name = "places_remember/memory_form.html"
    form_class = forms.MemoryForm
    success_url = reverse_lazy("places_remember:index")
    initial = {
        "latitude": 56.83800773134774,
        "longitude": 60.60362527445821,
        "zoom": 16,
    }

    def form_valid(self, form):
        print(f"Create memory {form.cleaned_data}")
        return super().form_valid(form)


@method_decorator(login_required, name="dispatch")
class UpdateMemoryView(FormView):
    template_name = "places_remember/memory_form.html"
    form_class = forms.MemoryForm
    success_url = reverse_lazy("places_remember:index")
