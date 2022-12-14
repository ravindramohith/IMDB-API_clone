from django.urls import path, include
from rest_framework.routers import DefaultRouter
from watchlist_app.api.views import (
    WatchListListAV,
    WatchListDetailAV,
    StreamPlatformListAV,     
    StreamPlatformDetailAV,
    ReviewListGV,
    ReviewDetailGV,
    ReviewCreateGV,
    StreamPlatformVS,
)

StreamPlatformRouter = DefaultRouter()
StreamPlatformRouter.register("platform", StreamPlatformVS, basename="streamplatform")

urlpatterns = [
    path("list", WatchListListAV.as_view(), name="watchlist-list"),
    path("<int:pk>", WatchListDetailAV.as_view(), name="watchlist-details"),
    path("", include(StreamPlatformRouter.urls)),
    # path("platforms", StreamPlatformListAV.as_view(), name="stream-platform-list"),
    # path(
    #     "platform/<int:pk>",
    #     StreamPlatformDetailAV.as_view(),
    #     name="stream-platform-details",
    # ),
    path(
        "stream/<int:pk>/review-create", ReviewCreateGV.as_view(), name="review-create"
    ),
    path("stream/<int:pk>/reviews", ReviewListGV.as_view(), name="reviews"),
    path("stream/reviews/<int:pk>", ReviewDetailGV.as_view(), name="review-detail"),
]
