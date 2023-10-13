import json

from django.shortcuts import render
from django.db.models import Q
from whereToPark.models import ByLaw


# Create your views here.
def index(request):
    np_bylaws = ByLaw.objects.get_np_bylaws_to_display()
    rp_bylaws = ByLaw.objects.get_rp_bylaws_to_display()
    context = {
        "rp_bylaws": rp_bylaws,
        "np_bylaws": np_bylaws,
    }
    return render(request, "whereToPark/index.html", context)
