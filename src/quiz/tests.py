from django.test import TestCase
from django.urls import reverse

from .forms import ChoiceFormSet
from .models import Choice, Exam, Question


class QuizModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.exam = Exam.objects.create(
            title="Django Fundamentals",
            description="Basic concepts assessment.",
        )
        cls.question = Question.objects.create(
            exam=cls.exam,
            text="What is Django?",
        )
        cls.choice = Choice.objects.create(
            question=cls.question,
            text="A Python web framework",
            is_correct=True,
        )

    def test_model_relationships_and_default_score(self):
        self.assertEqual(self.question.exam, self.exam)
        self.assertIn(self.question, self.exam.questions.all())
        self.assertIn(self.choice, self.question.choices.all())
        self.assertEqual(self.question.score, 1)

    def test_model_string_representations(self):
        self.assertEqual(str(self.exam), "Django Fundamentals")
        self.assertEqual(str(self.question), "What is Django?")
        self.assertEqual(str(self.choice), "A Python web framework")


class QuizViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.exam = Exam.objects.create(
            title="Django Exam",
            description="Assessment about Django.",
        )
        cls.question = Question.objects.create(
            exam=cls.exam,
            text="Which command starts the development server?",
        )
        Choice.objects.create(
            question=cls.question,
            text="python manage.py runserver",
            is_correct=True,
        )
        Choice.objects.create(
            question=cls.question,
            text="python manage.py start",
            is_correct=False,
        )

    def test_exam_list_displays_registered_exam(self):
        response = self.client.get(reverse("quiz:exam_list"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "quiz/exam_list.html")
        self.assertContains(response, self.exam.title)
        self.assertContains(response, self.exam.description)

    def test_exam_detail_displays_questions_and_choices(self):
        response = self.client.get(
            reverse("quiz:exam_detail", kwargs={"pk": self.exam.pk})
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "quiz/exam_detail.html")
        self.assertContains(response, self.question.text)
        self.assertContains(response, "python manage.py runserver")
        self.assertContains(response, "Correcta")


class QuestionCreateViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.exam = Exam.objects.create(
            title="Django Laboratory",
            description="Question creation tests.",
        )

    def build_form_data(self, correct_indexes):
        prefix = ChoiceFormSet.get_default_prefix()
        data = {
            "text": "What does MVT mean in Django?",
            f"{prefix}-TOTAL_FORMS": "4",
            f"{prefix}-INITIAL_FORMS": "0",
            f"{prefix}-MIN_NUM_FORMS": "0",
            f"{prefix}-MAX_NUM_FORMS": "1000",
        }

        choices = [
            "Model View Template",
            "Main View Test",
            "Model Version Type",
            "Module View Tool",
        ]

        for index, choice_text in enumerate(choices):
            data[f"{prefix}-{index}-text"] = choice_text
            if index in correct_indexes:
                data[f"{prefix}-{index}-is_correct"] = "on"

        return data

    def test_question_create_page_displays_four_choice_forms(self):
        response = self.client.get(
            reverse(
                "quiz:question_create",
                kwargs={"exam_id": self.exam.pk},
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "quiz/question_form.html")
        self.assertEqual(response.context["formset"].total_form_count(), 4)

    def test_valid_question_with_one_correct_choice_is_created(self):
        response = self.client.post(
            reverse(
                "quiz:question_create",
                kwargs={"exam_id": self.exam.pk},
            ),
            data=self.build_form_data(correct_indexes={0}),
        )

        question = Question.objects.get(exam=self.exam)
        self.assertRedirects(
            response,
            reverse("quiz:exam_detail", kwargs={"pk": self.exam.pk}),
        )
        self.assertEqual(question.score, 1)
        self.assertEqual(question.choices.count(), 4)
        self.assertEqual(question.choices.filter(is_correct=True).count(), 1)

    def test_question_without_correct_choice_is_rejected(self):
        response = self.client.post(
            reverse(
                "quiz:question_create",
                kwargs={"exam_id": self.exam.pk},
            ),
            data=self.build_form_data(correct_indexes=set()),
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "Debes marcar exactamente una alternativa como correcta.",
        )
        self.assertFalse(Question.objects.filter(exam=self.exam).exists())

    def test_question_with_multiple_correct_choices_is_rejected(self):
        response = self.client.post(
            reverse(
                "quiz:question_create",
                kwargs={"exam_id": self.exam.pk},
            ),
            data=self.build_form_data(correct_indexes={0, 1}),
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "Debes marcar exactamente una alternativa como correcta.",
        )
        self.assertFalse(Question.objects.filter(exam=self.exam).exists())
