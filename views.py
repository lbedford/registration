from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views import generic

from registration.models import Lbw

class IndexView(generic.ListView):
    template_name = 'registration/index.html'
    context_object_name = 'lbws'

    def get_queryset(self):
        """Return the last five published polls."""
        return Lbw.objects.order_by('-start_date')

class DetailView(generic.DetailView):
    model = Lbw
    template_name = 'registration/detail.html'

def register(request, lbw_id):
    return HttpResponse("You're registering on lbw %s." % lbw_id)
