from rest_framework import serializers


class QuerySerializer(serializers.Serializer):
    topic_id = serializers.IntegerField()
    query = serializers.CharField(max_length=2048)
