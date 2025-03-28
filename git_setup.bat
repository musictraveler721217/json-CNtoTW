@echo off
echo 初始化Git倉庫...
git init

echo 設置遠端倉庫...
set /p REPO_URL="請輸入GitHub倉庫URL (例如: https://github.com/username/repo.git): "
git remote add origin %REPO_URL%

echo 添加檔案到Git...
git add .

echo 提交變更...
git commit -m "初始提交"

echo 推送到GitHub...
git push -u origin master

echo 完成！
pause