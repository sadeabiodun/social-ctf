eval 'set +o history' 2>/dev/null || setopt HIST_IGNORE_SPACE 2>/dev/null
 touch ~/.gitcookies
 chmod 0600 ~/.gitcookies

 git config --global http.cookiefile ~/.gitcookies

 tr , \\t <<\__END__ >>~/.gitcookies
partner-code.googlesource.com,FALSE,/,TRUE,2147483647,o,git-fabiodun.princeton.edu=1//01GbwqnX8rwhbCgYIARAAGAESNwF-L9IrnOw322SVVR2jwAj9PmqVgEVQYTjtN5cupvl_3UkHEn-KyClsMjoOCXjwx3rj9FZeb4E
partner-code-review.googlesource.com,FALSE,/,TRUE,2147483647,o,git-fabiodun.princeton.edu=1//01GbwqnX8rwhbCgYIARAAGAESNwF-L9IrnOw322SVVR2jwAj9PmqVgEVQYTjtN5cupvl_3UkHEn-KyClsMjoOCXjwx3rj9FZeb4E
__END__
eval 'set -o history' 2>/dev/null || unsetopt HIST_IGNORE_SPACE 2>/dev/null
