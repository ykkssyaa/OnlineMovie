from django import forms

from reviews.models import Review, Mark


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['text']
        labels = {
            'text': 'Текст рецензии'
        }
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4})
        }


class MarkForm(forms.ModelForm):
    value = forms.ChoiceField(label='Оценка', choices=[(str(i), str(i)) for i in range(1, 6)])

    class Meta:
        model = Mark
        fields = ('value',)
