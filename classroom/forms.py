from django import forms
from . import models

class JoinClassroomForm(forms.Form):
    accessKey                       = forms.UUIDField(widget=forms.TextInput(attrs={'id':'access_key', 'name':'access_key',}))
    def clean(self):
        cleaned_data                = super().clean()
        enteredKey                  = cleaned_data.get("accessKey")
        try:
            classroom               = models.ClassRoom.objects.get(classRoomId = enteredKey)
        except models.ClassRoom.DoesNotExist:
            raise forms.ValidationError("Please enter a valid key. No such class exists!")
        return enteredKey

class NewAssignmentForm(forms.ModelForm):   
    class Meta:
        model                       = models.Assignments
        fields                      = ('description', 'maximumMarks' ,'assignmentQuestion')
        
class NewNotesForm(forms.ModelForm):
    class Meta:
        model                       = models.Notes
        fields                      = ('description', 'notesFile')

class AssignmentSubmissionForm(forms.ModelForm):
    class Meta:
        model                       = models.StudentAssignmentSubmission
        fields                      = ('submissionFile', 'assignmentId', )

class UpdateMarksForm(forms.ModelForm):
    class Meta:
        model                       = models.StudentAssignmentSubmission
        fields                      = ('marks', )
    
    def clean_marks(self, invalid=False):
        marks                       = self.cleaned_data.get('marks')
        if marks > self.instance.assignmentId.maximumMarks: 
            raise forms.ValidationError('Scored Marks cannot be greater than Maximum Marks({0})'.format(self.instance.assignmentId.maximumMarks))
        return marks