from pathlib import Path
from tempfile import TemporaryDirectory

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import override_settings
from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone

from .forms import PostForm
from .models import Category, Post


class PostModelTests(TestCase):
    def test_publish_sets_published_date(self):
        user = get_user_model().objects.create_user(username="author")
        post = Post.objects.create(author=user, title="Test", text="Body")

        post.publish()

        self.assertIsNotNone(post.published_date)


class PostFormTests(TestCase):
    def test_post_form_valid(self):
        category = Category.objects.create(name="Django", slug="django")
        form = PostForm(data={"title": "Form title", "text": "Form text", "category": category.id})

        self.assertTrue(form.is_valid())


class SeedDjangoLessonsCommandTests(TestCase):
    def test_command_creates_lessons_once(self):
        call_command("seed_django_lessons")
        call_command("seed_django_lessons")

        self.assertEqual(Category.objects.count(), 8)
        lessons = Post.objects.filter(author__username="django_start")
        self.assertEqual(lessons.count(), 11)
        self.assertTrue(lessons.filter(code_example__gt="").exists())

    def test_refresh_adds_materials_to_existing_sample_lessons(self):
        call_command("seed_django_lessons")
        Post.objects.filter(title="Django nebo Flask? Jak vybrat framework pro projekt").update(
            learning_goal=""
        )

        call_command("seed_django_lessons", refresh=True)

        lesson = Post.objects.get(title="Django nebo Flask? Jak vybrat framework pro projekt")
        self.assertNotEqual(lesson.learning_goal, "")


class PostViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.author = get_user_model().objects.create_user(username="author")
        self.other_user = get_user_model().objects.create_user(username="other")
        self.category = Category.objects.create(name="Python", slug="python")

    def test_post_list_shows_only_published_posts(self):
        published = Post.objects.create(
            author=self.author,
            title="Published",
            text="Visible",
            category=self.category,
            published_date=timezone.now(),
        )
        Post.objects.create(author=self.author, title="Draft", text="Hidden")

        response = self.client.get(reverse("post_list"))

        self.assertContains(response, published.title)
        self.assertNotContains(response, "Draft")
        self.assertContains(response, 'href="#main-content"')

    def test_post_list_filters_by_category(self):
        second_category = Category.objects.create(name="Web", slug="web")
        Post.objects.create(
            author=self.author,
            title="Python Post",
            text="Visible",
            category=self.category,
            published_date=timezone.now(),
        )
        Post.objects.create(
            author=self.author,
            title="Web Post",
            text="Visible",
            category=second_category,
            published_date=timezone.now(),
        )

        response = self.client.get(reverse("post_list_by_category", kwargs={"category_slug": "python"}))

        self.assertContains(response, "Python Post")
        self.assertNotContains(response, "Web Post")

    def test_post_detail_404_for_unpublished_post(self):
        draft = Post.objects.create(author=self.author, title="Draft", text="Hidden")

        response = self.client.get(reverse("post_detail", kwargs={"pk": draft.pk}))

        self.assertEqual(response.status_code, 404)

    def test_post_detail_includes_navigation_categories(self):
        post = Post.objects.create(
            author=self.author,
            title="Published",
            text="Visible",
            published_date=timezone.now(),
        )

        response = self.client.get(reverse("post_detail", kwargs={"pk": post.pk}))

        self.assertContains(response, self.category.name)

    def test_post_create_requires_login(self):
        response = self.client.get(reverse("post_new"))

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)

    def test_post_create_sets_author(self):
        self.client.force_login(self.author)

        response = self.client.post(
            reverse("post_new"),
            {"title": "New Post", "text": "New body", "category": self.category.id},
        )

        self.assertEqual(response.status_code, 302)
        post = Post.objects.get(title="New Post")
        self.assertEqual(post.author, self.author)
        self.assertIsNotNone(post.published_date)

    def test_post_form_has_programmatic_help_and_error_descriptions(self):
        self.client.force_login(self.author)

        response = self.client.get(reverse("post_new"))

        self.assertContains(response, 'for="id_title"')
        self.assertContains(response, 'aria-describedby="title-errors"')
        self.assertContains(response, "Přidat výukové materiály")

    def test_accessibility_statement_is_available(self):
        response = self.client.get(reverse("accessibility_statement"))

        self.assertContains(response, "Prohlášení o přístupnosti")
        self.assertContains(response, "WCAG 2.2")

    def test_registration_creates_and_logs_in_user(self):
        response = self.client.post(
            reverse("register"),
            {
                "username": "new_student",
                "password1": "Strong-passphrase-2026",
                "password2": "Strong-passphrase-2026",
            },
        )

        self.assertRedirects(response, reverse("post_list"))
        self.assertTrue(get_user_model().objects.filter(username="new_student").exists())

    def test_authenticated_user_is_not_shown_registration_form(self):
        self.client.force_login(self.author)

        response = self.client.get(reverse("register"))

        self.assertRedirects(response, reverse("post_list"))

    def test_bonus_tasks_require_login(self):
        response = self.client.get(reverse("bonus_tasks"))

        self.assertRedirects(response, f"{reverse('login')}?next={reverse('bonus_tasks')}")

    def test_bonus_tasks_are_available_to_authenticated_user(self):
        self.client.force_login(self.author)

        response = self.client.get(reverse("bonus_tasks"))

        self.assertContains(response, "Bonusová zóna")
        self.assertContains(response, "Katalog knih pro třídu")

    def test_post_edit_limited_to_author(self):
        post = Post.objects.create(
            author=self.author,
            title="Owned",
            text="Body",
            published_date=timezone.now(),
        )
        self.client.force_login(self.other_user)

        response = self.client.get(reverse("post_edit", kwargs={"pk": post.pk}))

        self.assertEqual(response.status_code, 404)


class DemoAccountsCommandTests(TestCase):
    def test_command_rejects_non_development_settings(self):
        with override_settings(DEBUG=False):
            with self.assertRaises(CommandError):
                call_command("create_demo_accounts")

    def test_demo_admin_has_administration_permissions(self):
        with TemporaryDirectory() as directory:
            base_dir = Path(directory)
            credentials_file = base_dir / "local" / "demo-accounts.txt"
            with override_settings(BASE_DIR=base_dir, DEBUG=True):
                call_command("create_demo_accounts", credentials_file=credentials_file)
            self.assertTrue(credentials_file.exists())
            self.assertIn("admin_demo |", credentials_file.read_text(encoding="utf-8"))

        admin = get_user_model().objects.get(username="admin_demo")
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)
