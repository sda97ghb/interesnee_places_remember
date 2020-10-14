from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase, Client, override_settings, RequestFactory
from django.urls import reverse

from places_remember import forms, models


class IndexViewTests(TestCase):
    def test_index_is_available(self):
        c = Client()
        self.assertEqual(c.get("").status_code, 200)
        self.assertEqual(c.get("/").status_code, 200)


class CreateMemoryViewTests(TestCase):
    def setUp(self) -> None:
        User = get_user_model()
        user = User.objects.create_user("test", "test@gmail.com", "test")

    def test_available_for_logged_in(self):
        c = Client()
        c.login(username="test", password="test")
        response = c.get(reverse("places_remember:create_memory"))
        self.assertEqual(response.status_code, 200)

    def test_redirects_not_logged_in_to_login(self):
        c = Client()
        path = reverse("places_remember:create_memory")
        expected_redirect = reverse("account_login") + "?next=" + path
        self.assertRedirects(c.get(path), expected_redirect)


class UpdateMemoryViewTests(TestCase):
    def setUp(self) -> None:
        User = get_user_model()
        user = User.objects.create_user("test", "test@gmail.com", "test")

    def test_available_for_logged_in(self):
        c = Client()
        c.login(username="test", password="test")
        path = reverse("places_remember:update_memory", kwargs={"pk": 1})
        response = c.get(path)
        self.assertEqual(response.status_code, 200)

    def test_redirects_not_logged_in_to_login(self):
        c = Client()
        path = reverse("places_remember:update_memory", kwargs={"pk": 1})
        expected_redirect = reverse("account_login") + "?next=" + path
        self.assertRedirects(c.get(path), expected_redirect)


class LoginTests(TestCase):
    def setUp(self) -> None:
        User = get_user_model()
        user = User.objects.create_user("test", "test@gmail.com", "test")

    def test_login_is_available_for_not_logged_in(self):
        c = Client()
        self.assertEqual(c.get(reverse("account_login")).status_code, 200)

    def test_login_is_not_available_for_logged_in(self):
        c = Client()
        c.login(username="test", password="test")
        self.assertRedirects(c.get(reverse("account_login")), reverse("places_remember:index"))

    def test_logout_is_available_for_logged_in(self):
        c = Client()
        c.login(username="test", password="test")
        self.assertEqual(c.get(reverse("account_logout")).status_code, 200)

    def test_logout_is_not_available_for_not_logged_in(self):
        c = Client()
        self.assertRedirects(c.get(reverse("account_logout")), reverse("places_remember:index"))

    def test_facebook_is_available(self):
        c = Client()
        response = c.get(reverse("facebook_login"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("https://www.facebook.com", response.url)
        self.assertIn("oauth", response.url)


class MemoryFormTests(TestCase):
    def test_has_fields(self):
        form = forms.MemoryForm()
        self.assertIn("latitude", form.fields)
        self.assertIn("longitude", form.fields)
        self.assertIn("zoom", form.fields)
        self.assertIn("place_id", form.fields)
        self.assertIn("place_name", form.fields)
        self.assertIn("title", form.fields)
        self.assertIn("text", form.fields)

    def test_good_case(self):
        data = {
            "latitude": 56.83800773134774,
            "longitude": 60.60362527445821,
            "zoom": 16,
            "place_id": None,
            "place_name": "",
            "title": "Awesome place",
            "text": "This place is really awesome!"
        }
        form = forms.MemoryForm(data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, data)

    def test_latitude_limits(self):
        data = {
            "longitude": 60.60362527445821,
            "zoom": 16,
            "place_id": None,
            "place_name": "",
            "title": "Awesome place",
            "text": "This place is really awesome!"
        }
        self.assertFalse(forms.MemoryForm({"latitude": -91, **data}).is_valid())
        self.assertTrue(forms.MemoryForm({"latitude": -90, **data}).is_valid())
        self.assertTrue(forms.MemoryForm({"latitude": 0, **data}).is_valid())
        self.assertTrue(forms.MemoryForm({"latitude": 90, **data}).is_valid())
        self.assertFalse(forms.MemoryForm({"latitude": 91, **data}).is_valid())

    def test_longitude_limits(self):
        data = {
            "latitude": 56.83800773134774,
            "zoom": 16,
            "place_id": None,
            "place_name": "",
            "title": "Awesome place",
            "text": "This place is really awesome!"
        }
        self.assertFalse(forms.MemoryForm({"longitude": -181, **data}).is_valid())
        self.assertTrue(forms.MemoryForm({"longitude": -180, **data}).is_valid())
        self.assertTrue(forms.MemoryForm({"longitude": 0, **data}).is_valid())
        self.assertTrue(forms.MemoryForm({"longitude": 180, **data}).is_valid())
        self.assertFalse(forms.MemoryForm({"longitude": 181, **data}).is_valid())

    def test_zoom_limits(self):
        data = {
            "latitude": 56.83800773134774,
            "longitude": 60.60362527445821,
            "place_id": None,
            "place_name": "",
            "title": "Awesome place",
            "text": "This place is really awesome!"
        }
        self.assertFalse(forms.MemoryForm({"zoom": -1, **data}).is_valid())
        self.assertTrue(forms.MemoryForm({"zoom": 0, **data}).is_valid())
        self.assertTrue(forms.MemoryForm({"zoom": 16, **data}).is_valid())
        self.assertTrue(forms.MemoryForm({"zoom": 21, **data}).is_valid())
        self.assertFalse(forms.MemoryForm({"zoom": 22, **data}).is_valid())

    def test_place_name_limits(self):
        data = {
            "latitude": 56.83800773134774,
            "longitude": 60.60362527445821,
            "zoom": 16,
            "place_id": None,
            "title": "Awesome place",
            "text": "This place is really awesome!"
        }
        self.assertTrue(forms.MemoryForm({"place_name": "", **data}).is_valid())
        self.assertTrue(forms.MemoryForm({"place_name": "Test, test, test", **data}).is_valid())
        self.assertTrue(forms.MemoryForm({"place_name": "t" * 100, **data}).is_valid())
        self.assertFalse(forms.MemoryForm({"place_name": "t" * 101, **data}).is_valid())

    def test_title_limits(self):
        data = {
            "latitude": 56.83800773134774,
            "longitude": 60.60362527445821,
            "zoom": 16,
            "place_id": None,
            "place_name": "",
            "text": "This place is really awesome!"
        }
        self.assertFalse(forms.MemoryForm({"title": "", **data}).is_valid())
        self.assertTrue(forms.MemoryForm({"title": "Test, test, test", **data}).is_valid())
        self.assertTrue(forms.MemoryForm({"title": "t" * 100, **data}).is_valid())
        self.assertFalse(forms.MemoryForm({"title": "t" * 101, **data}).is_valid())

    def test_text_limits(self):
        data = {
            "latitude": 56.83800773134774,
            "longitude": 60.60362527445821,
            "zoom": 16,
            "place_id": None,
            "place_name": "",
            "title": "Awesome place"
        }
        self.assertFalse(forms.MemoryForm({"text": "", **data}).is_valid())
        self.assertTrue(forms.MemoryForm({"text": "Test, test, test", **data}).is_valid())
        self.assertTrue(forms.MemoryForm({"text": "t" * 1000, **data}).is_valid())
        self.assertFalse(forms.MemoryForm({"text": "t" * 1001, **data}).is_valid())


class YandexMapsContextProcessorTests(TestCase):
    @override_settings()
    def test_requires_api_key(self):
        if hasattr(settings, "YANDEX_MAPS_API_KEY"):
            del settings.YANDEX_MAPS_API_KEY
        from places_remember.context_processors import yandex_maps
        self.assertRaises(Exception, yandex_maps, RequestFactory().get("/"))

    @override_settings(YANDEX_MAPS_API_KEY="actual-value-does-not-matter-here")
    def test_produced_context_has_values(self):
        from places_remember.context_processors import yandex_maps
        context = yandex_maps(RequestFactory().get("/"))
        self.assertIn("yandex_maps", context)
        self.assertIn("api_key", context["yandex_maps"])
        self.assertIn("api_script", context["yandex_maps"])
        self.assertIn("api_script_url", context["yandex_maps"])

    @override_settings(
        YANDEX_MAPS_API_KEY="actual-value-does-not-matter-here",
        YANDEX_MAPS_API_VERSION="1.2.3.4.5.6.7.8.9"
    )
    def test_use_api_version_setting(self):
        from places_remember.context_processors import yandex_maps
        context = yandex_maps(RequestFactory().get("/"))
        self.assertIn("1.2.3.4.5.6.7.8.9", context["yandex_maps"]["api_script_url"])


class PlaceModelTests(TestCase):
    def test_string_representation(self):
        place = models.Place(
            latitude=56.83800773134774, longitude=60.60362527445821,
            zoom=16,
            place_id=None, place_name=""
        )
        self.assertEqual(str(place), "Unknown place at 56.83800773134774,60.60362527445821")

    def test_verbose_name_plural(self):
        self.assertEqual(str(models.Place._meta.verbose_name_plural), "places")

    def test_ymap_url(self):
        place = models.Place(
            latitude=56.83800773134774, longitude=60.60362527445821,
            zoom=16,
            place_id=None, place_name=""
        )
        self.assertTrue(hasattr(place, "ymap_url"))
        self.assertIsNotNone(place.ymap_url)


class MemoryModelTests(TestCase):
    def setUp(self) -> None:
        self.User = get_user_model()
        self.user = self.User.objects.create_user(
            username="john", email="test@gmail.com", password="test",
            first_name="John", last_name="Doe"
        )

    def test_string_representation(self):
        memory = models.Memory.objects.create(
            user=self.user,
            title="Test memory",
            text="Test, test, test.",
        )
        place = models.Place.objects.create(
            latitude=56.83800773134774, longitude=60.60362527445821,
            zoom=16,
            place_id=None, place_name="",
            memory=memory
        )
        self.assertEqual(str(memory),
                         "John Doe's memory about Unknown place at 56.83800773134774,60.60362527445821: Test memory")

    def test_string_representation_no_first_and_last_names(self):
        user = self.User.objects.create_user(
            username="jane", email="test@gmail.com", password="test"
        )
        memory = models.Memory.objects.create(
            user=user,
            title="Test memory",
            text="Test, test, test.",
        )
        place = models.Place.objects.create(
            latitude=56.83800773134774, longitude=60.60362527445821,
            zoom=16,
            place_id=None, place_name="",
            memory=memory
        )
        self.assertEqual(str(memory),
                         "jane's memory about Unknown place at 56.83800773134774,60.60362527445821: Test memory")

    def test_verbose_name_plural(self):
        self.assertEqual(str(models.Memory._meta.verbose_name_plural), "memories")

    def test_get_absolute_url(self):
        c = Client()
        c.force_login(self.user)
        memory = models.Memory.objects.create(
            user=self.user,
            title="Test memory",
            text="Test, test, test.",
        )
        place = models.Place.objects.create(
            latitude=56.83800773134774, longitude=60.60362527445821,
            zoom=16,
            place_id=None, place_name="",
            memory=memory
        )
        response = c.get(memory.get_absolute_url())
        memory.delete()
        self.assertEqual(response.status_code, 200)
