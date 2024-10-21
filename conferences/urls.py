from django.urls import path
from .views import *

urlpatterns = [
    path('list/',conferenceList,name="listeconf"),
    path('conferenceListView/',conferenceListView.as_view(),name="listViewConf"),
    path('details/<int:pk>/',DetailsViewConference.as_view(),name="detailConf"),
]