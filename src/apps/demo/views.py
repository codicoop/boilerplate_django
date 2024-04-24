import yaml
from django.shortcuts import redirect, render

from apps.demo.forms import DataForm, DataFormReadOnly
from apps.demo.models import Data


def data_view(request):
    if request.method == "GET":
        form = DataForm()
    else:
        form = DataForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
    return render(request, "home.html", {"form": form})


def list_view(request):
    context = {"data": Data.objects.all()}
    return render(request, "list_view.html", context)


def detail_view(request, id):
    obj = Data.objects.get(id=id)
    obj.field_select_checkbox = yaml.safe_load(obj.field_select_checkbox)
    obj.save()
    form = DataFormReadOnly(instance=obj)
    return render(request, "details.html", {"form": form})


def update_view(request, id):
    obj = Data.objects.get(id=id)
    if request.method == "GET":
        obj.field_select_checkbox = yaml.safe_load(obj.field_select_checkbox)
        obj.save()
        form = DataForm(instance=obj)
    else:
        form = DataForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
    return render(request, "details.html", {"form": form})
