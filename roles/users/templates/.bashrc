# EXPORTS
export EDITOR=vi

###########
# ALIASES #
###########

# TODO: filesize and date formatting
alias ls='ls -AlF --color=auto'
alias grep='grep --color=auto'
alias update='sudo apt update && sudo apt upgrade -y'
alias install='sudo apt install'
alias remove='sudo apt remove'
alias lips='echo "Local IP: $(hostname -I | cut -d" " -f1)"; echo "Public IP: $(curl -s ifconfig.me)"'
alias meminfo='free -m -l -t -s'
alias ports='netstat -tulanp'
alias dusize='du -ah --max-depth=1 --exclude={/proc/*,/sys/*,/dev/*,/run/*,/tmp/*,/var/run/*,/var/tmp/*} 2>/dev/null | sort -hr'
alias disksize='df -h --total | grep -v tmpfs'
alias reboot='sudo reboot'
alias shutdown='sudo shutdown now'
alias apt-get='sudo apt-get'
alias aptclean='sudo apt autoremove && sudo apt clean && sudo apt autoclean'
alias yabs='curl -sL https://yabs.sh | bash'

############
# COMMANDS #
############

mkcd() { mkdir -p "$1" && cd "$1"; }
backup() { cp "$1"{,.bak}; }

###########
# HISTORY #
###########

HISTSIZE=5000 # Increase history size
HISTFILESIZE=10000 # Increase history file size
HISTCONTROL=ignoredups # Ignore duplicate commands in history

###########
# PROMPT #
###########

# Set a more informative prompt
export PS1="\[\033[38;5;11m\]\u\[$(tput sgr0)\]\[\033[38;5;15m\]@\h:\[$(tput sgr0)\]\[\033[38;5;6m\][\w]:\[$(tput sgr0)\]\[\033[38;5;15m\] \\$ \[$(tput sgr0)\]"

###########
# OPTIONS #
###########

shopt -s cdspell # Enable cdspell to automatically correct minor spelling errors in cd command
shopt -s extglob # Enable extended pattern matching
# shopt -s glob # Enable globbing
shopt -s histappend # Append to history instead of overwriting
shopt -s autocd # Enable autocd to allow directory names to be used as commands
