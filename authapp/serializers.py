from rest_framework import serializers
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name','last_name','email','password','profile_picture','role','phone_number','address']
        extra_kwargs ={
            'password':{'write_only':True}
        }

    def create(self, validated_data):
        user = self.Meta.model.objects.create_user(**validated_data)
        print("USER CREATED:", user)
        return user
        