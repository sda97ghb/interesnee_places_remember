from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


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
