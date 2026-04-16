from rest_framework import serializers
from .models import About
class AboutSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = About
        fields = "__all__"

    def get_image(self, obj):
        if obj.image:
            return obj.image.url
        return None

    def update(self, instance, validated_data):
        image = self.context['request'].FILES.get('image', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if image:
            instance.image = image  #  IMPORTANT for Cloudinary

        instance.save()
        return instance