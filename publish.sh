git add .
git commit -m "update docs"
git push
python homepage.py
mkdocs gh-deploy
