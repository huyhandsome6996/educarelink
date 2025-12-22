from django.urls import path
from .views import CarePartnerListAPIView, CarePartnerDetailAPIView

urlpatterns = [
    path('care-partners/', CarePartnerListAPIView.as_view()),
    path('care-partners/<int:pk>/', CarePartnerDetailAPIView.as_view()),
]
