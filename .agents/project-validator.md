---
name: project-validator
description: Validate the Django project, models, relationships, migrations, configuration, and automated checks without redesigning the application.
---

# Responsibilities

- Review `settings.py`, models, forms, views, URLs, admin registration, templates, and migrations.
- Confirm that `Exam`, `Question`, and `Choice` exist.
- Confirm the `Exam` to `Question` and `Question` to `Choice` relationships.
- Confirm that `Question.score` is a `PositiveIntegerField` with a default of `1`.
- Confirm that `0001_initial.py` and `0002_question_score.py` exist.
- Check that no real credential is hard-coded in versioned settings.

# Commands

Run from `src/` with the active project interpreter:

```text
python manage.py check
python manage.py showmigrations quiz
python manage.py test
```

# Guardrails

- Do not modify application behavior when validation succeeds.
- Do not rewrite applied migrations unless an evident syntax error blocks execution.
- Report checks, successes, failures, affected files, and GitHub readiness in Spanish.

