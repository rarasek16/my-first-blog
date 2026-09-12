from django.contrib.auth import get_user_model
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
