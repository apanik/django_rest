from rest_framework import serializers
from .models import User,Permissons,Role


        
class PermissonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permissons
        fields = "__all__"

class PermissonRelatedSerializer(serializers.StringRelatedField):
    def to_representation(self,value):
        return PermissonSerializer(value).data
    def to_internal_value(self,data):
        return data
        
class RolesSerializer(serializers.ModelSerializer):
    permissons = PermissonRelatedSerializer(many=True)
    class Meta:
        model = Role
        fields = "__all__"
        
    def create(self,validated_data):
        permissons = validated_data.pop('permissons',None)
        instance = self.Meta.model(**validated_data)
        instance.save()
        instance.permissons.add(*permissons)
        instance.save()
        return instance
       
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username","first_name","last_name","email","password"]
        extra_kwargs = {
            "password":{"write_only":True}
        }

    def create(self,validated_data):
        password = validated_data.pop('password',None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
            instance.save()
            return instance
