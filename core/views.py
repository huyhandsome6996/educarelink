from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User

from .models import CarePartner, Booking
from .serializers import (
    UserRegisterSerializer,
    CarePartnerListSerializer,
    CarePartnerDetailSerializer,
    CarePartnerRegisterSerializer,
    BookingCreateSerializer,
    BookingListSerializer
)


# ===== USER REGISTER =====
class UserRegisterAPIView(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Đăng ký thành công"}, status=201)
        return Response(serializer.errors, status=400)


# ===== CARE PARTNER PUBLIC =====
class CarePartnerListAPIView(APIView):
    def get(self, request):
        qs = CarePartner.objects.filter(trang_thai="da_duyet")
        return Response(CarePartnerListSerializer(qs, many=True).data)


class CarePartnerDetailAPIView(APIView):
    def get(self, request, pk):
        try:
            cp = CarePartner.objects.get(pk=pk, trang_thai="da_duyet")
        except CarePartner.DoesNotExist:
            return Response({"detail": "Không tìm thấy"}, status=404)
        return Response(CarePartnerDetailSerializer(cp).data)


# ===== CARE PARTNER REGISTER =====
class CarePartnerRegisterAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if hasattr(request.user, 'care_partner'):
            return Response({"detail": "Đã đăng ký rồi"}, status=400)

        serializer = CarePartnerRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({"detail": "Gửi hồ sơ thành công"}, status=201)
        return Response(serializer.errors, status=400)


# ===== BOOKING (PHỤ HUYNH) =====
class BookingCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = BookingCreateSerializer(data=request.data)

        if serializer.is_valid():
            cp = serializer.validated_data["nguoi_ho_tro"]

            # # check CarePartner đã được duyệt chưa
            if cp.trang_thai != "da_duyet":
                return Response(
                    {"detail": "CarePartner chưa được duyệt"},
                    status=400
                )

            # # QUAN TRỌNG: gán người đặt là user đang login
            serializer.save(nguoi_dat=request.user)

            return Response(
                {"detail": "Tạo booking thành công"},
                status=201
            )

        return Response(serializer.errors, status=400)



# ===== BOOKING LIST (CARE PARTNER) =====
class CarePartnerBookingListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            cp = request.user.care_partner
        except:
            return Response({"detail": "Bạn không phải CarePartner"}, status=403)

        qs = Booking.objects.filter(nguoi_ho_tro=cp)
        return Response(BookingListSerializer(qs, many=True).data)


# CarePartner xem danh sách booking của chính mình
# Chỉ user nào có CarePartner mới vào được
class CarePartnerBookingListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Nếu user không phải CarePartner → chặn
        if not hasattr(request.user, "care_partner"):
            return Response(
                {"detail": "Bạn không phải CarePartner"},
                status=403
            )

        bookings = Booking.objects.filter(
            nguoi_ho_tro=request.user.care_partner
        )

        serializer = BookingListSerializer(bookings, many=True)
        return Response(serializer.data)


# CarePartner nhận booking
class BookingAcceptAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, booking_id):
        # Chỉ CarePartner mới được nhận booking
        if not hasattr(request.user, "care_partner"):
            return Response({"detail": "Không có quyền"}, status=403)

        try:
            booking = Booking.objects.get(
                id=booking_id,
                nguoi_ho_tro=request.user.care_partner,
                trang_thai="cho_xac_nhan"
            )
        except Booking.DoesNotExist:
            return Response({"detail": "Booking không hợp lệ"}, status=404)

        booking.trang_thai = "da_nhan"
        booking.save()

        return Response({"detail": "Đã nhận booking"})


# CarePartner từ chối booking
class BookingRejectAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, booking_id):
        if not hasattr(request.user, "care_partner"):
            return Response({"detail": "Không có quyền"}, status=403)

        try:
            booking = Booking.objects.get(
                id=booking_id,
                nguoi_ho_tro=request.user.care_partner,
                trang_thai="cho_xac_nhan"
            )
        except Booking.DoesNotExist:
            return Response({"detail": "Booking không hợp lệ"}, status=404)

        booking.trang_thai = "tu_choi"
        booking.save()

        return Response({"detail": "Đã từ chối booking"})


# Phụ huynh hủy booking của chính mình
class BookingCancelAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, booking_id):
        try:
            booking = Booking.objects.get(
                id=booking_id,
                nguoi_dat=request.user
            )
        except Booking.DoesNotExist:
            return Response({"detail": "Booking không tồn tại"}, status=404)

        # Không cho hủy nếu đã hoàn thành
        if booking.trang_thai == "hoan_thanh":
            return Response({"detail": "Không thể hủy"}, status=400)

        booking.trang_thai = "huy"
        booking.save()

        return Response({"detail": "Đã hủy booking"})


# Đánh dấu booking hoàn thành
# (có thể do CarePartner hoặc sau này do hệ thống)
class BookingCompleteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, booking_id):
        if not hasattr(request.user, "care_partner"):
            return Response({"detail": "Không có quyền"}, status=403)

        try:
            booking = Booking.objects.get(
                id=booking_id,
                nguoi_ho_tro=request.user.care_partner,
                trang_thai="da_nhan"
            )
        except Booking.DoesNotExist:
            return Response({"detail": "Booking không hợp lệ"}, status=404)

        booking.trang_thai = "hoan_thanh"
        booking.save()

        return Response({"detail": "Booking đã hoàn thành"})
