#!/bin/bash
cat /etc/redhat-release | awk '{print $1" "$2" "$3" "$4" "$5" "$7}'