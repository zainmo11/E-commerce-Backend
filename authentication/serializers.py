from django.contrib.auth import get_user_model
from rest_framework.schemas.coreapi import serializers
from rest_framework.validators import UniqueValidator

User = get_user_model()


# TODO: Change into a proper serializer
class CredientalsSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)


class UserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=50, required=True)
    last_name = serializers.CharField(max_length=50, required=True)
    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(User.objects.all())]
    )
    is_seller = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
            "is_seller",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def get_is_seller(self, obj):
        return obj.groups.filter(name="Sellers").exists()
