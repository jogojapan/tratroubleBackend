from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import salted_hmac
from .models import Feedback, EmailVerification
from django.utils import timezone
import hashlib
import hmac

# Import email verification domain
from tratroubleBackend.email_config import EMAIL_VERIFICATION_DOMAIN

class SubmitEmailView(APIView):
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Generate token using HMAC with secret key
        secret_key = settings.SECRET_KEY.encode('utf-8')
        token = hmac.new(secret_key, email.encode('utf-8'), hashlib.sha256).hexdigest()

        # Create or update EmailVerification record
        ev, created = EmailVerification.objects.update_or_create(
            email=email,
            defaults={'token': token, 'created_at': timezone.now(), 'verified': False}
        )

        verification_link = f"http://{EMAIL_VERIFICATION_DOMAIN}/api/verify-email/?token={token}"
        send_mail(
            'Verify your email',
            f'Click the link to verify your email: {verification_link}',
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )
        return Response({'message': 'Verification email sent'})

class VerifyEmailView(APIView):
    def get(self, request):
        token = request.query_params.get('token')
        if not token:
            return Response({'error': 'Token is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            ev = EmailVerification.objects.get(token=token)
        except EmailVerification.DoesNotExist:
            return Response({'error': 'Invalid token'}, status=status.HTTP_404_NOT_FOUND)

        if ev.verified:
            return Response({'error': 'Email already verified'}, status=status.HTTP_409_CONFLICT)

        if not ev.is_recent():
            return Response({'error': 'Verification token expired'}, status=status.HTTP_410_GONE)

        ev.verified = True
        ev.save()

        return Response({'message': 'Email verified successfully'})

class SubmitFeedbackView(APIView):
    def post(self, request):
        token = request.data.get('token')
        line = request.data.get('line')
        destination = request.data.get('destination')
        geo_location = request.data.get('geo_location')
        
        if not all([token, line, destination, geo_location]):
            return Response({'error': 'All fields are required'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if token is registered and verified
        try:
            ev = EmailVerification.objects.get(token=token)
        except EmailVerification.DoesNotExist:
            return Response({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)

        if not ev.verified:
            return Response({'error': 'Email not verified for this token'}, status=status.HTTP_403_FORBIDDEN)

        feedback = Feedback.objects.create(
            token=token,
            line=line,
            destination=destination,
            geo_location=geo_location
        )
        return Response({'message': 'Feedback submitted successfully'})

class CheckTokenView(APIView):
    def post(self, request):
        token = request.data.get('token')
        if not token:
            return Response({'error': 'Token is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            ev = EmailVerification.objects.get(token=token)
        except EmailVerification.DoesNotExist:
            return Response({'error': 'Unknown token'}, status=status.HTTP_404_NOT_FOUND)

        if not ev.verified:
            return Response({'error': 'Email not verified for this token'}, status=status.HTTP_403_FORBIDDEN)

        return Response({'message': 'ok'}, status=status.HTTP_200_OK)
