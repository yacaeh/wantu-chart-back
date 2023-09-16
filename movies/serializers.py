from .models import Episode
from rest_framework import serializers

class EpisodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Episode
        fields = ('__all__')
