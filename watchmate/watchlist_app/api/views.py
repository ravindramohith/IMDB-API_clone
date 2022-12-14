from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from rest_framework import status, generics, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly,IsAuthenticated
from watchlist_app.api.permissions import (
    AdminOrReadOnlyPermission,
    ReviewUserOrReadOnlyPermission,
)
from watchlist_app.models import WatchList, StreamPlatform, Review
from watchlist_app.api.serializers import (
    WatchListSerializer,
    StreamPlatformSerializer,
    ReviewSerializer,
)

# from rest_framework.decorators import api_view


class ReviewListGV(generics.ListCreateAPIView):
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [AdminOrReadOnlyPermission]

    # overwriting current query set:
    def get_queryset(self):
        pk = self.kwargs["pk"]
        return Review.objects.filter(watchlist=pk)


class ReviewDetailGV(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [ReviewUserOrReadOnlyPermission]


class ReviewCreateGV(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        return Review.objects.all()

    def perform_create(self, serializer):
        pk = self.kwargs["pk"]
        watchlist = WatchList.objects.get(pk=pk)
        reviewed_user = self.request.user
        reviewed_queryset = Review.objects.filter(
            watchlist=watchlist, reviewed_user=reviewed_user
        )
        if reviewed_queryset.exists():
            raise ValidationError("You already have Reviewed to this movie")

        if not watchlist.average_rating:
            watchlist.average_rating = serializer.validated_data["rating"]
        else:
            watchlist.average_rating = (
                watchlist.average_rating + serializer.validated_data["rating"]
            ) / 2
        watchlist.number_of_reviews += 1
        watchlist.save()
        serializer.save(watchlist=watchlist, reviewed_user=reviewed_user)


class StreamPlatformVS(viewsets.ModelViewSet):
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer


# class StreamPlatformVS(viewsets.ViewSet):
#     def list(self, request):
#         queryset = StreamPlatform.objects.all()
#         serializer = StreamPlatformSerializer(queryset, many=True)
#         return Response(serializer.data)

#     def retrieve(self, request, pk=None):
#         queryset = StreamPlatform.objects.get(pk=pk)
#         serializer = StreamPlatformSerializer(queryset)
#         return Response(serializer.data)

#     def create(self, request):
#         serializer = StreamPlatformSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StreamPlatformListAV(APIView):
    def get(self, request):
        try:
            StreamPlatforms = StreamPlatform.objects.all()
        except StreamPlatform.DoesNotExist:
            return Response(
                {"Error": "StreamPlatforms not found"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = StreamPlatformSerializer(
            StreamPlatforms,
            many=True,
            # context={"request": request}
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = StreamPlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StreamPlatformDetailAV(APIView):
    def get(self, request, pk):
        try:
            streamPlatform = StreamPlatform.objects.get(pk=pk)
        except streamPlatform.DoesNotExist:
            return Response(
                {"Error": "StreamPlatform not found"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = StreamPlatformSerializer(streamPlatform)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            streamPlatform = StreamPlatform.objects.get(pk=pk)
        except streamPlatform.DoesNotExist:
            return Response(
                {"Error": "StreamPlatform not found"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = StreamPlatformSerializer(streamPlatform, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            streamPlatform = StreamPlatform.objects.get(pk=pk)
        except streamPlatform.DoesNotExist:
            return Response(
                {"Error": "StreamPlatform not found"}, status=status.HTTP_404_NOT_FOUND
            )
        streamPlatform.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class WatchListListAV(APIView):
    def get(self, request):
        try:
            WatchLists = WatchList.objects.all()
        except WatchList.DoesNotExist:
            return Response(
                {"Error": "WatchLists not found"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = WatchListSerializer(WatchLists, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WatchListDetailAV(APIView):
    def get(self, request, pk):
        try:
            watchList = WatchList.objects.get(pk=pk)
        except watchList.DoesNotExist:
            return Response(
                {"Error": "WatchList not found"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = WatchListSerializer(watchList)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            watchList = WatchList.objects.get(pk=pk)
        except watchList.DoesNotExist:
            return Response(
                {"Error": "WatchList not found"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = WatchListSerializer(watchList, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            watchList = WatchList.objects.get(pk=pk)
        except watchList.DoesNotExist:
            return Response(
                {"Error": "WatchList not found"}, status=status.HTTP_404_NOT_FOUND
            )
        watchList.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# @api_view(["GET", "POST"])
# def WatchList_list(request):
#     try:
#         WatchLists = WatchList.objects.all()
#     except WatchList.DoesNotExist:
#         return Response({"Error": "WatchLists not found"}, status=status.HTTP_404_NOT_FOUND)
#     if request.method == "GET":
#         serializer = WatchListSerializer(WatchLists, many=True)
#         return Response(serializer.data)
#     if request.method == "POST":
#         serializer = WatchListSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(["GET", "PUT", "DELETE"])
# def WatchList_details(request, pk):
#     try:
#         WatchList = WatchList.objects.get(pk=pk)
#     except WatchList.DoesNotExist:
#         return Response({"Error": "WatchList not found"}, status=status.HTTP_404_NOT_FOUND)

#     if request.method == "GET":
#         serializer = WatchListSerializer(WatchList)
#         return Response(serializer.data)
#     if request.method == "PUT":
#         serializer = WatchListSerializer(WatchList, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     if request.method == "DELETE":
#         WatchList.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
