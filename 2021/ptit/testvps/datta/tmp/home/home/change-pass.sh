#!/bin/bash
# Copyright 2017 - LongVan System Solution JSC
# OS: CentOS 6; CentOS 7; Ubuntu 12.04; Ubuntu 14.04; Ubuntu 16.04; Debian 8
# Feature: Change password root

# Variable
NEWPASS=$1

# Set password root
passwd << EOF
$NEWPASS
$NEWPASS
EOF
