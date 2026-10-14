#!/usr/bin/env bash
set -e

REPO_NAME="english-listening-practice"
GITHUB_USER="0xImwhatIm"

echo "🚀 準備建立並部署 https://github.com/${GITHUB_USER}/${REPO_NAME} ..."

git init
git branch -M main
git add .
git commit -m "feat: initial commit of Grade 7 English Listening & Reading Trainer"

if command -v gh &> /dev/null; then
  echo "✅ 偵測到 GitHub CLI (gh)，正在自動建立公開 Repo 並推送..."
  gh repo create "${GITHUB_USER}/${REPO_NAME}" --public --source=. --remote=origin --push
  echo "🎉 推送完成！請至 https://github.com/${GITHUB_USER}/${REPO_NAME}/settings/pages 將 Source 設為 GitHub Actions (或 Deploy from branch: main)！"
else
  echo "💡 請先在 GitHub 建立名為 ${REPO_NAME} 的空白儲存庫，接著執行："
  echo "   git remote add origin https://github.com/${GITHUB_USER}/${REPO_NAME}.git"
  echo "   git push -u origin main"
fi
