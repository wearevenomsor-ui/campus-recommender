@echo off
echo ========================================================
echo Pushing Campus Event Recommender to GitHub...
echo Author: Adarsh S
echo Repo: https://github.com/wearevenomsor-ui/campus-recommender
echo ========================================================

cd /d "C:\Users\Randi\Documents\PROJECT"

git init
git config user.name "Adarsh S"
git config user.email "wearevnomsor@gmail.com"
git config credential.helper manager
git branch -M main

git remote remove origin 2>nul
git remote add origin https://github.com/wearevenomsor-ui/campus-recommender.git

git add .
git commit -m "Campus Event Recommendation Engine by Adarsh S"

echo.
echo Now pushing to main branch...
git push -u origin main

echo.
echo ========================================================
echo Done! Check: https://github.com/wearevenomsor-ui/campus-recommender
echo ========================================================
pause
