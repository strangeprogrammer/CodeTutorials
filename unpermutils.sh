#!/bin/false

# Do not run this file directly - source it instead

unset -v UTILS_DIR UTILS_SETTINGS DEV_USER DEV_GROUP SERVER_USER SERVER_GROUP	&>/dev/null
unset -f changeperms developer devdeploy deployment openaccess closeaccess	&>/dev/null

PS1=${PS1#"(permutils) "}
