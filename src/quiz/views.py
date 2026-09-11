from django.shortcuts import get_object_or_404, redirect, render

from .forms import ChoiceFormSet, QuestionForm
from .models import Exam


def exam_list(request):
    exams = Exam.objects.all()

    return render(
        request,
        "quiz/exam_list.html",
        {"exams": exams},
    )


def exam_detail(request, pk):
    exam = get_object_or_404(
        Exam.objects.prefetch_related("questions__choices"),
        pk=pk,
    )

    return render(
        request,
        "quiz/exam_detail.html",
        {"exam": exam},
    )


def question_create(request, exam_id):
    exam = get_object_or_404(Exam, pk=exam_id)

    if request.method == "POST":
        question_form = QuestionForm(request.POST)
        formset = ChoiceFormSet(request.POST)

        if question_form.is_valid() and formset.is_valid():
            question = question_form.save(commit=False)
            question.exam = exam
            question.save()

            formset.instance = question
            formset.save()

            return redirect("quiz:exam_detail", pk=exam.pk)

    else:
        question_form = QuestionForm()
        formset = ChoiceFormSet()

    context = {
        "exam": exam,
        "question_form": question_form,
        "formset": formset,
    }

    return render(
        request,
        "quiz/question_form.html",
        context,
    )
