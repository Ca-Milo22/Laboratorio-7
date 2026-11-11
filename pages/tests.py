from django.test import TestCase
from django.urls import reverse
from django.db.models.deletion import ProtectedError

from .models import Category, Resource


class ClassroomHubPagesTests(TestCase):

    def setUp(self):
        # Creamos datos de ejemplo para las pruebas
        self.category = Category.objects.create(
            name="Pruebas",
            description="Categoría para pruebas"
        )

        self.resource = Resource.objects.create(
            title="Python desde cero",
            description="Introducción a la programación con Python",
            resource_type="Video",
            available=True,
            category=self.category
        )

    def test_home_page_responds_and_uses_template(self):
        response = self.client.get(reverse("pages:home"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/home.html")

    def test_home_page_displays_classroomhub(self):
        response = self.client.get(reverse("pages:home"))

        self.assertContains(response, "ClassroomHub")

    def test_resources_page_responds_and_uses_template(self):
        response = self.client.get(reverse("pages:resources"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/resources.html")

    def test_resources_page_displays_resource_title(self):
        response = self.client.get(reverse("pages:resources"))

        self.assertContains(response, "Python desde cero")

    def test_resources_page_displays_resource_type(self):
        response = self.client.get(reverse("pages:resources"))

        self.assertContains(response, "Video")

    def test_resources_page_displays_category(self):
        response = self.client.get(reverse("pages:resources"))

        self.assertContains(response, "Pruebas")

    def test_resources_page_displays_available_status(self):
        response = self.client.get(reverse("pages:resources"))

        self.assertContains(response, "Disponible")

    def test_available_resources_page_only_displays_available_resources(self):
        Resource.objects.create(
            title="Django no disponible",
            description="Recurso de prueba no disponible",
            resource_type="Documento",
            available=False,
            category=self.category
        )

        response = self.client.get(
            reverse("pages:available_resources")
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Python desde cero")
        self.assertNotContains(response, "Django no disponible")

    def test_about_page_is_available(self):
        response = self.client.get(reverse("pages:about"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/about.html")

    def test_unknown_page_returns_404(self):
        response = self.client.get("/unknown/")

        self.assertEqual(response.status_code, 404)

    def test_category_cannot_be_deleted_with_resources(self):
        with self.assertRaises(ProtectedError):
            self.category.delete()