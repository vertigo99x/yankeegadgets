from rest_framework import serializers

from .models import Category, Products, AdBanner, CartList


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Products
        fields = (
            "id",
            "name",
            "price",
            "previous_price",
            "description",
            "get_absolute_url",
            "rating",
            "get_image",
            "get_image_list",
            "get_thumbnail",
        )


class AdBannerSerializer(serializers.Serializer):
    class Meta:
        model = AdBanner
        fields = (
            "offer_event",
            "product_name",
            "starting_price",
            "get_thumbnail",
            )