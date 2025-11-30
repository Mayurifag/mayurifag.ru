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
alias ports='sudo ss -ltnp'
alias dusize='sudo ncdu /'
alias disksize='df -h --total | grep -v tmpfs'
alias reboot='sudo reboot'
alias shutdown='sudo shutdown now'
alias apt-get='sudo apt-get'
alias aptclean='sudo apt autoremove && sudo apt clean && sudo apt autoclean'
alias yabs='curl -sL https://yabs.sh | bash'
alias apt='sudo apt'

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

################
# DUMB FILE    #
################

createdumb() {
  local dumbfile="/var/dumb/dumbfile"
  if [ -f "$dumbfile" ]; then
    echo "File '$dumbfile' already exists."
  else
    if [ ! -d "/var/dumb" ]; then
      echo "Directory /var/dumb does not exist."
      return 1
    fi

    echo "Free space before: $(df -h /var/dumb | awk 'NR==2 {print $4}')"

    local avail
    avail=$(df --output=avail -k /var/dumb | tail -n 1)
    local size=$((avail * 20 / 100))

    echo "Creating '$dumbfile'..."
    if fallocate -l "${size}K" "$dumbfile"; then
      local created_size
      created_size=$(du -h "$dumbfile" | awk '{print $1}')
      echo "Done. Created '$dumbfile' with size: $created_size"
    else
      echo "Failed to create file."
      return 1
    fi

    echo "Free space after: $(df -h /var/dumb | awk 'NR==2 {print $4}')"
  fi
}

removedumb() {
  local dumbfile="/var/dumb/dumbfile"
  if [ -f "$dumbfile" ]; then
    echo "Free space before: $(df -h /var/dumb | awk 'NR==2 {print $4}')"
    local size_before
    size_before=$(du -h "$dumbfile" | awk '{print $1}')

    if rm "$dumbfile"; then
      echo "Removed '$dumbfile' (was $size_before)."
    else
      echo "Failed to remove '$dumbfile'."
      return 1
    fi

    echo "Free space after: $(df -h /var/dumb | awk 'NR==2 {print $4}')"
  else
    echo "File '$dumbfile' does not exist."
  fi
}
