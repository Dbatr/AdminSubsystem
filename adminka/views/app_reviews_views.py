from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from adminka.serializers import *
from crm.models import *
from django.shortcuts import get_object_or_404


@api_view(['GET'])
def get_all_reviews(request):
    reviews = App_review.objects.all()
    serializer = AppReviewSerializer(reviews, many=True)
    return Response(serializer.data)


@extend_schema(
    responses={200: AppReviewSerializer, 404: 'Review not found'}
)
@api_view(['GET'])
def get_review_by_id(request, review_id):
    review = get_object_or_404(App_review, id=review_id)
    serializer = AppReviewSerializer(review)
    return Response(serializer.data)


@extend_schema(
    request=AppReviewSerializer,
    responses={201: AppReviewSerializer, 400: 'Invalid data'}
)
@api_view(['POST'])
def create_review(request):
    serializer = AppReviewSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    request=AppReviewSerializer,
    responses={200: AppReviewSerializer, 400: 'Invalid data', 404: 'Review not found'}
)
@api_view(['PUT'])
def update_review(request, review_id):
    review = get_object_or_404(App_review, id=review_id)
    serializer = AppReviewSerializer(review, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    responses={204: 'No Content', 404: 'Review not found'}
)
@api_view(['DELETE'])
def delete_review(request, review_id):
    review = get_object_or_404(App_review, id=review_id)
    review.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
