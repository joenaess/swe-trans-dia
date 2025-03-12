# Contributing to swe-trans-dia

Thank you for considering contributing to the Swedish Transcription and Diarization project! We welcome contributions to help improve and expand this project.

## Code of Conduct

This project and everyone participating in it is governed by the [Contributor Covenant Code of Conduct](https://www.contributor-covenant.org/version/2/1/code_of_conduct.html). By participating, you are expected to uphold this code. Please report unacceptable behavior to <your-email@example.com>.

## How to Contribute

Here's a guide to help you contribute effectively:

### 1.  Fork the Repository

* Fork the repository to your own GitHub account.

### 2.  Set Up Your Development Environment

* Clone your fork to your local machine:

       ```bash
       git clone [https://github.com/your-username/swe-trans-dia.git](https://www.google.com/search?q=https://github.com/your-username/swe-trans-dia.git)
       cd swe-trans-dia
       ```

* Create and activate a virtual environment (recommended):

       ```bash
       python3 -m venv venv
       source venv/bin/activate  # macOS/Linux
       venv\Scripts\activate  # Windows
       ```

* Install the project dependencies:

       ```bash
       pip install -r app/requirements.txt
       ```

### 3.  Create a Branch

* Create a branch for your changes:

       ```bash
       git checkout -b feature/my-feature
       ```

### 4.  Code Style

* This project follows the PEP 8 style guide for Python. Please ensure that your code adheres to PEP 8.
* We use Ruff for linting and formatting.

* To check your code locally:

       ```bash
       ruff check .
       ```

* To automatically format your code:

       ```bash
       ruff format .
       ```

* Our CI will enforce these code style rules.

### 5.  Testing

* All contributions should be accompanied by relevant tests.
* To run the tests locally:

       ```bash
       pytest tests/
       ```
* CI will automatically run the test suite.
* Focus on writing tests that cover the specific changes you're making.

### 6.  Making Changes

* Implement your changes, ensuring they adhere to the code style and include tests.
* Keep your changes focused and avoid large, unrelated modifications.
* Write clear, concise, and well-documented code.

### 7.  Commit Changes

* Write clear and descriptive commit messages.
* Use the present tense ("Add feature" not "Added feature").
* Describe *what* changed and *why*.

    ```bash
   git add .
   git commit -m "feat: Add new feature for..."
    ```