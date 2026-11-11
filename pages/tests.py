
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.test import TestCase
from django.urls import reverse
from django.db.models.deletion import ProtectedError

from .models import Category, Resource


User = get_user_model()


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


class AuthenticationAndPermissionsTests(TestCase):

    def setUp(self):
        self.category = Category.objects.create(
            name="Categoría de autenticación"
        )

        self.resource = Resource.objects.create(
            title="Recurso de autenticación",
            description="Recurso para probar permisos",
            resource_type="Documento",
            available=True,
            category=self.category
        )

        self.password = "PruebaSegura123!"

        self.user = User.objects.create_user(
            username="usuario_prueba",
            password=self.password
        )

        self.view_permission = Permission.objects.get(
            codename="view_resource",
            content_type__app_label="pages"
        )

    # PRUEBAS DE REGISTRO

    def test_signup_page_responds_and_uses_template(self):
        response = self.client.get(reverse("pages:signup"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/signup.html")

    def test_signup_creates_normal_user_and_redirects_to_login(self):
        response = self.client.post(
            reverse("pages:signup"),
            {
                "username": "nuevo_usuario",
                "password1": self.password,
                "password2": self.password,
            }
        )

        new_user = User.objects.get(username="nuevo_usuario")

        self.assertRedirects(
            response,
            reverse("pages:login")
        )
        self.assertFalse(new_user.is_staff)
        self.assertFalse(new_user.is_superuser)
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_signup_with_invalid_data_does_not_create_user(self):
        response = self.client.post(
            reverse("pages:signup"),
            {
                "username": "usuario_invalido",
                "password1": "123",
                "password2": "456",
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            User.objects.filter(username="usuario_invalido").exists()
        )

    def test_authenticated_user_is_redirected_from_signup(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse("pages:signup"))

        self.assertRedirects(
            response,
            reverse("pages:dashboard")
        )

    # PRUEBAS DE INICIO Y CIERRE DE SESIÓN

    def test_login_page_responds_and_uses_template(self):
        response = self.client.get(reverse("pages:login"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/login.html")

    def test_login_with_valid_credentials_redirects_to_dashboard(self):
        response = self.client.post(
            reverse("pages:login"),
            {
                "username": "usuario_prueba",
                "password": self.password,
            }
        )

        self.assertRedirects(
            response,
            reverse("pages:dashboard")
        )
        self.assertIn("_auth_user_id", self.client.session)

    def test_login_with_invalid_credentials_does_not_start_session(self):
        response = self.client.post(
            reverse("pages:login"),
            {
                "username": "usuario_prueba",
                "password": "clave_incorrecta",
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_logout_post_closes_session_and_redirects_home(self):
        self.client.force_login(self.user)

        response = self.client.post(reverse("pages:logout"))

        self.assertRedirects(
            response,
            reverse("pages:home")
        )
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_logout_get_is_not_allowed(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse("pages:logout"))

        self.assertEqual(response.status_code, 405)

    # PRUEBAS DEL PANEL Y LAS SESIONES

    def test_dashboard_redirects_anonymous_user_to_login(self):
        response = self.client.get(reverse("pages:dashboard"))

        self.assertRedirects(
            response,
            f"{reverse('pages:login')}?next={reverse('pages:dashboard')}"
        )

    def test_dashboard_is_available_for_authenticated_user(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse("pages:dashboard"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/dashboard.html")

    def test_dashboard_session_counter_increases(self):
        self.client.force_login(self.user)

        first_response = self.client.get(reverse("pages:dashboard"))
        second_response = self.client.get(reverse("pages:dashboard"))

        self.assertEqual(first_response.context["visits"], 1)
        self.assertEqual(second_response.context["visits"], 2)

    # PRUEBAS DE GRUPOS Y PERMISOS

    def test_resource_review_redirects_anonymous_user_to_login(self):
        response = self.client.get(
            reverse("pages:resource-review")
        )

        self.assertRedirects(
            response,
            f"{reverse('pages:login')}?next={reverse('pages:resource-review')}"
        )

    def test_normal_user_cannot_access_resource_review(self):
        self.client.force_login(self.user)

        response = self.client.get(
            reverse("pages:resource-review")
        )

        self.assertEqual(response.status_code, 403)

    def test_group_reviewer_can_access_resource_review(self):
        reviewers, created = Group.objects.get_or_create(
            name="Catalog reviewers"
        )

        reviewers.permissions.add(self.view_permission)
        self.user.groups.add(reviewers)

        self.client.force_login(self.user)

        response = self.client.get(
            reverse("pages:resource-review")
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/review.html")
        self.assertContains(response, "Recurso de autenticación")

    def test_user_with_direct_permission_can_access_review(self):
        self.user.user_permissions.add(self.view_permission)

        self.client.force_login(self.user)

        response = self.client.get(
            reverse("pages:resource-review")
        )

        self.assertEqual(response.status_code, 200)

    # PRUEBAS DE ACCESO PÚBLICO AL CATÁLOGO

    def test_resources_page_remains_public(self):
        response = self.client.get(reverse("pages:resources"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Recurso de autenticación")

    def test_available_resources_page_remains_public(self):
        response = self.client.get(
            reverse("pages:available_resources")
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Recurso de autenticación")
