# Create your views here.
from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets

days = openapi.Parameter('days', in_=openapi.IN_QUERY, description='look back period for feedbacks',
                         type=openapi.TYPE_INTEGER)


@method_decorator(name='list', decorator=swagger_auto_schema(
    manual_parameters=[days]))
class BasicView(viewsets.ModelViewSet):
    pass
