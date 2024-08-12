from rest_framework import serializers

class GeminiSerializer(serializers.Serializer):
    message = serializers.CharField()
    chatHistory = serializers.ListField(
        child=serializers.DictField(), 
        required=False
    )
    image = serializers.ImageField(
        required=False, 
        allow_null=True
    )
    audio = serializers.FileField(
        required=False, 
        allow_null=True
    )
