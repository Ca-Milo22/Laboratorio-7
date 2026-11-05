from django.test import TestCase
from django.urls import reverse


class ClassroomHubPagesTests(TestCase):
    def test_home_page_responds_and_uses_template(self):
        response = self.client.get(reverse("pages:home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/home.html")
        self.assertContains(response, "ClassroomHub")

    def test_resources_page_has_example_resources(self):
        response = self.client.get(reverse("pages:resources"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/resources.html")
        self.assertEqual(len(response.context["resources"]), 3)
        self.assertContains(response, "Python desde cero")

    def test_about_page_is_available(self):
        response = self.client.get(reverse("pages:about"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/about.html")
        self.assertContains(response, "Sobre ClassroomHub")

    def test_unknown_page_returns_404(self):
        response = self.client.get("/unknown/")
        self.assertEqual(response.status_code, 404)
