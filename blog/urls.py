from django.urls import path

from . import views

urlpatterns = [
    path("", views.post_list, name="post_list"),
    path("pristupnost/", views.accessibility_statement, name="accessibility_statement"),
    path("accounts/register/", views.register, name="register"),
    path("bonus/", views.bonus_tasks, name="bonus_tasks"),
    path("category/<slug:category_slug>/", views.post_list, name="post_list_by_category"),
    path("post/new/", views.post_new, name="post_new"),
    path("post/<int:pk>/", views.post_detail, name="post_detail"),
    path("post/<int:pk>/edit/", views.post_edit, name="post_edit"),
]
