import json

from django.shortcuts import render
from django.db.models import Q
from whereToPark.models import NoParkingByLaw as np


# Create your views here.
def index(request):
    bylaws = np.objects.exclude(
        Q(boundary_a_lat=None)
        | Q(boundary_b_lat=None)
        | Q(boundary_a_lng=None)
        | Q(boundary_b_lng=None)
    ).exclude(bylaw_no__icontains="repealed")
    context = {"bylaws": list(bylaws.values())}
    return render(request, "whereToPark/index.html", context)
