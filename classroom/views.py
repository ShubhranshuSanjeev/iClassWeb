import uuid
from django.shortcuts import redirect
from django.views.generic import TemplateView, CreateView, ListView, FormView, UpdateView
from . import models, forms
from accounts.models import Teacher, Student, User

class TeacherDashboard(TemplateView):
    template_name                                   = 'classroom/teacherDashboard.html'

class StudentDashboard(TemplateView):
    template_name                                   = 'classroom/studentDashboard.html'

class Dashboard(TemplateView):
    def get(self, request, *args, **kwargs):
        if request.user.is_teacher:
            view                                    = TeacherDashboard.as_view()
        else:
            view                                    = StudentDashboard.as_view()
        return view(request, *args, **kwargs)

class CreateClassRoom(CreateView):
    model                                           = models.ClassRoom
    fields                                          = ['roomNumber', 'courseName']
    template_name                                   = 'classroom/class_creation_form.html'
    success_url                                     = '/teacher_dashboard/'

    def form_valid(self, form):
        form.instance.teacherId                     = Teacher.objects.get(username = self.request.user.username)
        form.instance.classRoomId                   = uuid.uuid4()
        return super().form_valid(form)

class JoinClassRoom(FormView):
    template_name                                   = 'classroom/join_class_form.html'
    form_class                                      = forms.JoinClassroomForm
    success_url                                     = '/student_dashboard/'

    def form_valid(self, form):
        data                                        = form.cleaned_data
        classroom                                   = models.ClassRoom.objects.get(classRoomId = data)
        student                                     = Student.objects.get(username = self.request.user)
        classroom.studentId.add(student)
        classroom.save()
        return super().form_valid(form)

class ListClassRooms(ListView):
    model                                           = models.ClassRoom

    def get_queryset(self):
        if self.request.user.is_teacher:
            return models.ClassRoom.objects.filter(teacherId = Teacher.objects.get(username = self.request.user)).values('courseName','classRoomId')
        else:
            return models.ClassRoom.objects.filter(studentId = Student.objects.get(username = self.request.user)).values('courseName','classRoomId')

class ClassRoomDetailsTeacher(TemplateView):
    template_name = 'classroom/classroom_detail_teacher.html'

    def get_context_data(self, **kwargs):
        assignments                                 = models.Assignments.objects.filter(classId = self.kwargs['pk'])
        notes                                       = models.Notes.objects.filter(classId = self.kwargs['pk'])
        data                                        = models.ClassRoom.objects.filter(classRoomId = self.kwargs['pk']).values('studentId', 'courseName', 'roomNumber', 'classRoomId')      
        context                                     = super(ClassRoomDetailsTeacher, self).get_context_data(**kwargs)
        
        context['studentNames'] = []
        numberOfStudents = 0
        for i in data:
            if User.objects.filter(username = i['studentId']):
                student                             = User.objects.filter(username = i['studentId']).values('first_name', 'last_name', 'email')
                context['studentNames'].append(student)
                numberOfStudents                    += 1
        
        context['assignment_form']                  = forms.NewAssignmentForm()
        context['notes_form']                       = forms.NewNotesForm()        
        context['assignments']                      = assignments
        context['notes']                            = notes
        context['courseName']                       = data[0]['courseName']
        context['roomNumber']                       = data[0]['roomNumber']
        context['classRoomId']                      = data[0]['classRoomId']
        context['numberOfStudent']                  = numberOfStudents        
        
        return context

class ClassRoomDetailsStudent(TemplateView):
    model                                           = models.ClassRoom
    template_name                                   = 'classroom/classroom_detail_student.html' 

    def get_context_data(self, **kwargs):
        assignments                                 = models.Assignments.objects.filter(classId = self.kwargs['pk'])
        notes                                       = models.Notes.objects.filter(classId = self.kwargs['pk'])
        data                                        = models.ClassRoom.objects.filter(classRoomId = self.kwargs['pk']).values('teacherId', 'courseName', 'roomNumber')[0]
        teacherName                                 = User.objects.filter(username = data['teacherId']).values('first_name', 'last_name')[0]
        context                                     = super(ClassRoomDetailsStudent, self).get_context_data(**kwargs)

        context['assignments']                      = assignments
        context['notes']                            = notes
        context['assignmentSubmissionForm']         = forms.AssignmentSubmissionForm()
        context['courseName']                       = data['courseName']
        context['roomNumber']                       = data['roomNumber']
        context['teacherName']                      = teacherName['first_name'] + ' ' + teacherName['last_name']
        
        return context

class NewAssignmentView(CreateView):
    model                                           = models.Assignments
    form_class                                      = forms.NewAssignmentForm
    template_name                                   =  'classroom/classroom_detail_teacher.html'

    def form_valid(self, form):
        form.instance.classId                       = models.ClassRoom.objects.filter(classRoomId = self.kwargs['pk'])[0]
        return super().form_valid(form)

class NewNotesView(CreateView):
    model                                           = models.Notes
    form_class                                      = forms.NewNotesForm
    template_name                                   = 'classroom/classroom_detail_teacher.html'

    def form_valid(self, form):
        form.instance.classId                       = models.ClassRoom.objects.filter(classRoomId = self.kwargs['pk'])[0]
        return super().form_valid(form)

class AssignmentSubmissionView(CreateView):
    model                                           = models.StudentAssignmentSubmission
    form_class                                      = forms.AssignmentSubmissionForm
    template_name                                   = 'classroom/classroom_detail_student.html'

    def form_valid(self, form):
        assignment                                  = form.save(commit=False)
        try:
            students                                = [data['studentId'] for data in models.StudentAssignmentSubmission.objects.filter(assignmentId = assignment.assignmentId).values('studentId')]
            if self.request.user.username in students:
                entry                               = models.StudentAssignmentSubmission.objects.get(studentId = self.request.user.username)
                entry.submissionFile                = assignment.submissionFile
                entry.save()
            else:
                raise
        except:
            form.instance.studentId                     = models.Student.objects.get(username = self.request.user)
            form.instance.marks                         = 0
            form.save()

class ClassRoomDetails(TemplateView):
    def get(self, request, *args, **kwargs):
        if request.user.is_teacher:
            view                                    = ClassRoomDetailsTeacher.as_view()
        else:
            view                                    = ClassRoomDetailsStudent.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if 'assignment' in request.POST:
            view                                    = NewAssignmentView.as_view()
        if 'notes' in request.POST:
            view                                    = NewNotesView.as_view()
        if 'uploadButton' in request.POST:
            view                                    = ClassRoomDetailsStudent.as_view()
        if 'assignmentSubmission' in request.POST:
            view                                    = AssignmentSubmissionView.as_view()
        view(request, *args, **kwargs)
        return redirect('/view_classrooms/{0}'.format(kwargs['pk']))

class UpdateMarksView(UpdateView):
    model                                           = models.StudentAssignmentSubmission
    template_name                                   = 'classroom/marksupdateform.html'
    form_class                                      = forms.UpdateMarksForm
    
    def get_object(self):
        return models.StudentAssignmentSubmission.objects.get(id = self.kwargs['pk'])

class ListAssignmentSubmissions(ListView):
    model                                           = models.StudentAssignmentSubmission
    template_name                                   = 'classroom/studentassignmentsubmission_list.html'
    
    def get_context_data(self, **kwargs):
        context                                     = super(ListAssignmentSubmissions, self).get_context_data(**kwargs)
        assignmentInstance                          = models.Assignments.objects.get(id = self.kwargs['pk'])
        numberOfSubmissions                         = len(models.StudentAssignmentSubmission.objects.filter(assignmentId = self.kwargs['pk']).values('studentId'))

        context['assignmentName']                   = assignmentInstance.description
        context['maximumMarks']                     = assignmentInstance.maximumMarks
        context['courseName']                       = assignmentInstance.classId.courseName
        context['numberOfStudents']                 = len(assignmentInstance.classId.studentId.all())
        context['numberOfSubmissions']              = numberOfSubmissions
        return context

    def get_queryset(self):
        return models.StudentAssignmentSubmission.objects.filter(assignmentId = self.kwargs['pk'])
