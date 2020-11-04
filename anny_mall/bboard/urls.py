from django.urls import path

from .views import (
	about_page, 
	AdListView, 
	AdDetailView, 
	AdCreateView,
	AdUpdateView,
	AdDeleteView
)

urlpatterns = [
    path("", AdListView.as_view(), name="home-page"),
    path("about/", about_page, name="about-page"),
    path("ad/<int:pk>/", AdDetailView.as_view(), name="ad-detail"),
    path("ad/<int:pk>/update/", AdUpdateView.as_view(), name="ad-update"),
    path("ad/<int:pk>/delete/", AdDeleteView.as_view(), name="ad-delete"),
    path("ad/new/", AdCreateView.as_view(), name="ad-create")

]
