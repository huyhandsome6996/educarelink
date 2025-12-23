from django.urls import path
from .views import CarePartnerListAPIView, CarePartnerDetailAPIView, BookingCreateAPIView

urlpatterns = [
    path('care-partners/', CarePartnerListAPIView.as_view()),
    path('care-partners/<int:pk>/', CarePartnerDetailAPIView.as_view()),
    path('bookings/', BookingCreateAPIView.as_view()),
]
