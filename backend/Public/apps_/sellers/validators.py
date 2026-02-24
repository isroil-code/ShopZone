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
  
    if not account_number or not account_number.strip():
        raise ValidationError("Hisob raqami kiritilishi shart.")

    if not account_number.isdigit():
        raise ValidationError("Hisob raqami faqat raqamlardan iborat bo'lishi kerak.")

    if len(account_number) != 16:
        raise ValidationError("Hisob raqami 16 ta raqamdan iborat bo'lishi kerak.")
    
 
    required_prefixes = ['2020', '2021']
    if not any(account_number.startswith(prefix) for prefix in required_prefixes):
        raise ValidationError(f"Hisob raqami {' yoki '.join(required_prefixes)} bilan boshlanishi kerak.")
    
