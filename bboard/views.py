from typing import Dict
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.shortcuts import render, get_object_or_404

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


class AdCreateView(CreateView):
    model = Item
    fields = [
        "name",
        "length",
        "description",
        "price",
        "rubric",
        "image"
    ]


class AdUpdateView(UpdateView):
    model = Item
    fields = [
        "name",
        "length",
        "description",
        "price",
        "rubric",
        "image"
    ]


class AdDeleteView(DeleteView):
    model = Item
    success_url = '/'


def about_page(request):
    return render(request, "bboard/about_us.html")
