from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from adminka.serializers import *
from crm.models import *
from django.shortcuts import get_object_or_404
from adminka.permissions import *


@extend_schema(
    tags=["Applications"],
)
@api_view(['GET'])
@permission_classes([IsOrganisatorOrSupervisor])
def get_all_applications(request):
    applications = Application.objects.all()
    serializer = ApplicationSerializer(applications, many=True)
    return Response(serializer.data)


@extend_schema(
    tags=["Applications"],
    responses={200: ApplicationSerializer, 404: 'Application not found'}
)
@api_view(['GET'])
@permission_classes([IsOrganisatorOrSupervisor])
def get_application_by_id(request, application_id):
    application = get_object_or_404(Application, id=application_id)
    serializer = ApplicationSerializer(application)
    return Response(serializer.data)


@extend_schema(
    tags=["Applications"],
    request=ApplicationSerializer,
    responses={201: ApplicationSerializer, 400: 'Invalid data'}
)
@api_view(['POST'])
@permission_classes([IsOrganisatorOrSupervisor])
def create_application(request):
    serializer = ApplicationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    tags=["Applications"],
    request=ApplicationSerializer,
    responses={200: ApplicationSerializer, 400: 'Invalid data', 404: 'Application not found'}
)
@api_view(['PUT'])
@permission_classes([IsOrganisatorOrSupervisor])
def update_application(request, application_id):
    application = get_object_or_404(Application, id=application_id)
    serializer = ApplicationSerializer(application, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    tags=["Applications"],
    responses={204: 'No Content', 404: 'Application not found'}
)
@api_view(['DELETE'])
@permission_classes([IsOrganisatorOrSupervisor])
def delete_application(request, application_id):
    application = get_object_or_404(Application, id=application_id)
    application.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

