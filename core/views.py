from rest_framework.views import APIView
from rest_framework.response import Response
from .models import CarePartner, Booking
from .serializers import (
    CarePartnerListSerializer,
    CarePartnerDetailSerializer,
    BookingSerializer,
)
from rest_framework import status



class CarePartnerListAPIView(APIView):
    def get(self, request):
        qs = CarePartner.objects.filter(trang_thai="da_duyet")
        serializer = CarePartnerListSerializer(qs, many=True)
        return Response(serializer.data)


class CarePartnerDetailAPIView(APIView):
    def get(self, request, pk):
        try:
            care_partner = CarePartner.objects.get(pk=pk, trang_thai="da_duyet")
        except CarePartner.DoesNotExist:
            return Response({"detail": "Không tìm thấy"}, status=404)

        serializer = CarePartnerDetailSerializer(care_partner)
        return Response(serializer.data)

class BookingCreateAPIView(APIView):
    def post(self, request):
        serializer = BookingSerializer(data=request.data)

        if serializer.is_valid():
            care_partner = serializer.validated_data['nguoi_ho_tro']

            # Chỉ cho phép đặt lịch với CarePartner đã duyệt
            if care_partner.trang_thai != "da_duyet":
                return Response(
                    {"detail": "Care Partner chưa được duyệt"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            serializer.save(trang_thai="cho_xac_nhan")
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)