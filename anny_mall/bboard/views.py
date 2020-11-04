from typing import Dict
from django.views.generic import (
	ListView, 
	DetailView, 
	CreateView,
	UpdateView,
	DeleteView
)
from django.shortcuts import render

from .models import Item


def home_page(request):
    ads: Item = Item.objects.all()
    context: Dict = {
        "ads": ads
    }
    return render(request=request, template_name="bboard/home_page.html", context=context)


class AdListView(ListView):
	model = Item
	template_name = "bboard/home_page.html"
	context_object_name = "ads"
	ordering = ["-published"]

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
