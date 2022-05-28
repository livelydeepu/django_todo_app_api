from cmath import exp
from django.shortcuts import render
from rest_framework import generics
from todos import models
from .serializers import TodoSerializer
from rest_framework import filters

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


class ListTodo(generics.ListCreateAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = models.Todo.objects.all()
    serializer_class = TodoSerializer
    filter_backends = [UserFilterBackend]

    # Validate the todos are created by login user only
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DetailTodo(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = models.Todo.objects.all()
    serializer_class = TodoSerializer
    filter_backends = [UserFilterBackend]

    # Validate the todos are created by login user only
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
