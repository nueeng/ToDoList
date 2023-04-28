from rest_framework import status
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from users.models import User
from users.serializers import UserSerializer
from users.serializers import UserSerializer, CustomTokenObtainPairSerializer


class UserView(APIView):
    def post(self, request):
        '''회원가입'''
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"회원가입이 완료되었습니다."}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message":f"{serializer.errors}"}, status=status.HTTP_400_BAD_REQUEST)


class UserUpdateView(APIView):
    def patch(self, request, user_id):
        '''회원정보 수정'''
        user = get_object_or_404(User, id=user_id)
        if request.user == user:
            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"message":"회원정보가 수정되었습니다."}, status=status.HTTP_200_OK)
            else:
                return Response({"message":f"{serializer.errors}"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("권한이 없습니다.", status=status.HTTP_403_FORBIDDEN)
        
    def delete(self, request, user_id):
        '''회원탈퇴'''
        user = get_object_or_404(User, id=user_id)
        if request.user == user:
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("권한이 없습니다.", status=status.HTTP_403_FORBIDDEN)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
