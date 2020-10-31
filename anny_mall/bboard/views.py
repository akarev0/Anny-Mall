from typing import Dict

from django.shortcuts import render

ads = [
    {
        "name": "Платье синее",
        "length": "128",
        "price": "90",
        "brand": None,
        "image": "picture_1"
    },
    {
        "name": "Свитшот новый",
        "length": "128",
        "price": "350",
        "brand": "",
        "image": "picture_2"
    }
]


def home_page(request):
    context: Dict = {
        "ads": ads
    }
    return render(request=request, template_name="bboard/home_page.html", context=context)


def about_page(request):
    return render(request, "bboard/about_us.html")
