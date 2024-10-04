from rest_framework import status, viewsets
from rest_framework.response import Response
from .models import Photo
from .serializers import PhotoSerializer
from .utils import genQR, decrypt_id
from django.http import HttpResponse, JsonResponse

class PhotoViewSet(viewsets.ModelViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer

    def create(self, request, *args, **kwargs):
        # request.FILES를 함께 serializer에 전달
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # 파일을 포함한 데이터를 저장 (DB에 먼저 저장하여 ID 생성)
            photo_instance = serializer.save()

            # QR 코드 생성 후 해당 photo_instance에 저장
            qr_code_image = genQR(photo_instance.id)  # genQR 함수에서 ContentFile 반환
            photo_instance.qr_code.save(f"qr_{photo_instance.id}.png", qr_code_image)
            photo_instance.save()  # 다시 저장하여 qr_code 갱신

            qr_code_url = photo_instance.qr_code.url  # QR 코드 URL 반환

            return Response({
                    "message": "Image and QR code generated successfully!",
                    "qr_code_url": qr_code_url
                }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # QR 코드 스캔 후 암호화된 ID를 복호화하여 처리하는 뷰
def qr_code_view(request, encrypted_id):
    try:
        # 암호화된 ID 복호화
        user_id = decrypt_id(encrypted_id)
        
        # 해당 ID의 사진 데이터를 처리 (예시로 해당 photo를 가져옴)
        photo_instance = Photo.objects.get(id=user_id)
        
        # 예시로 Photo 객체의 정보 반환
        return JsonResponse({
            "photo_id": photo_instance.id,
            "image_url": photo_instance.image.url,
            "message": "QR code processed successfully."
        })

    except Photo.DoesNotExist:
        return HttpResponse("Photo not found.", status=404)

    except Exception as e:
        return HttpResponse("Invalid QR Code.", status=400)