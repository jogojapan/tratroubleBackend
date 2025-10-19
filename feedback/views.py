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

class SubmitEmailView(APIView):
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)
        platform = request.data.get('platform') or 'web'

        # Generate token using HMAC with secret key
        secret_key = settings.SECRET_KEY.encode('utf-8')
        token = hmac.new(secret_key, email.encode('utf-8'), hashlib.sha256).hexdigest()

        # Create or update EmailVerification record
        ev, created = EmailVerification.objects.update_or_create(
            email=email,
            defaults={'token': token, 'created_at': timezone.now(), 'verified': False}
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

class VerifyEmailView(APIView):
    def post(self, request):
        token = request.data.get('token')
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
