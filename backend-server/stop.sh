
# Remove all the compiled files
find . -name "*.pyc" -type f -delete

PID_HOME="/tmp/elsa_quiz"
APPLICATION="app.py"

# Kill the PIDs
echo `cat $PID_HOME/$APPLICATION.pid`
pkill -e -F $PID_HOME/$APPLICATION.pid