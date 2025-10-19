from datetime import timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import BasePermission
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied
from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import salted_hmac
from .models import Feedback, EmailVerification
from django.utils import timezone
import hashlib
import hmac
import secrets


class IsValidTokenPermission(BasePermission):
    def has_permission(self, request, view):
        token = None
        if request.method == 'GET':
            token = request.query_params.get('token')
        else:
            token = request.data.get('token')
        if not token:
            raise AuthenticationFailed('Token is required')
        try:
            ev = EmailVerification.objects.get(token=token)
        except EmailVerification.DoesNotExist:
            raise AuthenticationFailed('Invalid token')
        if not ev.verified:
            raise PermissionDenied('Email not verified for this token')
        request.email_verification = ev
        return True

# Import email verification domain
from tratroubleBackend.email_config import EMAIL_VERIFICATION_DOMAIN
from tratroubleBackend.email_config import EMAIL_VERIFICATION_APP_NAME

class DeviceIdentifier:
    def get_device_id(self, request):
        """Extract device identifier from request"""
        # Try to get device ID from custom header (mobile apps)
        device_id = request.META.get('HTTP_X_DEVICE_ID')

        # Fallback to User-Agent fingerprinting for web
        if not device_id:
            user_agent = request.META.get('HTTP_USER_AGENT', '')
            accept_language = request.META.get('HTTP_ACCEPT_LANGUAGE', '')
            # Create fingerprint from browser characteristics
            fingerprint_data = f"{user_agent}|{accept_language}"
            device_id = hashlib.sha256(fingerprint_data.encode()).hexdigest()[:32]

        return device_id

class SubmitEmailView(APIView):
    TOKEN_EXPIRY_HOURS = 24

    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)
        platform = request.data.get('platform') or 'web'
        device_id = DeviceIdentifier().get_device_id(request)
        token_data = f"{email}{device_id}{secrets.token_urlsafe(16)}{timezone.now().timestamp()}"
        secret_key = settings.SECRET_KEY.encode('utf-8')

        # Generate token using HMAC with secret key
        token = self._generate_hmac_token(email, device_id)
        expires_at = timezone.now() + timedelta(hours=self.TOKEN_EXPIRY_HOURS)
        
        # Create or update EmailVerification record
        ev = EmailVerification.objects.create(
            email=email,
            token=token,
            device_id=device_id,
            platform=platform,
            created_at=timezone.now(),
            expires_at=expires_at,
            verified=False,
        )

        verification_link = f"https://{EMAIL_VERIFICATION_DOMAIN}/api/verify-email/?token={token}"
        send_mail(
            'Verify your email',
            f'Click the link to verify your email: {verification_link}',
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )
        return Response({'message': 'Verification email sent'})

    def _generate_hmac_token(self, email, device_id):
        """Generate HMAC-signed token"""
        # Include timestamp for uniqueness
        timestamp = str(int(timezone.now().timestamp()))

        # Create message to sign
        message = f"{email}|{device_id}|{timestamp}|{secrets.token_urlsafe(8)}"

        # Sign with Django's SECRET_KEY
        secret_key = settings.SECRET_KEY.encode('utf-8')
        signature = hmac.new(
            secret_key,
            message.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()

        return signature  # This will be the token

class VerifyEmailView(APIView):
    def post(self, request):
        token = request.data.get('token')
        if not token:
            return Response({'error': 'Token is required'}, status=status.HTTP_400_BAD_REQUEST)
        if len(token) != 64:
            return Response({'error': 'Invalid token format'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            ev = EmailVerification.objects.get(token=token)
        except EmailVerification.DoesNotExist:
            return Response({'error': 'Invalid token'}, status=status.HTTP_404_NOT_FOUND)

        if ev.verified:
            return Response({'error': 'Email already verified'}, status=status.HTTP_409_CONFLICT)
        
        if timezone.now() > ev.expires_at:
            return Response({'error': 'Verification token expired'}, status=status.HTTP_410_GONE)

        # Device binding verification - critical security check
        current_device_id = DeviceIdentifier().get_device_id(request)
        if ev.device_id and ev.device_id != current_device_id:
            return Response({
                'error': 'Device mismatch', 
                'message': 'Verification must be completed on the same device that requested it.'
            }, status=status.HTTP_400_BAD_REQUEST)

        ev.verified = True
        ev.save()

        return Response({'message': 'Email verified successfully'})

class SubmitFeedbackView(APIView):
    permission_classes = [IsValidTokenPermission]

    def post(self, request):
        token = request.data.get('token')
        line = request.data.get('line')
        destination = request.data.get('destination')
        geo_location = request.data.get('geo_location')
        
        if not all([token, line, destination, geo_location]):
            return Response({'error': 'All fields are required'}, status=status.HTTP_400_BAD_REQUEST)

        feedback = Feedback.objects.create(
            token=token,
            line=line,
            destination=destination,
            geo_location=geo_location
        )
        return Response({'message': 'Feedback submitted successfully'})
        
class BadJsonView(APIView):
    permission_classes = [IsValidTokenPermission]

    def post(self, request):
        token = request.data.get('token')
        json_str = request.data.get('json')
        target = request.data.get('target')

        if not all([token, json_str, target]):
            return Response({'error': 'All fields are required'}, status=status.HTTP_400_BAD_REQUEST)

        print(f"Received bad-json request with token={token}, json={json_str}, target={target}")
        return Response({'message': 'Received bad-json request'})

class CheckTokenView(APIView):
    def get(self, request):
        token = request.query_params.get('token')
        if not token:
            return Response({'error': 'Token is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            ev = EmailVerification.objects.get(token=token)
        except EmailVerification.DoesNotExist:
            return Response({'error': 'Unknown token'}, status=status.HTTP_404_NOT_FOUND)

        if not ev.verified:
            return Response({'error': 'Email not verified for this token'}, status=status.HTTP_403_FORBIDDEN)

        return Response({'message': 'ok'}, status=status.HTTP_200_OK)
