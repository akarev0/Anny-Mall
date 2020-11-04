from typing import Dict
from django.views.generic import ListView
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



def about_page(request):
    return render(request, "bboard/about_us.html")

def create_new_ad(request) -> None:
	pass