from django import forms
from pybo.models import Question

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['subject', 'content']
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.textarea(attrs={'class': 'form-control', 'rows': 10}),
        }
        labels = {
            'subject': '제목',
            'content': '내용',
        }