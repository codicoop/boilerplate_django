from django.shortcuts import render, redirect

from apps.demo.forms import DataForm
from apps.demo.models import Data


def data_view(request):
    if request.method == 'GET':
        form = DataForm()
    else:
        form = DataForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, "home.html", {'form': form})


def list_view(request):
    context = {}
    context["data"] = Data.objects.all()
    return render(request, "list_view.html", context)


def detail_view(request, id):
    context = {}
    context["data"] = Data.objects.get(id=id)
    return render(request, "detail_view.html", context)


def update_view(request, id):
    if request.method == 'GET':
        context = {}
        context["data"] = Data.objects.get(id=id)
        return render(request, "update_view.html", context)
    else:
        form = DataForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        return render(request, "home.html", {'form': form})
