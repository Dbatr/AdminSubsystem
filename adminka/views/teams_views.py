from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from adminka.serializers import *
from crm.models import *
from django.shortcuts import get_object_or_404


@extend_schema(
    responses={200: TeamSerializer}
)
@api_view(['GET'])
def get_all_teams(request):
    teams = Team.objects.all()
    serializer = TeamSerializer(teams, many=True)
    return Response(serializer.data)


@extend_schema(
    responses={200: TeamSerializer, 404: 'Team not found'}
)
@api_view(['GET'])
def get_team_by_id(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    serializer = TeamSerializer(team)
    return Response(serializer.data)


@extend_schema(
    request=TeamSerializer,
    responses={201: TeamSerializer, 400: 'Invalid data'}
)
@api_view(['POST'])
def create_team(request):
    serializer = TeamSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    request=TeamSerializer,
    responses={200: TeamSerializer, 400: 'Invalid data', 404: 'Team not found'}
)
@api_view(['PUT'])
def update_team(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    serializer = TeamSerializer(team, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    responses={204: 'No Content', 404: 'Team not found'}
)
@api_view(['DELETE'])
def delete_team(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    team.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)