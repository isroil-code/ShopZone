from rest_framework import serializers
from .models import SellerIndividual, SellerEntrepreneur, SellerCompany, Seller, SellerProfile, SellerBankAccount
from apps_.users.serializer import UserProfileSerializer
from apps_.users.models import UserProfile

class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = ['biznes_type', 'status', 'created_at', 'updated_at']
        read_only_fields = ['status', 'created_at', 'updated_at']  

class SellerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellerProfile
        fields = ['name', 'surname', 'phone_number2', 'father_name']
    
    def validate_name(self, value):
        if not value or len(value.strip()) < 2:
            raise serializers.ValidationError("Ism kamida 2 ta belgidan iborat bo'lishi kerak.")
        return value.strip()
    
    def validate_surname(self, value):
        if not value or len(value.strip()) < 2:
            raise serializers.ValidationError("Familiya kamida 2 ta belgidan iborat bo'lishi kerak.")
        return value.strip()
    
    def validate_father_name(self, value):
        if not value or len(value.strip()) < 2:
            raise serializers.ValidationError("Otasining ismi kamida 2 ta belgidan iborat bo'lishi kerak.")
        return value.strip()
    
    def validate_phone_number2(self, value):
 
        if not value:
            raise serializers.ValidationError("Qo'shimcha telefon raqam kiritilishi shart.")
        
        return value
        
class SellerIndividualSerializer(serializers.ModelSerializer):
    biznes_type = serializers.ChoiceField(
        choices=["individual"], read_only=True
    )
    
    class Meta:
        model = SellerIndividual
        fields = ['jshshir', 'ruyhatdan_otish_guvohnamasi_raqami', 'passport_image','inn','created_at', 'updated_at', 'biznes_type']
    
    def validate_jshshir(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("JSHSHIR faqat raqamlardan iborat bo'lishi kerak.")
        if len(value) != 14:
            raise serializers.ValidationError("JSHSHIR 14 ta raqamdan iborat bo'lishi kerak.")
        return value
    
    def validate_ruyhatdan_otish_guvohnamasi_raqami(self, value):
        if not value or len(value.strip()) == 0:
            raise serializers.ValidationError("Ro'yxatdan o'tish guvohnomasi raqami kiritilishi shart.")
        return value
    
class SellerEntrepreneurSerializer(serializers.ModelSerializer):
    biznes_type = serializers.ChoiceField(
        choices=["entrepreneur"], read_only=True
    )
    
    class Meta:
        model = SellerEntrepreneur
        fields = ['birth_date', 'passport_series', 'passport_number', 'jshshir', 'ruyhatdan_otish_guvohnamasi_raqami', 'passport_image', 'inn', 'created_at', 'biznes_type']
    
    def validate_jshshir(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("JSHSHIR faqat raqamlardan iborat bo'lishi kerak.")
        if len(value) != 14:
            raise serializers.ValidationError("JSHSHIR 14 ta raqamdan iborat bo'lishi kerak.")
        return value
    
    def validate_passport_series(self, value):
        if not value or len(value) != 2:
            raise serializers.ValidationError("Passport seriyasi 2 ta harfdan iborat bo'lishi kerak.")
        if not value.isalpha():
            raise serializers.ValidationError("Passport seriyasi faqat harflardan iborat bo'lishi kerak.")
        return value.upper()
    
    def validate_passport_number(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("Passport raqami faqat raqamlardan iborat bo'lishi kerak.")
        if len(value) != 7:
            raise serializers.ValidationError("Passport raqami 7 ta raqamdan iborat bo'lishi kerak.")
        return value
    
class SellerCompanySerializer(serializers.ModelSerializer):
    biznes_type = serializers.ChoiceField(
        choices=["company"], read_only=True
    )
    
    class Meta:
        model = SellerCompany
        fields = ['company_name', 'stir', 'oked','registration_certificate','tashkilot_direktori_qarori', 'passport_image','created_at', 'updated_at', 'biznes_type']
    
    def validate_stir(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("STIR faqat raqamlardan iborat bo'lishi kerak.")
        if len(value) != 9:
            raise serializers.ValidationError("STIR 9 ta raqamdan iborat bo'lishi kerak.")
        return value
    
    def validate_oked(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("OKED faqat raqamlardan iborat bo'lishi kerak.")
        if len(value) != 5:
            raise serializers.ValidationError("OKED 5 ta raqamdan iborat bo'lishi kerak.")
        return value
    
    def validate_company_name(self, value):
        if not value or len(value.strip()) < 3:
            raise serializers.ValidationError("Kompaniya nomi kamida 3 ta belgidan iborat bo'lishi kerak.")
        return value
        


class SellerInformationSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField()
    individual_info = serializers.SerializerMethodField()
    entrepreneur_info = serializers.SerializerMethodField()
    company_info = serializers.SerializerMethodField()
    email = serializers.CharField(source='user.email', read_only=True)
    tasdiqlash_screenshoti_or_rasmi = serializers.FileField(source='shartnoma.first.tasdiqlash_screenshoti_or_rasmi', required=True)
    


    class Meta:
        model = Seller
        fields = ['biznes_type','email', 'status', 'created_at', 'updated_at', 'profile', 'individual_info', 'entrepreneur_info', 'company_info', 'tasdiqlash_screenshoti_or_rasmi']
        

    def get_profile(self, obj):
        try:
            profile = obj.profile
            return SellerProfileSerializer(profile).data
        except SellerProfile.DoesNotExist:
            return None
        
    def get_individual_info(self, obj):
        try:
            individual_info = obj.individual_info
            return SellerIndividualSerializer(individual_info).data
        except SellerIndividual.DoesNotExist:
            return None
        
    def get_entrepreneur_info(self, obj):
        try:
            entrepreneur_info = obj.entrepreneur_info
            return SellerEntrepreneurSerializer(entrepreneur_info).data
        except SellerEntrepreneur.DoesNotExist:
            return None
        
    def get_company_info(self, obj):        
        try:
            company_info = obj.company_info
            return SellerCompanySerializer(company_info).data
        except SellerCompany.DoesNotExist:
            return None
        
        
class BankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellerBankAccount
        fields = ['bank_name', 'account_number', 'bank_code']
    
    def validate_bank_code(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("Bank kodi (MFO) faqat raqamlardan iborat bo'lishi kerak.")
        if len(value) != 5:
            raise serializers.ValidationError("Bank kodi (MFO) 5 ta raqamdan iborat bo'lishi kerak.")
        return value
    
    def validate_account_number(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("Hisob raqami faqat raqamlardan iborat bo'lishi kerak.")
        if len(value) != 16:
            raise serializers.ValidationError("Hisob raqami 16 ta raqamdan iborat bo'lishi kerak.")
        return value
    
    def validate_bank_name(self, value):
        if not value or len(value.strip()) < 3:
            raise serializers.ValidationError("Bank nomi kamida 3 ta belgidan iborat bo'lishi kerak.")
        return value

class SellerCommisionerSerializer(serializers.ModelSerializer):
    biznes_type = serializers.CharField(read_only=True)
    status = serializers.CharField(read_only=True)
    jshshir_or_stir = serializers.SerializerMethodField()
    shartnoma_raqami = serializers.CharField(source='shartnoma.first.shartnoma_raqami', read_only=True)
    bank_code = serializers.SerializerMethodField()
    hisob_raqami = serializers.SerializerMethodField()
    shartnoma_tuzilgan_sana = serializers.SerializerMethodField()
    shartnoma_amaldagi_sana = serializers.SerializerMethodField()
    email = serializers.CharField(source='user.email', read_only=True)  
    tasdiqlash_screenshoti_or_rasmi = serializers.FileField(source='shartnoma.first.tasdiqlash_screenshoti_or_rasmi', required=True)
    
    name = serializers.CharField(source='profile.name', read_only=True)
    surname = serializers.CharField(source='profile.surname', read_only=True)
    father_name = serializers.CharField(source='profile.father_name', read_only=True)
    phone_number2 = serializers.CharField(source='profile.phone_number2', read_only=True)
    
    class Meta:
        model = Seller
        fields = ['id', 'email', 'name', 'surname', 'father_name', 'phone_number2', 'biznes_type', 'status', 'jshshir_or_stir', 'shartnoma_raqami', 'bank_code', 'hisob_raqami', 'shartnoma_tuzilgan_sana', 'shartnoma_amaldagi_sana', 'tasdiqlash_screenshoti_or_rasmi']


    def get_jshshir_or_stir(self, obj):
        biznes_type = obj.biznes_type
        if biznes_type == 'individual':
            try:
                return obj.individual_info.jshshir
            except SellerIndividual.DoesNotExist:
                return None
        elif biznes_type == 'entrepreneur':
            try:
                return obj.entrepreneur_info.jshshir
            except SellerEntrepreneur.DoesNotExist:
                return None
        elif biznes_type == 'company':
            try:
                return obj.company_info.stir
            except SellerCompany.DoesNotExist:
                return None
        return None
    
    def get_bank_code(self, obj):
        try:
            return obj.bank_account.first().bank_code
        except (SellerBankAccount.DoesNotExist, AttributeError):
            return None
    
    def get_hisob_raqami(self, obj):
        try:
            return obj.bank_account.first().account_number
        except (SellerBankAccount.DoesNotExist, AttributeError):
            return None
    
    def get_shartnoma_tuzilgan_sana(self, obj):
        try:
            return obj.shartnoma.first().signed_at
        except (AttributeError, TypeError):
            return None
    
    def get_shartnoma_amaldagi_sana(self, obj):
        try:
            return obj.shartnoma.first().to_date
        except (AttributeError, TypeError):
            return None
    
    
    