from cmath import exp
from http.client import NOT_FOUND
from django.shortcuts import render
from rest_framework import generics
from todos import models
from .serializers import TodoSerializer, TagSerializer
from rest_framework import filters
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import logout

# Create your views here.


class BasicAuthAPIView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        content = {
            'user': str(request.user),
            'auth': str(request.auth),
        }
        return Response(content)


class UserFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(user=request.user)


class ListTag(generics.ListCreateAPIView):
    serializer_class = TagSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = models.Tag.objects.all()

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class DetailTag(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TagSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = models.Tag.objects.all()

    # Validate the todos are created by login user only
    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class ListTodo(generics.ListCreateAPIView):
    serializer_class = TodoSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = models.Todo.objects.all()
    filter_backends = [UserFilterBackend]

    # Validate the todos are created by login user only
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DetailTodo(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TodoSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = models.Todo.objects.all()
    filter_backends = [UserFilterBackend]

    # Validate the todos are created by login user only
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
