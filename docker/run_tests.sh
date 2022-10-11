# #!/usr/bin/env bash

set -eo pipefail

# only generate html locally
#pytest tests --cov-report html

echo "Running MyPy..."
#mypy tidecast tests

echo "Running black..."
black tidecast tests

echo "Running iSort..."
isort tidecast tests

echo "Running flake8..."
flake8 tidecast tests

echo "Running bandit..."
bandit --ini .bandit --quiet -r tidecast