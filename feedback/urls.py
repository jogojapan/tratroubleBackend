from django.urls import path
from .views import SubmitEmailView, VerifyEmailView, SubmitFeedbackView, CheckTokenView

urlpatterns = [
    path('submit-email/', SubmitEmailView.as_view(), name='submit-email'),
    path('verify-email/', VerifyEmailView.as_view(), name='verify-email'),
    path('submit-feedback/', SubmitFeedbackView.as_view(), name='submit-feedback'),
    path('check-token/', CheckTokenView.as_view(), name='check-token'),
]
