from django.urls import path

from .views import home_page, about_page, AdListView

urlpatterns = [
    # path("", home_page, name="home-page"),
    path("", AdListView.as_view(), name="home-page"),
    path("about/", about_page, name="about-page"),
]
