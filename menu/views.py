from django.http import Http404
from django.shortcuts import render
from django.views.generic import TemplateView

from menu.models import MenuItem


class Page(TemplateView):
    template_name = 'page/index.html'


def my_view(request, url_type):
    """
    Вьюха-заглушка для демонстрации меню.
    """
    try:
        obj = MenuItem.objects.get(named_url=url_type)
    except MenuItem.DoesNotExist:
        try:
            obj = MenuItem.objects.get(url=url_type)
        except MenuItem.MultipleObjectsReturned:
            raise Http404()
        except MenuItem.DoesNotExist:
            raise Http404("Объект не найден.")
    return render(request, 'page/index.html', {'obj': obj})
