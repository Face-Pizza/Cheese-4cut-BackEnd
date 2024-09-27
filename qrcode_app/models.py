from django.db import models

# Create your models here.
# Photo 모델 생성
class Photo(models.Model):
    id = models.AutoField(primary_key=True)
    photo = models.ImageField(blank=True)    # 네컷 사진
    created_at = models.DateTimeField(auto_now_add=True)    # 생성 날짜
    qr_code = models.ImageField(upload_to='QRcode/', blank=True, null=True)
    # 그냥 항상 유저 정보 불일치 값을 넣어놓고 링크 이동 못하게 해야겠다