from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class CustomUser(AbstractUser):
    """ Model representing a custom user. """
    ROLE_CHOICES = (
        ("INTERVIEWER", "Interviewer"),
        ("CANDIDATE", "Candidate"),
    )

    email = models.EmailField(max_length=254, unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    department = models.CharField(max_length=100, blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='created_users')

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.role})"


class JobPosition(models.Model):
    """ Model representing a job position. """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100, help_text="Enter the job title")
    description = models.TextField(help_text="Enter the job description")
    created_at = models.DateTimeField(auto_now_add=True, help_text="The date and time when the job position was created")
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, help_text="The user who created the job position")

    def __str__(self):
        return self.title


class InterviewSession(models.Model):
    """ Model representing an interview session. """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    job_position = models.ForeignKey(JobPosition, on_delete=models.CASCADE, help_text="The job position for which the interview session is scheduled")
    interviewer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='interviewer_sessions', limit_choices_to={'role': 'INTERVIEWER'}, help_text="The interviewer conducting the session")
    candidate = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='candidate_sessions', limit_choices_to={'role': 'CANDIDATE'}, help_text="The candidate attending the session")
    scheduled_at = models.DateTimeField(help_text="The date and time when the interview session is scheduled")
    duration_minutes = models.PositiveIntegerField(help_text="The duration of the interview session in minutes")
    google_meet_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"Interview Session for {self.job_position.title} with {self.candidate} scheduled at {self.scheduled_at}"


class InterviewQuestion(models.Model):
    """ Model representing an interview question. """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session = models.ForeignKey(InterviewSession, on_delete=models.CASCADE, related_name='questions', help_text="The interview session to which the question belongs")
    question_text = models.TextField(help_text="The text of the interview question")
    difficulty_level = models.CharField(max_length=50, help_text="The difficulty level of the question (e.g., Easy, Medium, Hard)")
    created_at = models.DateTimeField(auto_now_add=True, help_text="The date and time when the question was created")

    def __str__(self):
        return f"Question for {self.session.job_position.title}: {self.question_text[:50]}..."


class CandidateResponse(models.Model):
    """ Model representing a candidate's response to an interview question. """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # Pro Tip: Django uses the actual object name for fields, naming fields with '_id' explicitly can cause confusion.
    session = models.ForeignKey(InterviewSession, on_delete=models.CASCADE, related_name='responses', help_text="The interview session to which the response belongs")
    question = models.ForeignKey(InterviewQuestion, on_delete=models.CASCADE, related_name='responses', help_text="The interview question to which the response belongs")
    transcript = models.TextField(help_text="The transcript of the candidate's response")
    sentiment_score = models.FloatField(help_text="The sentiment score of the candidate's response")
    is_correct = models.BooleanField(help_text="Indicates whether the candidate's response is correct")
    submitted_at = models.DateTimeField(auto_now_add=True, help_text="The date and time when the response was submitted")

    def __str__(self):
        return f"Response to '{self.question.question_text[:20]}...' by {self.session.candidate}"


class EvaluationReport(models.Model):
    """ Model representing an evaluation report for a candidate's performance in an interview session. """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    interview_session = models.OneToOneField(InterviewSession, on_delete=models.CASCADE, related_name='evaluation_report', help_text="The interview session for which the evaluation report is generated")
    transcript = models.TextField(help_text="The transcript of the candidate's responses during the interview session")
    sentiment_score = models.FloatField(help_text="The overall sentiment score of the candidate's responses")
    communication_score = models.FloatField(help_text="The communication score of the candidate's responses")
    problem_solving_score = models.FloatField(help_text="The problem-solving score of the candidate's responses")
    technical_knowledge_score = models.FloatField(help_text="The technical knowledge score of the candidate's responses")

    def __str__(self):
        return f"Evaluation Report for Session: {self.interview_session.id}"