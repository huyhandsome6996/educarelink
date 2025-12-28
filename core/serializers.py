from rest_framework import serializers
from django.contrib.auth.models import User
from .models import CarePartner, Booking


# ========== USER REGISTER ==========
class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email', '')
        )


# ========== CARE PARTNER ==========
class CarePartnerListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarePartner
        fields = [
            'id', 'ho_ten', 'gioi_tinh', 'nam_sinh',
            'ky_nang', 'kinh_nghiem', 'gia_theo_gio',
            'khu_vuc'
        ]


class CarePartnerDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarePartner
        exclude = ['so_cccd', 'anh_cccd_mat_truoc', 'anh_cccd_mat_sau']


class CarePartnerRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarePartner
        exclude = ['user', 'trang_thai', 'ngay_gui']


# ========== BOOKING ==========
class BookingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = [
            'nguoi_ho_tro',
            'thoi_gian_bat_dau',
            'thoi_gian_ket_thuc',
            'ghi_chu'
        ]




# Serializer dùng cho CarePartner xem booking
# Không cho sửa, chỉ xem
class BookingListSerializer(serializers.ModelSerializer):
    nguoi_dat = serializers.CharField(source="nguoi_dat.username", read_only=True)

    class Meta:
        model = Booking
        fields = [
            "id",
            "nguoi_dat",
            "thoi_gian_bat_dau",
            "thoi_gian_ket_thuc",
            "ghi_chu",
            "trang_thai",
            "ngay_gui",
        ]
