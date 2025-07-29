# ALX Backend Python - Unit Tests and Integration Tests

This project contains unit tests and integration tests for Python utilities and a GitHub organization client. It follows best practices using `unittest`, `parameterized`, and `unittest.mock` for mocking external calls.

---

## Project Structure

- `utils.py`  
  Contains utility functions:
  - `access_nested_map` — safely access nested dictionaries.
  - `get_json` — fetch JSON data from URLs.
  - `memoize` — decorator to cache method results.

- `client.py`  
  Defines `GithubOrgClient` class for interacting with the GitHub API.

- `test_utils.py`  
  Unit tests for `utils.py` functions.

- `test_client.py`  
  Unit and integration tests for `GithubOrgClient`.

---

## Requirements

- Python 3.7 (Ubuntu 18.04 LTS compatible)
- `parameterized` package (for parameterized tests)
- `requests` package (used by `get_json`)

Install dependencies with:

```bash
pip install parameterized requests
