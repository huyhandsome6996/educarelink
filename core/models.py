from django.db import models


class CarePartner(models.Model):
    TRANG_THAI_CHOICES = [
        ("cho_duyet", "Chờ duyệt"),
        ("da_duyet", "Đã duyệt"),
        ("tu_choi", "Từ chối"),
    ]

    ho_ten = models.CharField(max_length=100, verbose_name="Họ và tên")
    gioi_tinh = models.CharField(max_length=10, verbose_name="Giới tính")
    nam_sinh = models.IntegerField(verbose_name="Năm sinh")

    so_cccd = models.CharField(max_length=20, verbose_name="Số CCCD")
    anh_cccd_mat_truoc = models.ImageField(upload_to="cccd/", verbose_name="CCCD mặt trước")
    anh_cccd_mat_sau = models.ImageField(upload_to="cccd/", verbose_name="CCCD mặt sau")
    anh_bang_cap = models.ImageField(upload_to="bang_cap/", verbose_name="Ảnh bằng cấp")

    ky_nang = models.TextField(verbose_name="Kỹ năng")
    kinh_nghiem = models.TextField(verbose_name="Kinh nghiệm")

    gia_theo_gio = models.IntegerField(verbose_name="Giá theo giờ")
    khu_vuc = models.CharField(max_length=255, verbose_name="Khu vực")

    dang_hoat_dong = models.BooleanField(default=True)
    trang_thai = models.CharField(
        max_length=20,
        choices=TRANG_THAI_CHOICES,
        default="cho_duyet"
    )

    ngay_tao = models.DateTimeField(auto_now_add=True)

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
