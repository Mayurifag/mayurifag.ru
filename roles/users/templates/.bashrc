# EXPORTS
export EDITOR=vi

###########
# ALIASES #
###########

alias apt-get='sudo apt-get'
alias apt='sudo apt'
alias aptclean='sudo apt autoremove && sudo apt clean && sudo apt autoclean'
alias disksize='df -h --total | grep -v tmpfs'
alias dusize='sudo ncdu /'
alias grep='grep --color=auto'
alias install='sudo apt install'
alias ld='lazydocker'
alias lips='echo "Local IP: $(hostname -I | cut -d" " -f1)"; echo "Public IP: $(curl -s ifconfig.me)"'
alias ls='ls -AlF --color=auto'
alias meminfo='free -m -l -t -s'
alias ports='sudo ss -ltnp'
alias reboot='sudo reboot'
alias remove='sudo apt remove'
alias shutdown='sudo shutdown now'
alias update='sudo apt update && sudo apt upgrade -y'
alias yabs='curl -sL https://yabs.sh | bash'

# CrowdSec
alias cscli='docker exec crowdsec cscli'

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

# Determine user color: Red if root, Yellow if standard user
if [ "$EUID" -eq 0 ]; then
  USER_COLOR="\[\033[38;5;196m\]" # Red
else
  USER_COLOR="\[\033[38;5;11m\]"  # Yellow (Original)
fi

# Set a more informative prompt
export PS1="${USER_COLOR}\u\[$(tput sgr0)\]\[\033[38;5;15m\]@\h:\[$(tput sgr0)\]\[\033[38;5;6m\][\w]:\[$(tput sgr0)\]\[\033[38;5;15m\] \\$ \[$(tput sgr0)\]"

###########
# OPTIONS #
###########

shopt -s cdspell # Enable cdspell to automatically correct minor spelling errors in cd command
shopt -s extglob # Enable extended pattern matching
# shopt -s glob # Enable globbing
shopt -s histappend # Append to history instead of overwriting
shopt -s autocd # Enable autocd to allow directory names to be used as commands

################
# DUMB FILE    #
################

DUMB_FILE="/var/dumb/dumbfile"

# Helper to print stats (KISS)
_dumb_info() {
  echo "Free space: $(df -h "${DUMB_FILE%/*}" | awk 'NR==2 {print $4}')"
}

createdumb() {
  [ -f "$DUMB_FILE" ] && { echo "File '$DUMB_FILE' already exists."; return 0; }
  [ ! -d "${DUMB_FILE%/*}" ] && { echo "Directory ${DUMB_FILE%/*} does not exist."; return 1; }

  _dumb_info

  # Calculate 20% of available space (in KB)
  local avail_kb=$(df --output=avail -k "${DUMB_FILE%/*}" | tail -n 1)
  local size_kb=$((avail_kb * 20 / 100))

  echo "Creating file with size: $((size_kb / 1024))M..."

  if fallocate -l "${size_kb}K" "$DUMB_FILE"; then
    ls -lh "$DUMB_FILE"
  else
    echo "Failed to create file."
    return 1
  fi

  _dumb_info
}

removedumb() {
  [ ! -f "$DUMB_FILE" ] && { echo "File '$DUMB_FILE' does not exist."; return 1; }

  _dumb_info

  # Verbose remove
  rm -v "$DUMB_FILE" && _dumb_info
}
