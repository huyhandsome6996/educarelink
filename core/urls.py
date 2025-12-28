from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import *

urlpatterns = [
    # AUTH
    path("auth/register/", UserRegisterAPIView.as_view()),
    path("auth/login/", TokenObtainPairView.as_view()),
    path("auth/refresh/", TokenRefreshView.as_view()),

    # CARE PARTNER
    path("care-partners/", CarePartnerListAPIView.as_view()),
    path("care-partners/<int:pk>/", CarePartnerDetailAPIView.as_view()),
    path("care-partners/register/", CarePartnerRegisterAPIView.as_view()),
    path("care-partners/bookings/", CarePartnerBookingListAPIView.as_view()),

    # BOOKING
    path("bookings/", BookingCreateAPIView.as_view()),
    path("bookings/<int:booking_id>/accept/", BookingAcceptAPIView.as_view()),
    path("bookings/<int:booking_id>/reject/", BookingRejectAPIView.as_view()),
    path("bookings/<int:booking_id>/cancel/", BookingCancelAPIView.as_view()),
    path("bookings/<int:booking_id>/complete/", BookingCompleteAPIView.as_view()),
]

