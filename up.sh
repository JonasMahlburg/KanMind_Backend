git add .
git commit -m "$*"
git push
ssh paintingotter34@34.12.5.36 "cd projects/KanMind_Backend && sudo git pull && sudo supervisorctl restart kanmind-gunicorn"
