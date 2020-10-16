import logging

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.db import transaction, IntegrityError
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import FormView

from places_remember import forms, models


class IndexView(View):
    def get(self, request):
        if request.user.is_authenticated:
            current_user_memories = models.Memory.objects.filter(user=self.request.user)
            context = {
                "memory_list": current_user_memories
            }
            return TemplateResponse(request, "places_remember/index_authenticated.html", context)
        else:
            return TemplateResponse(request, "places_remember/index_not_authenticated.html")


class AboutView(View):
    def get(self, request):
        return TemplateResponse(request, "places_remember/about.html")


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
    extra_context = {
        "title": "Add memory"
    }

    def form_valid(self, form):
        try:
            with transaction.atomic():
                memory = models.Memory.objects.create(
                    user=self.request.user,
                    title=form.cleaned_data["title"],
                    text=form.cleaned_data["text"]
                )
                place = models.Place.objects.create(
                    latitude=form.cleaned_data["latitude"],
                    longitude=form.cleaned_data["longitude"],
                    zoom=form.cleaned_data["zoom"],
                    place_id=form.cleaned_data["place_id"],
                    place_name=form.cleaned_data["place_name"],
                    memory=memory
                )
        except IntegrityError as error:
            log = logging.getLogger(__name__)
            log.exception(
                "Memory creation caused IntegrityError while being called with following form's cleaned data: %s",
                form.cleaned_data
            )
        else:
            return super().form_valid(form)


@method_decorator(login_required, name="dispatch")
class UpdateMemoryView(UserPassesTestMixin, FormView):
    template_name = "places_remember/memory_form.html"
    form_class = forms.MemoryForm
    success_url = reverse_lazy("places_remember:index")
    extra_context = {
        "title": "Edit memory"
    }

    def test_func(self):
        pk = self.kwargs["pk"]
        memory = get_object_or_404(models.Memory, pk=pk)
        return memory.user == self.request.user

    def get_initial(self):
        pk = self.kwargs["pk"]
        memory = get_object_or_404(models.Memory, pk=pk)
        place = memory.place
        initial = super().get_initial()
        initial.update({
            "latitude": place.latitude,
            "longitude": place.longitude,
            "zoom": place.zoom,
            "place_id": place.place_id,
            "place_name": place.place_name,
            "title": memory.title,
            "text": memory.text
        })
        return initial

    def form_valid(self, form):
        pk = self.kwargs["pk"]
        try:
            with transaction.atomic():
                memory = get_object_or_404(models.Memory, pk=pk)
                memory.title = form.cleaned_data["title"]
                memory.text = form.cleaned_data["text"]
                memory.save()
                memory.place.latitude = form.cleaned_data["latitude"]
                memory.place.longitude = form.cleaned_data["longitude"]
                memory.place.zoom = form.cleaned_data["zoom"]
                memory.place.place_id = form.cleaned_data["place_id"]
                memory.place.place_name = form.cleaned_data["place_name"]
                memory.place.save()
        except IntegrityError as error:
            log = logging.getLogger(__name__)
            log.exception(
                "Memory update caused IntegrityError while being called with following form's cleaned data: %s",
                form.cleaned_data
            )
        else:
            return super().form_valid(form)


# TODO: add delete memory view
