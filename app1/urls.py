from django.urls import path
from app1.views import (
    DoctorsListView, DoctorsDetailView,
    DoctorsTimingListView, DoctorsTimingDetailView,
    MiselListView, MiselDetailView,
)

urlpatterns = [
    # hms_doctors
    path('doctors/',             DoctorsListView.as_view(),        name='doctors-list'),
    path('doctors/<str:code>/',  DoctorsDetailView.as_view(),      name='doctors-detail'),

    # hms_doctorstiming
    path('doctorstiming/',              DoctorsTimingListView.as_view(),   name='doctorstiming-list'),
    path('doctorstiming/<str:slno>/',   DoctorsTimingDetailView.as_view(), name='doctorstiming-detail'),

    # misel
    path('misel/',                          MiselListView.as_view(),   name='misel-list'),
    path('misel/<str:misel_primary>/',      MiselDetailView.as_view(), name='misel-detail'),
]