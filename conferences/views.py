from django.shortcuts import render
from .models import conference
from django.views.generic import ListView,DetailView


def conferenceList(req):
    liste=conference.objects.all().order_by('-start_date')
    return render(req,'conferences/conferenceList.html',{'conferences':liste})

class conferenceListView(ListView):
    model=conference
    template_name='conferences/conferenceList2.html'
    context_object_name='conferences'
    def get_queryset(self):
        return conference.objects.order_by('-start_date')
    
class DetailsViewConference(DetailView):
    model=conference
    template_name='conferences/conferenceDetails.html'
    context_object_name='conferences'