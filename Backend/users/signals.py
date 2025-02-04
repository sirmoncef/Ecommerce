from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail
from django.dispatch import receiver
import random

@receiver(reset_password_token_created)
def send_otp_email(sender, instance, reset_password_token, *args, **kwargs):
    """
    Envoie un email contenant un OTP pour la réinitialisation du mot de passe.
    """
    
    otp_code = str(random.randint(100000, 999999))  

    
    reset_password_token.key = otp_code  
    reset_password_token.save()

   
    email_message = f"""
    Bonjour {reset_password_token.user.username},

    Vous avez demandé à réinitialiser votre mot de passe.

    🔑 Votre code OTP : {otp_code}

    Si vous n'avez pas demandé cette réinitialisation, ignorez cet email.

    Cordialement,
    L'équipe de support
    """

    
    send_mail(
        subject="🔑 Réinitialisation du mot de passe - Code OTP",
        message=email_message,
        from_email="moncefzabat37@gmail.com",  
        recipient_list=[reset_password_token.user.email],  
        fail_silently=False
    )
