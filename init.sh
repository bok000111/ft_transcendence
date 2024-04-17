echo 'alias manage="python /workspaces/ft_transcendence/srcs/requirements/django/manage.py"' >> ~/.zshrc

echo 'if [ -z "$SSH_AUTH_SOCK" ]; then
   # Check for a currently running instance of the agent
   RUNNING_AGENT="`ps -ax | grep 'ssh-agent -s' | grep -v grep | wc -l | tr -d '[:space:]'`"
   if [ "$RUNNING_AGENT" = "0" ]; then
        # Launch a new instance of the agent
        ssh-agent -s &> $HOME/.ssh/ssh-agent
   fi
   eval `cat $HOME/.ssh/ssh-agent`
fi' >> ~/.zshrc
echo 호스트 터미널에서 '"ssh-add $HOME/.ssh/id_rsa && eval "$(ssh-agent -s)"' 를 실행해면 바로 github에 접근할 수 있습니다.
