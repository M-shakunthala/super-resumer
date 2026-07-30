#!/bin/bash

echo "🔍 GitHub Cleanup Verification"
echo "=============================="
echo ""

# Check for sensitive files
sensitive_files=(".env" "jobs.db" "*.pyc" "__pycache__" "chrome_profile" "chrome_sessions")

echo "Checking for sensitive files..."
all_clean=true

for item in "${sensitive_files[@]}"; do
    if find . -name "$item" -o -name "$item" | grep -q .; then
        echo "❌ Found: $item"
        all_clean=false
    else
        echo "✅ Clean: $item"
    fi
done

echo ""
echo "Checking directory structure..."
required_dirs=("agents" "core" "infra" "memory" "ui" "config" "tests" "docs" "screenshots")

for dir in "${required_dirs[@]}"; do
    if [ -d "$dir" ]; then
        echo "✅ $dir/ exists"
    else
        echo "❌ $dir/ missing"
        all_clean=false
    fi
done

echo ""
echo "Checking for .gitignore..."
if [ -f ".gitignore" ]; then
    echo "✅ .gitignore exists"
    if grep -q ".env" .gitignore; then
        echo "✅ .env is ignored"
    else
        echo "❌ .env not in .gitignore"
        all_clean=false
    fi
else
    echo "❌ .gitignore missing"
    all_clean=false
fi

echo ""
echo "Checking for .env.example..."
if [ -f ".env.example" ]; then
    echo "✅ .env.example exists"
else
    echo "❌ .env.example missing"
    all_clean=false
fi

echo ""
if [ "$all_clean" = true ]; then
    echo "🎉 Repository is clean and ready for GitHub!"
    echo ""
    echo "Next steps:"
    echo "1. git init"
    echo "2. git add ."
    echo "3. git commit -m 'Initial commit'"
    echo "4. Create GitHub repository"
    echo "5. git remote add origin <your-repo-url>"
    echo "6. git push -u origin main"
else
    echo "⚠️  Issues found. Please clean up before uploading."
fi