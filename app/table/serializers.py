from rest_framework import serializers


class TableFieldSerializer(serializers.Serializer):
    type = serializers.CharField(max_length=50)
    name = serializers.CharField(max_length=100)


class TableSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    fields = serializers.ListField(
        child=TableFieldSerializer(), min_length=1, max_length=10
    )


class UpdateTableSerializer(serializers.Serializer):
    fields = serializers.ListField(
        child=TableFieldSerializer(), min_length=1, max_length=10
    )


class TableRowSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    value = serializers.CharField(max_length=100)
