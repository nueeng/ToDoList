from rest_framework import status
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from todo.models import Todo
from todo.serializers import TodoSerializer, TodoCreateSerializer, TodoListSerializer


class TodoView(APIView):
    def get(self, request):
        '''해야할 일 조회 함수'''
        todo = Todo.objects.all()
        serializer = TodoListSerializer(todo, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        '''해야할 일 작성 함수'''
        serializer = TodoCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user) # 유저정보 입력
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TodoUpdateView(APIView):
    def patch(self, request, todo_id):
        '''해야할 일 수정 함수'''
        todo = get_object_or_404(Todo, id=todo_id)
        if request.user == todo.user:
            serializer = TodoCreateSerializer(todo, data=request.data)
            if serializer.is_valid():
                serializer.save() # 여기는 유저정보 todo정보에 이미 저장되어있어서 안넣어줘도 됨
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response("권한이 없습니다!", status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, todo_id):
        '''해야할 일 삭제 함수'''
        todo = get_object_or_404(Todo, id=todo_id)
        if request.user == todo.user:
            todo.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("권한이 없습니다!", status=status.HTTP_403_FORBIDDEN)
