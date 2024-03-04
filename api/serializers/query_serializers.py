from rest_framework import serializers


class QuerySerializer(serializers.Serializer):
    topic_id = serializers.CharField(max_length=256, required=True)
    query = serializers.CharField(max_length=2048)
