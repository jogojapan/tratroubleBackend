from django.urls import path
from .views import SubmitEmailView, VerifyEmailView, SubmitFeedbackView, CheckTokenView
from .views import SubmitEmailView, VerifyEmailView, SubmitFeedbackView, CheckTokenView, BadJsonView

urlpatterns = [
    path('submit-email/', SubmitEmailView.as_view(), name='submit-email'),
    path('verify-email/', VerifyEmailView.as_view(), name='verify-email'),
    path('submit-feedback/', SubmitFeedbackView.as_view(), name='submit-feedback'),
    path('bad-json/', BadJsonView.as_view(), name='bad-json'),
    path('check-token/', CheckTokenView.as_view(), name='check-token'),
]
