import qrcode
from io import BytesIO
from django.core.files.base import ContentFile
from PIL import Image

QRCODE_SERVER_URL = 'https://cheese4cut-qrcode.vercel.app/'

# qrcode 생성
def genQR(id: int) -> ContentFile:
    qr = qrcode.QRCode(
        version=1,      # qr의 저장 size
        error_correction=qrcode.ERROR_CORRECT_M,    # 오류 복원 레벨
        box_size=3,     # qr 이미지 크기
        border=1        # 테두리 여백
    )
    qr.add_data(QRCODE_SERVER_URL + '/' + str(id))
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    # 이미지를 메모리 상의 BytesIO 객체에 저장
    img_io = BytesIO()
    img.save(img_io, format='PNG')  # PNG 형식으로 저장
    img_io.seek(0)  # 파일 포인터를 처음으로 이동

    # ContentFile로 반환 (Django ImageField에 저장할 수 있는 형식)
    return ContentFile(img_io.read(), name=f'qr_{id}.png')