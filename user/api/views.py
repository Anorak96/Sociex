from user.models import User
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from django.http import Http404
from user.api import serializers
from .permissions import IsUserWriteOnly
from rest_framework.filters import SearchFilter
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

class UserView(APIView):
    """User Detail"""
    serializer_class = serializers.UserSerializer

    def get(self, request):
        user = get_object_or_404(User, pk=self.request.user)
        serializer = serializers.UserSerializer(user)
        return Response(serializer.data)

    def delete(self, request, pk, *args, **kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if not request.user == user:
            raise PermissionDenied("You can not delete this user. You must be the Owner")
        return super().delete(request, *args, **kwargs) # type:ignore

    def put(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        serializer = serializers.UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserDetail(APIView):
    """User Detail"""
    serializer_class = serializers.UserSerializer
    # pagination_class = PageNumberPagination

    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        serializer = serializers.UserSerializer(user)
        return Response(serializer.data)

    def delete(self, request, pk, *args, **kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if not request.user == user:
            raise PermissionDenied("You can not delete this user. You must be the Owner")
        return super().delete(request, *args, **kwargs) # type:ignore

    def put(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        serializer = serializers.UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegistrationApiView(generics.CreateAPIView):
    permission_classes = ()
    authentication_classes = ()
    serializer_class = serializers.UserCreateSerializer

class UpdateUserView(APIView):
    permission_classes = [IsUserWriteOnly] # Custom permission class used
    serializer_class = serializers.UpdateUserSerializer

    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        serializer = serializers.UpdateUserSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk, *args, **kwargs):
        user = self.get_object(pk) # type:ignore
        serializer = serializers.UpdateUserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteUserView(generics.DestroyAPIView):
    queryset = User.objects.all()
    lookup_field = 'pk'

    def delete(self, request, *args, **kwargs):
        user_pk = request.data.get('pk')
        response = super().delete(request, *args, **kwargs)
        