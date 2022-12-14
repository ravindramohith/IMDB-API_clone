from rest_framework import serializers
from watchlist_app.models import WatchList, StreamPlatform, Review


class ReviewSerializer(serializers.ModelSerializer):
    reviewed_user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        # fields = "__all__"
        exclude = ["watchlist"]


class WatchListSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = WatchList
        fields = "__all__"
        # fields = ["name", "description"]
        # exclude = ["active"]

    def validate(self, data):
        if len(str(data["name"])) < 4:
            raise serializers.ValidationError("Name is too short")
        if data["description"] == data["name"]:
            raise serializers.ValidationError("Description should'nt be equal to name")
        return data


class StreamPlatformSerializer(serializers.ModelSerializer):
    watchlist = WatchListSerializer(many=True, read_only=True)
    # watchlist = serializers.HyperlinkedRelatedField(
    #     many=True, read_only=True, view_name="watchlist-details"
    # )

    class Meta:
        model = StreamPlatform
        fields = "__all__"


# class WatchListSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField()
#     description = serializers.CharField()
#     active = serializers.BooleanField()

#     def create(self, validated_data):
#         return WatchList.objects.create(**validated_data)

#     def update(self, instance, validated_data):
#         instance.name = validated_data.get("name", instance.name)
#         instance.active = validated_data.get("active", instance.active)
#         instance.description = validated_data.get("description", instance.description)
#         instance.save()
#         return instance
