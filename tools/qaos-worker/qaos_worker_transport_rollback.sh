#!/bin/sh
set -eu

rm -f /etc/sudoers.d/qaos-worker-broker
rm -f /var/lib/qaos-broker/.ssh/authorized_keys
userdel qaos-broker 2>/dev/null || true
rm -rf /var/lib/qaos-broker
rm -rf /var/lib/qaos-worker-broker
rm -rf /run/qaos-worker-broker
rm -f /usr/local/sbin/qaos-worker-broker
rm -f /usr/local/sbin/qaos_worker_exchange.py
