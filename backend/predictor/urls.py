from django.urls import path
from .views import PredictAPIView, LivePredictAPIView

urlpatterns = [
    path('predict/', PredictAPIView.as_view(), name='predict'),
    path('live/<int:match_id>/', LivePredictAPIView.as_view(), name='live_predict'),
]
