from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, LoginSerializer
from django_rest_passwordreset.models import ResetPasswordToken



User = get_user_model()

class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
   
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data["user"]
            tokens = RefreshToken.for_user(user)

            return Response(
                {
                    "message": "Login successful",
                    "access": str(tokens.access_token),
                    "refresh": str(tokens),
                    
                },
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class LogoutView(APIView):
    permissions_clases  = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_toke = request.data["refresh"]
            token = RefreshToken(refresh_toke)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    

class VerifyOTPAndResetPasswordView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get("email")
        otp_code = request.data.get("otp")
        new_password = request.data.get("new_password")

        if not email or not otp_code or not new_password:
            return Response(
                {"error": "Vous devez entrer l'email, l'OTP et le nouveau mot de passe."}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            reset_token = ResetPasswordToken.objects.get(user__email=email, key=otp_code)
        except ResetPasswordToken.DoesNotExist:
            return Response(
                {"error": "OTP invalide ou email incorrect."}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # Récupérer l'utilisateur
        user = reset_token.user
        user.set_password(new_password)
        user.save()

        
        reset_token.delete()

        return Response(
            {"message": "Mot de passe réinitialisé avec succès."}, 
            status=status.HTTP_200_OK
        )

