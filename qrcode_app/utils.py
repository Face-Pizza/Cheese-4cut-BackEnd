import qrcode
from io import BytesIO
from django.core.files.base import ContentFile
from PIL import Image
from cryptography.fernet import Fernet
import base64

# 대칭 키 생성 (한 번 생성 후 보관)
key = Fernet.generate_key()  # 이 키는 안전하게 보관해야 합니다
cipher_suite = Fernet(key)

# ID 암호화 함수
def encrypt_id(user_id: int) -> str:
    # ID를 바이트로 변환한 후 암호화
    user_id_bytes = str(user_id).encode('utf-8')
    encrypted_id = cipher_suite.encrypt(user_id_bytes)
    
    # URL-safe 문자열로 변환
    return base64.urlsafe_b64encode(encrypted_id).decode('utf-8')

# ID 복호화 함수
def decrypt_id(encrypted_id: str) -> int:
    # URL-safe 문자열을 다시 바이트로 변환한 후 복호화
    encrypted_id_bytes = base64.urlsafe_b64decode(encrypted_id)
    decrypted_id = cipher_suite.decrypt(encrypted_id_bytes)
    
    return int(decrypted_id.decode('utf-8'))

QRCODE_SERVER_URL = 'http://facepizza-cheese.site'

# qrcode 생성
def genQR(id: int) -> ContentFile:
    # ID를 암호화
    encrypted_id = encrypt_id(id)

    qr = qrcode.QRCode(
        version=1,      # qr의 저장 size
        error_correction=qrcode.ERROR_CORRECT_M,    # 오류 복원 레벨
        box_size=3,     # qr 이미지 크기
        border=1        # 테두리 여백
    )
    qr.add_data(f'{QRCODE_SERVER_URL}/{encrypted_id}')
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    # 이미지를 메모리 상의 BytesIO 객체에 저장
    img_io = BytesIO()
    img.save(img_io, format='PNG')  # PNG 형식으로 저장
    img_io.seek(0)  # 파일 포인터를 처음으로 이동

    # ContentFile로 반환 (Django ImageField에 저장할 수 있는 형식)
    return ContentFile(img_io.read(), name=f'qr_{id}.png')