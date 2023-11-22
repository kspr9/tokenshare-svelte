from django.urls import path

from . import views

app_name="mail"

urlpatterns = [
    path("", views.inbox, name="inbox"),
    #path("login", views.login_view, name="login"),
    #path("logout", views.logout_view, name="logout"),
    #path("register/", views.register, name="register"),

    # API Routes
    path("send_msg", views.compose, name="compose"),
    path("messages/<int:msg_id>", views.message, name="message"),
    path("messages/<str:mailbox>", views.mailbox, name="mailbox"),
]