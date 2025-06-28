# Contributing to RootMonkey

Thank you for your interest in contributing to RootMonkey!
This guide outlines the process for contributing to the project.

## How to Contribute

### Bug Reports and Feature Requests
The best way to report a bug or request a new feature is to **open an issue on GitHub**.
When filing an issue, please provide as much detail as possible.

### Submitting Pull Requests

We use Pull Requests (PRs) to review and merge code changes.
  * **For minor changes** (e.g., fixing a typo, a small bug), feel free to submit a PR directly.
  * **For significant changes** (e.g., adding a new feature, major refactoring), please **open an issue first** to discuss the proposed changes with the maintainers.

## Development Setup

Follow these steps to set up your local development environment.

#### 1. Clone the Repository

First, clone the repository to your local machine:

```bash
git clone https://github.com/rootagent/rmk.git
cd rmk
```

#### 2. Create and Activate a Virtual Environment

We use `uv` to manage our Python environment and dependencies. Create and activate a new virtual environment:

```bash
uv venv --python 3.12
source .venv/bin/activate  # On Windows, use: .venv\Scripts\activate
```

#### 3. Install Dependencies and Tools

Install the project in "editable" mode, which allows your code changes to be reflected immediately. Then, install the pre-commit hooks for code formatting and linting.

```bash
uv pip install -e .

pre-commit install
```

## Running Tests

We use `pytest` for unit testing. All tests are located in the `tests/` directory.

  * To run the entire test suite, execute:
    ```bash
    pytest
    ```
  * When adding new features or fixing bugs, please include corresponding tests to maintain code quality and coverage.

## Code Style and Linting

We use `pre-commit` hooks to ensure consistent code style and quality.

  * The hooks will run automatically every time you make a commit.
  * If a hook fails, it may automatically fix the file. Simply git add the modified files and commit again.
  * You can also run the hooks manually on all files at any time:
    ```bash
    pre-commit run --all-files
    ```
