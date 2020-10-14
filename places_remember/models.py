from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse


class Place(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    zoom = models.IntegerField()
    place_id = models.IntegerField(null=True, blank=True)
    place_name = models.CharField(max_length=100, blank=True)

    def __str__(self):
        place_name = self.place_name if self.place_name else "Unknown place"
        return f"{place_name} at {self.latitude},{self.longitude}"


class Memory(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    text = models.TextField(max_length=1000)
    place = models.OneToOneField(Place, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "memories"
        indexes = [
            models.Index(fields=("user_id",))
        ]

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}'s memory about {self.place}: {self.title}"

    def get_absolute_url(self):
        return reverse("places_remember:update_memory", kwargs={"pk": self.pk})
