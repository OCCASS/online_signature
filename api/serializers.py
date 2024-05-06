from rest_framework import serializers


class DocumentSerializer(serializers.Serializer):
    html = serializers.CharField()
    name = serializers.CharField()


class SendSMSSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    document = DocumentSerializer()
