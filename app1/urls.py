from django.urls import path
from app1.views import (
    ClientRegisterView,
    DoctorsDetailView, DoctorsBulkView,
    DoctorsTimingDetailView, DoctorsTimingBulkView,
    MiselDetailView, MiselBulkView,
)

urlpatterns = [
    path('register/',                           ClientRegisterView.as_view(),      name='client-register'),

    path('doctors/bulk/',                       DoctorsBulkView.as_view(),         name='doctors-bulk'),
    path('doctors/<str:code>/',                 DoctorsDetailView.as_view(),       name='doctors-detail'),

    path('doctorstiming/bulk/',                 DoctorsTimingBulkView.as_view(),   name='doctorstiming-bulk'),
    path('doctorstiming/<str:slno>/',           DoctorsTimingDetailView.as_view(), name='doctorstiming-detail'),

    path('misel/bulk/',                         MiselBulkView.as_view(),           name='misel-bulk'),
    path('misel/<str:misel_primary>/',          MiselDetailView.as_view(),         name='misel-detail'),
]