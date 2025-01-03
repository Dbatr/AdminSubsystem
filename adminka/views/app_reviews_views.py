from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from adminka.serializers import *
from crm.models import *
from django.shortcuts import get_object_or_404
from adminka.permissions import *

@extend_schema(
    tags=["App reviews"],
)
@api_view(['GET'])
@permission_classes([IsOrganisatorOrSupervisor])
def get_all_reviews(request):
    reviews = App_review.objects.all()
    serializer = AppReviewSerializer(reviews, many=True)
    return Response(serializer.data)


@extend_schema(
    tags=["App reviews"],
    responses={200: AppReviewSerializer, 404: 'Review not found'}
)
@api_view(['GET'])
@permission_classes([IsOrganisatorOrSupervisor])
def get_review_by_id(request, review_id):
    review = get_object_or_404(App_review, id=review_id)
    serializer = AppReviewSerializer(review)
    return Response(serializer.data)


@extend_schema(
    tags=["App reviews"],
    request=AppReviewSerializer,
    responses={201: AppReviewSerializer, 400: 'Invalid data'}
)
@api_view(['POST'])
@permission_classes([IsOrganisatorOrSupervisor])
def create_review(request):
    serializer = AppReviewSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    tags=["App reviews"],
    request=AppReviewSerializer,
    responses={200: AppReviewSerializer, 400: 'Invalid data', 404: 'Review not found'}
)
@api_view(['PUT'])
@permission_classes([IsOrganisatorOrSupervisor])
def update_review(request, review_id):
    review = get_object_or_404(App_review, id=review_id)
    serializer = AppReviewSerializer(review, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    tags=["App reviews"],
    responses={204: 'No Content', 404: 'Review not found'}
)
@api_view(['DELETE'])
@permission_classes([IsOrganisatorOrSupervisor])
def delete_review(request, review_id):
    review = get_object_or_404(App_review, id=review_id)
    review.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
