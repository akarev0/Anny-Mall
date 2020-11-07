from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)

from .models import Item, Rubric


class AdListView(ListView):
    model = Item
    template_name = "bboard/home_page.html"
    context_object_name = "ads"
    ordering = ["-published"]
    paginate_by = 3


class ByRubricListView(ListView):
    model = Item
    template_name = "bboard/rubric.html"
    context_object_name = "ads"
    ordering = ["-published"]
    paginate_by = 3

    def get_queryset(self):
        ads = get_object_or_404(Rubric, name=self.kwargs.get("rubric"))
        return Item.objects.filter(rubric=ads).order_by("-published")


class AdDetailView(DetailView):
    model = Item


class AdCreateView(LoginRequiredMixin, CreateView):
    model = Item
    fields = [
        "name",
        "length",
        "description",
        "price",
        "rubric",
        "image"
    ]


class AdUpdateView(LoginRequiredMixin, UpdateView):
    model = Item
    fields = [
        "name",
        "length",
        "description",
        "price",
        "rubric",
        "image"
    ]


class AdDeleteView(LoginRequiredMixin, DeleteView):
    model = Item
    success_url = '/'


def about_page(request):
    return render(request, "bboard/about_us.html")
