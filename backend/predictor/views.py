from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import PredictionSerializer
from .services.predictor import predict_win_probability
from .services.live_fetcher import fetch_live_match


class PredictAPIView(APIView):

    def post(self, request):
        serializer = PredictionSerializer(data=request.data)

        if serializer.is_valid():
            result = predict_win_probability(serializer.validated_data)
            return Response(result)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LivePredictAPIView(APIView):

    def get(self, request, match_id):

        match_data = fetch_live_match(match_id)

        if not match_data:
            return Response({"error": "Could not fetch live match"}, status=400)

        # If second innings data not present, just return match info
        if "current_score" not in match_data:
            return Response(match_data)

        # Otherwise compute prediction
        result = predict_win_probability(match_data)

        # Merge match info + prediction
        match_data.update(result)

        return Response(match_data)
