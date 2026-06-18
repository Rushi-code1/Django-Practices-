from rest_framework import serializers
from .models import CustomUser, JobPosition, InterviewSession, InterviewQuestion, CandidateResponse,EvaluationReport


class CustomUserSerializer(serializers.ModelSerializer):
    """ Serializer for the CustomUser model. """
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'last_name', 'role', 'department', 'date_joined']

class JobPositionSerializer(serializers.ModelSerializer):
    """ Serializer for the JobPosition model. """
    created_by = CustomUserSerializer(read_only=True)
    class Meta:
        model = JobPosition
        fields = ['id', 'title', 'description', 'created_at', 'created_by']

class InterviewSessionSerializer(serializers.ModelSerializer):
    """ Serializer for the InterviewSession model. """
    job_position = JobPositionSerializer(read_only=True)
    interviewer = CustomUserSerializer(read_only=True)
    candidate = CustomUserSerializer(read_only=True)

    class Meta:
        model = InterviewSession
        fields = ['id', 'job_position', 'interviewer', 'candidate', 'scheduled_at', 'duration_minutes', 'google_meet_url']

class InterviewQuestionSerializer(serializers.ModelSerializer):
    """ Serializer for the InterviewQuestion model. """
    session = InterviewSessionSerializer(read_only=True)

    class Meta:
        model = InterviewQuestion
        fields = ['id', 'session', 'question_text', 'difficulty_level', 'created_at']

class CandidateResponseSerializer(serializers.ModelSerializer):
    """ Serializer for the CandidateResponse model. """
    question = InterviewQuestionSerializer(read_only=True)

    class Meta:
        model = CandidateResponse
        fields = ['id', 'question', 'response_text', 'created_at']

class EvaluationSerializer(serializers.ModelSerializer):
    """ Serializer for the Evaluation model. """
    session = InterviewSessionSerializer(read_only=True)

    class Meta:
        model = EvaluationReport
        fields = ['id', 'session', 'score', 'feedback', 'created_at']   