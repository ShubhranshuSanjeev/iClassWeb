from django.db import models
from classroom.models import ClassRoom
from accounts.models import Teacher, Student

class Quiz(models.Model):
    classId             = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)
    title               = models.CharField(max_length=255)

    def get_absolute_url(self):
        return '/list_quiz/{0}'.format(self.classId)

class Question(models.Model):
    quizId              = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question            = models.CharField(max_length=255)

    def get_absolute_url(self):
        return '/manage_quiz/{0}'.format(self.quizId.id)

class Answer(models.Model):
    questionId          = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer              = models.CharField(max_length=255)
    is_correct          = models.BooleanField(verbose_name="Correct Answer", default=False)

    def __str__(self):
        return self.answer

class QuizSubmission(models.Model):
    studentId           = models.ForeignKey(Student, on_delete=models.CASCADE)
    quizId              = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    marks               = models.IntegerField()
    attemptTime         = models.DateTimeField(auto_now_add=True)

class StudentAnswers(models.Model):
    submissionId        = models.ForeignKey(QuizSubmission, on_delete=models.CASCADE)
    questionId          = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer              = models.ForeignKey(Answer, on_delete=models.CASCADE)       