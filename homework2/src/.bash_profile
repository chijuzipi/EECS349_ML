#Setting PATH for Python 3.4
# The orginal version is saved in .bash_profile.pysave

PATH="/Library/Frameworks/Python.framework/Versions/3.4/bin:${PATH}"
export PATH

#set the vim bash path
export PATH="/usr/local/bin:$PATH"

#set the node path
export NODE_PATH=/usr/local/lib/node_modules
#export NODE_PATH=/usr/local/lib/node_modules

#Setting colors for the terminal display
export PS1="\[\033[36m\]\u\[\033[m\]@\[\033[32m\]\h:\[\033[33;1m\]\w\[\033[m\]\$ "
export CLICOLOR=1
export LSCOLORS=gxBxhxDxfxhxhxhxhxcxcx
alias sls='ls -GFh'

#adding the algorithms 4th textbook code jar to JAVA buildpath
#export CLASSPATH=$CLASSPATH:~/Documents/Java_workspace/algs4_jar/stdlib.jar
#export CLASSPATH=$CLASSPATH:~/Documents/java_workspace/algs4_jar/algs4.jar
export CFLAGS=-Qunused-arguments
export CPPFLAGS=-Qunused-arguments


alias chrm='open /Applications/Google\ Chrome.app'
alias cdtextbook='cd ~/Dropbox/CS\ textbook/'
alias eclipse='bash /Applications/eclipse/runEclipse.sh'
alias cdCSP='cd ~/Documents/CSP'
alias cdTA='cd ~/Documents/TA'
alias cdJAVASPACE='cd ~/Documents/Java_workspace'
alias vi='vim'
alias cd..='cd ..'
alias l='ls'
alias ls='ls -l'
alias la='ls'
alias subl='sublime'
alias jc='javac'
alias j='java'
alias mongomac='mongo 192.168.0.101:27017'

function cd {
  builtin cd "$@" && ls 
}

##
# Your previous /Users/Yu/.bash_profile file was backed up as /Users/Yu/.bash_profile.macports-saved_2015-04-19_at_12:24:43
##

# MacPorts Installer addition on 2015-04-19_at_12:24:43: adding an appropriate PATH variable for use with MacPorts.
export PATH="/opt/local/bin:/opt/local/sbin:$PATH"
# Finished adapting your PATH environment variable for use with MacPorts.

