from django import forms
from django.forms import BaseInlineFormSet, inlineformset_factory

from .models import Choice, Exam, Question


class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ["title", "description"]


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ["text"]
        widgets = {
            "text": forms.Textarea(
                attrs={"placeholder": "Escribe el enunciado de la pregunta"}
            ),
        }


class BaseChoiceFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()

        if any(self.errors):
            return

        correct_choices = 0

        for form in self.forms:
            if not form.cleaned_data:
                continue

            if form.cleaned_data.get("DELETE"):
                continue

            if form.cleaned_data.get("is_correct"):
                correct_choices += 1

        if correct_choices != 1:
            raise forms.ValidationError(
                "Debes marcar exactamente una alternativa como correcta."
            )


ChoiceFormSet = inlineformset_factory(
    Question,
    Choice,
    fields=["text", "is_correct"],
    widgets={
        "text": forms.TextInput(
            attrs={"placeholder": "Escribe una alternativa"}
        ),
        "is_correct": forms.CheckboxInput(
            attrs={"aria-label": "Marcar como respuesta correcta"}
        ),
    },
    formset=BaseChoiceFormSet,
    extra=4,
    can_delete=True,
)
