from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'name', 'gender', 'age', 'introduction']
        
    def create(self, validated_data):
        user = super().create(validated_data) # DB에 저장
        password = user.password
        user.set_password(password) # 비밀번호 암호화 해싱해주는 함수
        user.save() # 해쉬된 내용을 다시 DB에 저장
        return user

    def update(self, instance, validated_data):
        validated_data.pop('email', None)  # email 필드가 수정되지 않도록 함
        user = super().update(instance, validated_data)
        password = user.password
        user.set_password(password)
        user.save()
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['name'] = user.name
        token['gender'] = user.gender
        token['age'] = user.age

        return token
