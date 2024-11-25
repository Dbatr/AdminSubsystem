from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from adminka.serializers import *
from crm.models import *
from django.shortcuts import get_object_or_404


@api_view(['GET'])
def get_all_applications(request):
    applications = Application.objects.all()
    serializer = ApplicationSerializer(applications, many=True)
    return Response(serializer.data)


@extend_schema(
    responses={200: ApplicationSerializer, 404: 'Application not found'}
)
@api_view(['GET'])
def get_application_by_id(request, application_id):
    application = get_object_or_404(Application, id=application_id)
    serializer = ApplicationSerializer(application)
    return Response(serializer.data)


@extend_schema(
    request=ApplicationSerializer,
    responses={201: ApplicationSerializer, 400: 'Invalid data'}
)
@api_view(['POST'])
def create_application(request):
    serializer = ApplicationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    request=ApplicationSerializer,
    responses={200: ApplicationSerializer, 400: 'Invalid data', 404: 'Application not found'}
)
@api_view(['PUT'])
def update_application(request, application_id):
    application = get_object_or_404(Application, id=application_id)
    serializer = ApplicationSerializer(application, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    responses={204: 'No Content', 404: 'Application not found'}
)
@api_view(['DELETE'])
def delete_application(request, application_id):
    application = get_object_or_404(Application, id=application_id)
    application.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

