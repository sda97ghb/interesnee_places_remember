from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse


class Memory(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    text = models.TextField(max_length=1000)

    class Meta:
        verbose_name_plural = "memories"
        indexes = [
            models.Index(fields=("user_id",))
        ]

    def __str__(self):
        if self.user.first_name or self.user.last_name:
            username = f"{self.user.first_name} {self.user.last_name}"
        else:
            username = self.user.username
        return f"{username}'s memory about {self.place}: {self.title}"

    def get_absolute_url(self):
        return reverse("places_remember:update_memory", kwargs={"pk": self.pk})


class Place(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    zoom = models.IntegerField()
    place_id = models.IntegerField(null=True, blank=True)
    place_name = models.CharField(max_length=100, blank=True)
    memory = models.OneToOneField(Memory, on_delete=models.CASCADE)

    def __str__(self):
        place_name = self.place_name if self.place_name else "Unknown place"
        return f"{place_name} at {self.latitude},{self.longitude}"
