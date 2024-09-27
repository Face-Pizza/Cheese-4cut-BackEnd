from rest_framework import serializers
from .models import *
import base64, uuid, io
from django.core.files.base import ContentFile
from .utils import genQR

class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = '__all__'

    """def create(self, validated_data):
        image_data = validated_data.get('photo')
        # Photo 인스턴스 생성
        photo_instance = super().create(validated_data)
        qr_img = genQR(photo_instance.id)

        qr_io = io.BytesIO()
        qr_img.save(qr_io, format='PNG')
        qr_file_name = f'{uuid.uuid4()}.png'
        photo_instance.qr_code.save(qr_file_name, ContentFile(qr_io.getvalue()), save=True)

        # 제대로 디코딩 되는지 확인
        if image_data and image_data.startswith('data:image'):
            format, imgstr = image_data.split(';base64,')
            ext = format.split('/')[-1]
            #imgstr = base64.b64decode(imgstr)
            #file_name = f"{uuid.uuid4()}.{ext}"
            #image_file = ContentFile(imgstr, name=file_name)

            if ext not in ['jpg', 'jpeg', 'png']:
                raise serializers.ValidationError("Unsupported file type")
            
            #photo_instance.photo.save(file_name, image_file, save=True)
            photo_instance.photo = image_data
            photo_instance.save()
            
        return photo_instance"""