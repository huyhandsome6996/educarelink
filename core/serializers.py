from rest_framework import serializers
from .models import CarePartner, Booking


class CarePartnerListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarePartner
        fields = [
            'id',
            'ho_ten',
            'gioi_tinh',
            'nam_sinh',
            'ky_nang',
            'kinh_nghiem',
            'gia_theo_gio',
            'khu_vuc',
            'dang_hoat_dong',
        ]


class CarePartnerDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarePartner
        exclude = [
            'so_cccd',
            'anh_cccd_mat_truoc',
            'anh_cccd_mat_sau',
        ]


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = [
            'id',
            'ten_phu_huynh',
            'so_dien_thoai',
            'nguoi_ho_tro',
            'thoi_gian_bat_dau',
            'thoi_gian_ket_thuc',
            'ghi_chu',
            'trang_thai',
            'ngay_gui',
        ]
        read_only_fields = ['trang_thai', 'ngay_gui']
