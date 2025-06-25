#!/bin/bash
# Push RaiderBot to GitHub

echo "🐕 Pushing RaiderBot to GitHub..."

# Add your GitHub remote (replace YOUR_USERNAME with your actual GitHub username)
echo "➡️ Add your GitHub remote URL:"
echo "Example: git remote add origin https://github.com/YOUR_USERNAME/raiderbot-palantir-foundry.git"
echo ""
read -p "Enter your GitHub repository URL: " REPO_URL

git remote add origin $REPO_URL

# Verify remote was added
echo "✅ Remote added:"
git remote -v

# Push all branches and tags
echo "🚀 Pushing to GitHub..."
git push -u origin main

echo "✅ Successfully pushed to GitHub!"
echo ""
echo "🎯 Next steps:"
echo "1. Add repository topics on GitHub: palantir-foundry, german-shepherd-ai, transportation"
echo "2. Update repository settings if needed"
echo "3. Share with your team!"
echo ""
echo "🐕 Woof! RaiderBot is now on GitHub!"
