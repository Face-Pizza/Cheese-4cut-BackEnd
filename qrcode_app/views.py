from rest_framework import status, viewsets
from rest_framework.response import Response
from .models import Photo
from .serializers import PhotoSerializer
from .utils import genQR

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

            return Response({"message": "Image and QR code generated successfully!"}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    """queryset = Photo.objects.all()
    serializer_class = PhotoSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        photo = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)"""