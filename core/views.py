from rest_framework.views import APIView
from rest_framework.response import Response
from .models import CarePartner
from .serializers import (
    CarePartnerListSerializer,
    CarePartnerDetailSerializer
)


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
