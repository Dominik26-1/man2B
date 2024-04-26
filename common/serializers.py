from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers


class BasicSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        read_only_fields = ["avg_rating", 'count', 'latest_feedbacks']
        abstract = True

    days = openapi.Parameter('days', in_=openapi.IN_QUERY, description='description', type=openapi.TYPE_INTEGER)

    @swagger_auto_schema(manual_parameters=[days])
    def get_latest_feedbacks(self, instance):
        count = instance.new_feedback_count(self.context['request'].query_params)
        return count
