from django.shortcuts import render

from rest_framework import viewsets
from .models import (
    CustomUser, 
    JobPosition, 
    InterviewSession, 
    InterviewQuestion,
    CandidateResponse,
    EvaluationReport
    )
from . import serializers
# Create your views here.


class CustomUserViewSet(viewsets.ModelViewSet):
    """ ViewSet for the CustomUser model. """
    serializer_class = serializers.CustomUserSerializer

    def get_queryset(self):
        """ get_queryset method to filter users based on role query parameter. """
        user = self.request.user
        if user.role == 'INTERVIEWER':
            return CustomUser.objects.filter(Q(id = user.id) | Q(created_by = user))     
        elif user.role == 'CANDIDATE':
            return CustomUser.objects.filter(id = user.id)
        else:
            return CustomUser.objects.none()  # Return an empty queryset for other roles or unauthenticated users
    def perform_create(self, serializer):
        """ Override perform_create method to set the created_by field for new users. """
        serializer.save(created_by=self.request.user)

    def List(self, request, *args, **kwargs):
        """ Override list method to filter users based on role query parameter. """
        queryset = self.get_queryset()
        role = request.query_params.get('role', None)
        if role is not None:
            queryset = queryset.filter(role=role)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self,request, id=None):
        """ Override retrieve method to get a single user by ID. """
        queryset = self.get_queryset()
        user = get_object_or_404(queryset, id=id)
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    def create(self, request, *args, kwargs):
        """ Override create method to set the created_by field for new users. """
        data=request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)



class JobPositionViewSet(viewsets.ModelViewSet):
    """ ViewSet for the JobPosition model. """
    serializer_class = serializers.JobPositionSerializer

class InterviewSessionViewSet(viewsets.ModelViewSet):
    """ ViewSet for the InterviewSession model. """
   
    serializer_class = serializers.InterviewSessionSerializer

class InterviewQuestionViewSet(viewsets.ModelViewSet):
    """ ViewSet for the InterviewQuestion model. """
    serializer_class = serializers.InterviewQuestionSerializer

class CandidateResponseViewSet(viewsets.ModelViewSet):
    """ ViewSet for the CandidateResponse model. """
    serializer_class = serializers.CandidateResponseSerializer

class EvaluationViewSet(viewsets.ModelViewSet):
    """ ViewSet for the Evaluation model. """
    serializer_class = serializers.EvaluationSerializer