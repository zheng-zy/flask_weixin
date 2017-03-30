git fetch --all
git reset --hard origin/master
nohup python app.py > /dev/null 2>./error.txt &
