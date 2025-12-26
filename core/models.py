from django.db import models
from django.contrib.auth.models import User


class CarePartner(models.Model):
    TRANG_THAI_CHOICES = [
        ("cho_duyet", "Chờ duyệt"),
        ("da_duyet", "Đã duyệt"),
        ("tu_choi", "Từ chối"),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="care_partner"
    )

    ho_ten = models.CharField(max_length=100)
    gioi_tinh = models.CharField(max_length=10)
    nam_sinh = models.IntegerField()

    so_cccd = models.CharField(max_length=20)
    anh_cccd_mat_truoc = models.ImageField(upload_to="cccd/", null=True, blank=True) 
    anh_cccd_mat_sau = models.ImageField(upload_to="cccd/", null=True, blank=True)
    anh_bang_cap = models.ImageField(upload_to="bang_cap/", null=True, blank=True)

    ky_nang = models.TextField()
    kinh_nghiem = models.TextField()

    gia_theo_gio = models.IntegerField()
    khu_vuc = models.CharField(max_length=255)

    trang_thai = models.CharField(
        max_length=20,
        choices=TRANG_THAI_CHOICES,
        default="cho_duyet"
    )

    ngay_gui = models.DateTimeField(auto_now_add=True)
    dang_hoat_dong = models.BooleanField(default=True)

    def __str__(self):
        return self.ho_ten



class Booking(models.Model):
    ten_phu_huynh = models.CharField(max_length=100)
    so_dien_thoai = models.CharField(max_length=20)

    nguoi_ho_tro = models.ForeignKey(CarePartner, on_delete=models.CASCADE)

    thoi_gian_bat_dau = models.DateTimeField()
    thoi_gian_ket_thuc = models.DateTimeField()

    ghi_chu = models.TextField(blank=True)
    trang_thai = models.CharField(max_length=20, default="cho_xac_nhan")

    ngay_gui = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.ten_phu_huynh
