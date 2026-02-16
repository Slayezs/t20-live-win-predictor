from rest_framework import serializers


class PredictionSerializer(serializers.Serializer):
    current_score = serializers.FloatField()
    overs_completed = serializers.FloatField()
    wickets_lost = serializers.IntegerField()
    target = serializers.FloatField()
