# Contributing to Local LLM Instrumentation Platform

We love your input! We want to make contributing to this project as easy and transparent as possible.

## Project Setup
1. Fork and clone the repo.
2. Ensure you have Docker and Docker Compose installed.
3. Copy `backend/.env.example` to `backend/.env`.
4. Run `make rebuild` to start the stack.
5. The frontend is accessible at `http://localhost:5173` and the backend at `http://localhost:8000`.

## Coding Standards
- **Backend:** We use `black` for formatting and `flake8` for linting. All PyTorch hooks must explicitly avoid VRAM leaks by calling `.item()` or `.detach().cpu()` on tensors before passing them to the EventBus.
- **Frontend:** We use ESLint and Prettier. Shadcn-UI components should not be heavily modified unless necessary. Ensure Tailwind classes are organized logically.

## Commit Message Conventions
We follow conventional commits:
- `feat:` for new features
- `fix:` for bug fixes
- `docs:` for documentation changes
- `refactor:` for refactoring code without adding features or fixing bugs
- `chore:` for updating build tasks, package manager configs, etc.

Example: `feat(telemetry): implement attention entropy calculation`

## Pull Request Process
1. Ensure your code passes all linting.
2. Describe your changes in the PR description thoroughly.
3. If adding a new telemetry hook, provide a screenshot of the Memory Monitor to prove it does not leak VRAM.
4. Request review from a maintainer.
