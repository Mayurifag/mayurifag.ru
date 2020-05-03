# this worker will be used as postfix milter
milter = yes;

timeout = 120s; # Needed for Milter usually

# note to self - tighten up these permissions
#bind_socket = "/var/run/rspamd/milter.sock mode=0666 owner=nobody";

# DEFAULT: listens on localhost:11332


# the following specifies self-scan mode, for when rspamd is on the same
# machine as postfix
timeout = 120s;
upstream "local" {
  default = yes;
  self_scan = yes;
}

max_retries = 5; # How many times master is queried in case of failure

bind_socket = "127.0.0.1:11332";
bind_socket = "[::1]:11332";
