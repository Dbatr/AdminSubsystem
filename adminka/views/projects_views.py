from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from adminka.serializers import *
from crm.models import *
from django.shortcuts import get_object_or_404


@api_view(['GET'])
def get_all_projects(request):
    projects = Project.objects.all()
    serializer = ProjectSerializer(projects, many=True)
    return Response(serializer.data)

@extend_schema(
    responses={200: ProjectSerializer, 404: 'Project not found'}
)
@api_view(['GET'])
def get_project_by_id(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    serializer = ProjectSerializer(project)
    return Response(serializer.data)


@extend_schema(
    request=ProjectSerializer,
    responses={201: ProjectSerializer, 400: 'Invalid data'}
)
@api_view(['POST'])
def create_project(request):
    serializer = ProjectSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    request=ProjectSerializer,
    responses={200: ProjectSerializer, 400: 'Invalid data', 404: 'Project not found'}
)
@api_view(['PUT'])
def update_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    serializer = ProjectSerializer(project, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    responses={204: 'No Content', 404: 'Project not found'}
)
@api_view(['DELETE'])
def delete_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    project.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)