from django import forms


class MemoryForm(forms.Form):
    latitude = forms.FloatField(widget=forms.HiddenInput())
    longitude = forms.FloatField(widget=forms.HiddenInput())
    place_id = forms.IntegerField(required=False, widget=forms.HiddenInput())
    place_name = forms.CharField(required=False, widget=forms.HiddenInput())
    zoom = forms.IntegerField(widget=forms.HiddenInput())
    title = forms.CharField()
    text = forms.CharField(widget=forms.Textarea)
