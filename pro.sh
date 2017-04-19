ps -ef | grep python | grep -v grep | awk '{print $2}'| xargs kill -9
git fetch --all
git reset --hard origin/master
nohup python app.py > /dev/null 2>./error.txt &
