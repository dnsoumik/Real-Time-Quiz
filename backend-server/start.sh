#WEB SERVER

ulimit -n 10000

PID_HOME="/tmp/elsa_quiz"
LOG_PATH="./log"
LOG_FILE="$LOG_PATH/run.log"

APPLICATION="app.py"

mkdir -p $PID_HOME
mkdir -p $LOG_PATH

IN_LINE="nohup python$PYTHON_VERSION ./$APPLICATION > dev/null"
$IN_LINE &

rm $PID_HOME/$APPLICATION.pid

pgrep "python ./app.py > dev/null" -f > $PID_HOME/$APPLICATION.pid

chgrp xlayer -R $PID_HOME
chgrp xlayer -R $LOG_PATH
chmod g=rwx -R $PID_HOME
chmod g=rwx -R $LOG_PATH