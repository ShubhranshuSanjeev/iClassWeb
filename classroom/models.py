import uuid
from django.db import models
from accounts.models import Teacher, Student

class ClassRoom(models.Model):
    classRoomId             = models.UUIDField(primary_key=True, editable = False)
    roomNumber              = models.IntegerField()
    courseName              = models.CharField(verbose_name='Course Name', max_length = 50)
    teacherId               = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    studentId               = models.ManyToManyField(Student)

class Assignments(models.Model):
    classId                 = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)
    description             = models.CharField(verbose_name='Description', max_length = 75, null=True)
    assignmentQuestion      = models.FileField(upload_to='uploads/', null=True)
    maximumMarks            = models.IntegerField(default=0)
    
    def get_absolute_url(self):
        return '/view_classroom/{0}'.format(self.classId)

class Notes(models.Model):
    classId                 = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)
    description             = models.CharField(max_length = 100)
    notesFile               = models.FileField(upload_to='uploads/', null=True)

    def get_absolute_url(self):
        return '/view_classroom/{0}'.format(self.classId)

class StudentAssignmentSubmission(models.Model):
    assignmentId            = models.ForeignKey(Assignments, on_delete=models.CASCADE)
    studentId               = models.ForeignKey(Student, on_delete=models.CASCADE)
    submissionFile          = models.FileField(upload_to='uploads/')
    marks                   = models.PositiveIntegerField()

    def get_absolute_url(self):
        return '/list_submissions/{0}'.format(self.assignmentId.id)