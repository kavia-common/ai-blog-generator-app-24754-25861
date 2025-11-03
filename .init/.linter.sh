#!/bin/bash
cd /home/kavia/workspace/code-generation/ai-blog-generator-app-24754-25861/BackendAPIService
source venv/bin/activate
flake8 .
LINT_EXIT_CODE=$?
if [ $LINT_EXIT_CODE -ne 0 ]; then
  exit 1
fi

