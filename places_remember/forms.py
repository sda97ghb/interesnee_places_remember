from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class MemoryForm(forms.Form):
    latitude = forms.FloatField(widget=forms.HiddenInput())
    longitude = forms.FloatField(widget=forms.HiddenInput())
    zoom = forms.FloatField(widget=forms.HiddenInput())
    place_id = forms.IntegerField(required=False, widget=forms.HiddenInput())
    place_name = forms.CharField(max_length=100, required=False, widget=forms.HiddenInput())
    title = forms.CharField(label=_("Title"), max_length=100)
    text = forms.CharField(label=_("Text"), widget=forms.Textarea, max_length=1000)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].widget.attrs["class"] = "form-control"
        self.fields["text"].widget.attrs["class"] = "form-control"
        label_suffix = kwargs.get("label_suffix", None)
        self.label_suffix = label_suffix if label_suffix is not None else ""

    def clean_latitude(self):
        latitude = self.cleaned_data["latitude"]
        if -90 <= latitude <= 90:
            return latitude
        else:
            raise ValidationError(_("Latitude must be in a range from -90 to 90"), code="invalid")

    def clean_longitude(self):
        longitude = self.cleaned_data["longitude"]
        if -180 <= longitude <= 180:
            return longitude
        else:
            raise ValidationError(_("Longitude must be in a range from -180 to 180"), code="invalid")

    def clean_zoom(self):
        zoom = self.cleaned_data["zoom"]
        if 0 <= zoom <= 21:
            # Usual Yandex maps can produce float zoom on devices with touchscreen.
            # Though api documentation defines it as integer and static maps does not support float zoom.
            return int(zoom)
        else:
            raise ValidationError(_("Zoom must be in a range from 0 (entire world) to 21"))
