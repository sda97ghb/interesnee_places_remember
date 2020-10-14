from django import forms
from django.core.exceptions import ValidationError


class MemoryForm(forms.Form):
    latitude = forms.FloatField(widget=forms.HiddenInput())
    longitude = forms.FloatField(widget=forms.HiddenInput())
    zoom = forms.IntegerField(widget=forms.HiddenInput())
    place_id = forms.IntegerField(required=False, widget=forms.HiddenInput())
    place_name = forms.CharField(max_length=100, required=False, widget=forms.HiddenInput())
    title = forms.CharField(max_length=100)
    text = forms.CharField(widget=forms.Textarea, max_length=1000)

    def clean_latitude(self):
        latitude = self.cleaned_data["latitude"]
        if -90 <= latitude <= 90:
            return latitude
        else:
            raise ValidationError("Latitude must be in a range from -90 to 90", code="invalid")

    def clean_longitude(self):
        longitude = self.cleaned_data["longitude"]
        if -180 <= longitude <= 180:
            return longitude
        else:
            raise ValidationError("Longitude must be in a range from -180 to 180", code="invalid")

    def clean_zoom(self):
        zoom = self.cleaned_data["zoom"]
        if 0 <= zoom <= 21:
            return zoom
        else:
            raise ValidationError("Zoom must be in a range from 0 (entire world) to 21")
