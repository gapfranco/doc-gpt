from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers.query_serializers import QuerySerializer

from core.models import Topic
from core.utils.QueryManager import QueryManager


class QueryView(APIView):
    # @context_correlation_id_from_request("boletos")
    def post(self, request):
        serializer = QuerySerializer(data=request.data)
        if serializer.is_valid():
            topic_id = request.data["topic_id"]
            query = request.data["query"]

            topico = Topic.objects.get(pk=topic_id)
            collection_id = str(topico.collection_id)
            query_manager = QueryManager(collection_id)
            answer, cost = query_manager.question(query)

            return Response(
                {
                    "query": answer["query"],
                    "result": answer["result"],
                    "cost": cost,
                }
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
