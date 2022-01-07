#!/bin/bash
# Copyright 2017 - LongVan System Solution JSC
# OS: Ubuntu 12.04; Ubuntu 14.04; Ubuntu 16.04; Debian 8
# Feature: Configuration network

# Variable
MAC=$1
IP=$2
SUBNET=$3
GATEWAY=$4
DNS1=$5
DNS2=$6
INAME=$(ip -o link show | grep $MAC | sed -rn '/^[0-9]+: e/{s/.: ([^:]*):.*/\1/p}')

# Configuration Interface
cp /etc/network/interfaces /etc/network/interfaces.default
echo "
# This file describes the network interfaces available on your system
# and how to activate them. For more information, see interfaces(5).

source /etc/network/interfaces.d/*

# The loopback network interface
auto lo
iface lo inet loopback

# The primary network interface
auto $INAME
iface $INAME inet static
address $IP
netmask $SUBNET
gateway $GATEWAY
dns-nameservers $DNS1
dns-nameservers $DNS2" > /etc/network/interfaces

# Restart network
service networking restart
