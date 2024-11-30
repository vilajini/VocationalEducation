from django.db import models

# Create your models here.
from django.db import models

class Users(models.Model):
    user_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.CharField(unique=True, max_length=255)
    role = models.CharField(max_length=50)
    language = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField()

    class Meta:
        db_table = 'users'


class Questions(models.Model):
    content = models.TextField()  # Question content
    difficulty_level = models.CharField(max_length=50, choices=[
        ('easy', 'Basic'),
        ('medium', 'Intermediate'),
        ('hard', 'Advanced')
    ])
    topic = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'questions'



class VivaSessions(models.Model):
    session_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=50)
    score = models.FloatField(blank=True, null=True)

    class Meta:
        db_table = 'viva_sessions'


class Responses(models.Model):
    response_id = models.AutoField(primary_key=True)
    session = models.ForeignKey(VivaSessions, on_delete=models.CASCADE)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    question = models.ForeignKey(Questions, on_delete=models.CASCADE)
    response_text = models.TextField(blank=True, null=True)
    is_correct = models.BooleanField(blank=True, null=True)
    confidence_score = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField()

    class Meta:
        db_table = 'responses'


class Feedback(models.Model):
    feedback_id = models.AutoField(primary_key=True)
    response = models.ForeignKey(Responses, on_delete=models.CASCADE)
    feedback_text = models.TextField()
    suggested_question = models.ForeignKey(Questions, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField()

    class Meta:
        db_table = 'feedback'

