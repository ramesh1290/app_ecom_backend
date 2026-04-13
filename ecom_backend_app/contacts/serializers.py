from rest_framework import serializers

from .models import Contact
class ContactSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    subject = serializers.CharField(max_length=200)
    message = serializers.CharField()
    def create(self, validated_data):
        return Contact.objects.create(first_name=validated_data['first_name'],
                                      last_name=validated_data['last_name'],
                                      email=validated_data['email'], 
                                      subject=validated_data['subject'],
                                      message=validated_data['message']
                                      )