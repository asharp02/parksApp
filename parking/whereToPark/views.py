import json

from django.shortcuts import render
from django.db.models import Q
from whereToPark.models import ByLaw as np
from whereToPark.models import ByLaw as rp


# Create your views here.
def index(request):
    np_bylaws = np.objects.exclude(
        Q(boundary_a_lat=None)
        | Q(boundary_b_lat=None)
        | Q(boundary_a_lng=None)
        | Q(boundary_b_lng=None)
    ).exclude(bylaw_no__icontains="repealed")
    rp_bylaws = rp.objects.exclude(
        Q(boundary_a_lat=None)
        | Q(boundary_b_lat=None)
        | Q(boundary_a_lng=None)
        | Q(boundary_b_lng=None)
    ).exclude(bylaw_no__icontains="repealed")
    # bylaws = list(np_bylaws.values()) + list(rp_bylaws.values())
    context = {
        "rp_bylaws": list(rp_bylaws.values()),
        "np_bylaws": list(np_bylaws.values()),
    }
    return render(request, "whereToPark/index.html", context)
