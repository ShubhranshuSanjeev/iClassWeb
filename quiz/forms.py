from django import forms
from . import models

class CreateQuizForm(forms.ModelForm):
    class Meta:
        model       = models.Quiz
        fields      = ('title', )

class QuestionForm(forms.ModelForm):
    class Meta:
        model = models.Question
        fields = ('question', )

class AnswerInlineFormset(forms.BaseInlineFormSet):
    def clean(self):
        super().clean()

        has_one_correct_answer = False
        for form in self.forms:
            if not form.cleaned_data.get('DELETE', False):
                if form.cleaned_data.get('is_correct', False):
                    has_one_correct_answer = True
                    break
        if not has_one_correct_answer:
            raise forms.ValidationError('Mark at least one answer as correct.', code='no_answer_correct')

AnswerFormSet = forms.inlineformset_factory(
    models.Question,
    models.Answer,
    formset=AnswerInlineFormset,
    fields=('answer', 'is_correct'),
    min_num=2,
    validate_min=True,
    max_num=10,
    validate_max=True
)

class AttemptQuizForm(forms.ModelForm):
    answer = forms.ModelChoiceField(
        queryset=models.Answer.objects.none(), 
        widget=forms.RadioSelect(), 
        required=True,
        empty_label=None)
    
    class Meta:
        model = models.StudentAnswers
        fields = ('answer', )

    def  __init__(self, *args, **kwargs):
        question = kwargs.pop('question')
        super().__init__(*args, **kwargs)
        self.fields['answer'].queryset = models.Answer.objects.filter(questionId = question.id)
