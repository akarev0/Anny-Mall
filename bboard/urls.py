from django.urls import path

from .views import (
	about_page, 
	AdListView, 
	AdDetailView, 
	AdCreateView,
	AdUpdateView,
	AdDeleteView,
	ByRubricListView
)

urlpatterns = [
    path("", AdListView.as_view(), name="home-page"),
    path("ad/<str:rubric>", ByRubricListView.as_view(), name="rubric-ads"),
    path("about/", about_page, name="about-page"),
    path("ad/<int:pk>/", AdDetailView.as_view(), name="ad-detail"),
    path("ad/<int:pk>/update/", AdUpdateView.as_view(), name="ad-update"),
    path("ad/<int:pk>/delete/", AdDeleteView.as_view(), name="ad-delete"),
    path("ad/new/", AdCreateView.as_view(), name="ad-create")

]
