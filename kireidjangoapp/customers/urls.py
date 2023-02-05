from django.urls import path

from . import views

from django.contrib.auth import views as auth_views


urlpatterns = [
    path("register/", views.register, name = "register"),
    path('login/', views.login, name='login'),
    path("password_reset/", views.password_reset, name="password_reset"),
    path("password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="customers/password/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path("reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="customers/password/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path( "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="customers/password/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    # path("profile/", profile, name="users-profile"),
    # path("password-change/", ChangePasswordView.as_view(), name="password_change"),
]