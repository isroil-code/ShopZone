import os
from django.core.exceptions import ValidationError

ALLOWED_EXTENSIONS = [".pdf", ".jpg", ".jpeg", ".png"]
MAX_FILE_SIZE = 10 * 1024 * 1024  

def validate_file(file):
    ext = os.path.splitext(file.name)[1].lower()

    if ext not in ALLOWED_EXTENSIONS:
        raise ValidationError("Faqat PDF, JPG, PNG ruxsat etiladi")

    if file.size > MAX_FILE_SIZE:
        raise ValidationError("Fayl hajmi 10MB dan katta bo'lmasligi kerak")
    
    
def validate_account_number(account_number):
    required_numbers = ['2020', '2021', '2021']
    if not account_number.startswith(tuple(required_numbers)):
        raise ValidationError(f"Hisob raqami quyidagi raqamlar bilan boshlanishi kerak: {', '.join(required_numbers)}")
    
    
