from django.urls import path
from django.urls import path
from .views import SubmitEmailView, VerifyEmailView, CheckTokenView, BadJsonView, RideFeedbackView

urlpatterns = [
    path('submit-email/', SubmitEmailView.as_view(), name='submit-email'),
    path('verify-email/', VerifyEmailView.as_view(), name='verify-email'),
    path('ride-feedback/', RideFeedbackView.as_view(), name='ride-feedback'),
    path('bad-json/', BadJsonView.as_view(), name='bad-json'),
    path('check-token/', CheckTokenView.as_view(), name='check-token'),
]
