from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib import messages
from django.db import transaction
from . import models, forms
from classroom.models import ClassRoom
from accounts.models import Student
from django.views.generic import ListView, CreateView, UpdateView, TemplateView

class CreateQuiz(CreateView):
    model                   = models.Quiz
    form_class              = forms.CreateQuizForm

    def form_valid(self, form):
        form.instance.classId = ClassRoom.objects.filter(classRoomId = self.kwargs['pk'])[0]
        return super().form_valid(form)

class ListQuiz(ListView):
    model                   = models.Quiz
    template_name           = 'quiz/quiz_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = forms.CreateQuizForm()
        return context

    def get_queryset(self):
        return models.Quiz.objects.filter(classId = self.kwargs['pk'])

class QuizView(TemplateView):
    def get(self, request, *args, **kwargs):
        view            = ListQuiz.as_view()
        return view(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        view        = CreateQuiz.as_view()
        view(request, *args, **kwargs)
        return redirect('/list_quiz/{0}'.format(kwargs['pk']))

class ManageQuiz(UpdateView):
    model = models.Quiz
    fields = ['title', ]
    template_name = 'quiz/manage_quiz.html'

    def get_success_url(self):
        return '/manage_quiz/{0}'.format(self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['questions'] = models.Question.objects.filter(quizId = self.kwargs['pk'])
        return context

    def get_object(self):
        return self.model.objects.get(id = self.kwargs['pk'])

class AddQuestion(CreateView):
    model                   = models.Question
    form_class = forms.QuestionForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['quizTitle'] = models.Quiz.objects.get(id = self.kwargs['pk']).title
        return context

    def form_valid(self, form):
        form.save(commit = False)
        form.instance.quizId = models.Quiz.objects.get(id = self.kwargs['pk'])
        form.save()
        return redirect('/manage_questions/{0}/{1}'.format(self.kwargs['pk'], form.instance.id))

class ManageQuestion(TemplateView):
    template_name = 'quiz/answer_form.html'

    def post(self, request, *args, **kwargs):
        question = get_object_or_404(models.Question, pk=kwargs['pk'], quizId=kwargs['quiz_pk'])
        quiz = get_object_or_404(models.Quiz, pk=kwargs['quiz_pk'])
        form = forms.QuestionForm(request.POST, instance=question)
        formset = forms.AnswerFormSet(request.POST, instance=question)
        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                form.save()
                formset.save()
            messages.success(request, 'Question and answers saved successfully!')
            return redirect('/manage_quiz/{0}'.format(kwargs['quiz_pk']))
        return render(request, 'quiz/answer_form.html')

    def get_context_data(self, **kwargs):
        question = get_object_or_404(models.Question, pk=kwargs['pk'], quizId=kwargs['quiz_pk'])
        print(question)
        context = super().get_context_data(**kwargs) 
        context['question'] = question.question
        context['form'] = forms.QuestionForm(instance=question)
        context['formset'] = forms.AnswerFormSet(instance=question)  
        return context

class QuizEntryView(CreateView):
    model = models.QuizSubmission
    template_name = 'quiz/attempt_quiz.html'
    fields = []

    def form_valid(self, form):
        form.save(commit = False)
        form.instance.marks = 0
        form.instance.studentId = Student.objects.get(username = self.request.user.username)
        form.instance.quizId = models.Quiz.objects.get(id = self.kwargs['pk'])
        form.save()
        x =  models.Question.objects.filter(quizId = self.kwargs['pk']).values('id')[0]['id']
        print(x)
        return redirect('/quiz/{0}/{1}/{2}'.format(self.kwargs['pk'], form.instance.id, x))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['quiz'] = models.Quiz.objects.get(id = self.kwargs['pk']).title
        return context         

class AttemptQuiz(TemplateView):
    model = models.StudentAnswers
    template_name = 'quiz/question_display.html'

    def post(self, request, *args, **kwargs):
        if 'get_question' in request.POST:
            return redirect('/quiz/{0}/{1}/{2}'.format(self.kwargs['quiz_id'], self.kwargs['pk'], request.POST['get_question']))
        else:
            update = 0
            studentAnswerId = ''
            form = forms.AttemptQuizForm(question = models.Question.objects.get(id = self.kwargs['question_no']), data=request.POST)
            if form.is_valid():
                with transaction.atomic():
                    update_check = models.StudentAnswers.objects.filter(submissionId = self.kwargs['pk'])
                    for x in update_check:
                        print(self.kwargs['question_no'], x.questionId.id)
                        if int(self.kwargs['question_no']) == x.questionId.id:
                            update = 1
                            studentAnswerId = x.id
                            break  
                    if not update:
                        student_answer = form.save(commit = False)
                        student_answer.submissionId = models.QuizSubmission.objects.get(id = self.kwargs['pk'])
                        student_answer.questionId = models.Question.objects.get(id = self.kwargs['question_no'])
                        student_answer.save()
                    else:
                        inst = models.StudentAnswers.objects.get(id = studentAnswerId)
                        inst.answer = form.instance.answer
                        inst.save(update_fields=['answer'])
            else:
                print(form.errors)
            next_question = self.get_unanswered_questions(**kwargs).id
            return redirect('/quiz/{0}/{1}/{2}'.format(self.kwargs['quiz_id'], self.kwargs['pk'], next_question))

    def get_unanswered_questions(self, **kwargs):
        questions_answered = [ans['questionId']  for ans in models.StudentAnswers.objects.filter(submissionId = self.kwargs['pk']).values('questionId')]
        questions_unanswered = models.Question.objects.filter(quizId = self.kwargs['quiz_id']).exclude(id__in=questions_answered)
        return questions_unanswered[0]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        unanswered_question = models.Question.objects.get(id = self.kwargs['question_no']) 
        questions = models.Question.objects.filter(quizId = self.kwargs['quiz_id']).values('id')
        context['questions'] = []
        i = 1
        for question in questions:
            context['questions'].append((question['id'], i))
            i += 1
        context['question'] = unanswered_question.question
        context['form'] = forms.AttemptQuizForm(question = unanswered_question)
        return context
