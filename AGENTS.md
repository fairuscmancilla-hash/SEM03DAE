# Django Laboratory Finalization Agents

This repository uses a primary coordination role and three specialist roles to close the Django laboratory safely.

## Primary agent

Use `.agents/django-lab-finalizer.md` as the coordinator. It must delegate focused work to:

- `.agents/project-validator.md`
- `.agents/git-manager.md`
- `.agents/evidence-preparer.md`

## Required workflow

1. Validate the Django project.
2. Review migrations.
3. Review Git and `.gitignore`.
4. Review files proposed for version control.
5. Prepare local commits.
6. Validate the branch and remote.
7. Prepare, but never automatically execute, the push.
8. Organize final evidence.

## Repository guardrails

- Preserve application behavior unless a critical execution or publication issue requires a minimal correction.
- Keep Django migrations versioned.
- Never delete `db.sqlite3` to resolve an error.
- Never commit `venv/`, `db.sqlite3`, `.env`, `__pycache__/`, `*.pyc`, or `.vscode/`.
- Never expose credentials.
- Never invent a repository URL.
- Never run `git push`, `git push --force`, `git reset --hard`, or `git clean -fd` automatically.
- Explain findings and requested actions to the user in Spanish.
- Keep source code and technical identifiers in English.

