from django.core.signing import TimestampSigner

signer = TimestampSigner()

def generate_verification_token(user_id):
    return signer.sign(user_id)

def verify_verification_token(token, max_age=3600):
    try:
        user_id = signer.unsign(token, max_age=max_age)
        return user_id
    except Exception:
        return None
    
    