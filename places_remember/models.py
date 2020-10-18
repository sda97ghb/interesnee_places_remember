from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _, gettext


class Memory(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name=_("user"))
    title = models.CharField(max_length=100, verbose_name=_("title"))
    text = models.TextField(max_length=1000, verbose_name=_("text"))

    class Meta:
        verbose_name = _("memory")
        verbose_name_plural = _("memories")
        indexes = [
            models.Index(fields=("user_id",))
        ]

    def __str__(self):
        if self.user.first_name or self.user.last_name:
            username = f"{self.user.first_name} {self.user.last_name}"
        else:
            username = self.user.username
        # return f"{username}'s memory about {self.place}: {self.title}"
        return gettext("%(username)s's memory about %(place)s: %(title)s") % {
            "username": username,
            "place": self.place,
            "title": self.title
        }

    def get_absolute_url(self):
        return reverse("places_remember:update_memory", kwargs={"pk": self.pk})


class Place(models.Model):
    latitude = models.FloatField(verbose_name=_("latitude"))
    longitude = models.FloatField(verbose_name=_("longitude"))
    zoom = models.IntegerField(verbose_name=_("zoom"))
    place_id = models.IntegerField(null=True, blank=True, verbose_name=_("place id"))
    place_name = models.CharField(max_length=100, blank=True, verbose_name=_("place name"))
    memory = models.OneToOneField(Memory, on_delete=models.CASCADE, verbose_name=_("memory"))
    
    class Meta:
        verbose_name = _("place")
        verbose_name_plural = _("places")

    def __str__(self):
        place_name = self.place_name if self.place_name else gettext("Unknown place")
        return gettext("%(place_name)s at %(latitude)f,%(longitude)f") % {
            "place_name": place_name,
            "latitude": self.latitude,
            "longitude": self.longitude
        }

    @property
    def ymap_url(self):
        return f"https://static-maps.yandex.ru/1.x/?l=map&ll={self.longitude},{self.latitude}&size=600,400&z={self.zoom}&pt={self.longitude},{self.latitude},pm2dom"
