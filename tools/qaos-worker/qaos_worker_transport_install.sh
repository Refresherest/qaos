#!/bin/sh
set -eu

BROKER_USER=qaos-broker
BROKER_HOME=/var/lib/qaos-broker

install -o root -g root -m 0700 \
  /tmp/qaos_worker_transport_rollback.sh \
  /usr/local/sbin/qaos-worker-broker-rollback

systemd-run \
  --unit=qaos-worker-broker-rollback \
  --on-active=15m \
  /usr/local/sbin/qaos-worker-broker-rollback

install -o root -g root -m 0755 \
  /tmp/qaos_worker_broker.py \
  /usr/local/sbin/qaos-worker-broker
install -o root -g root -m 0644 \
  /tmp/qaos_worker_exchange.py \
  /usr/local/sbin/qaos_worker_exchange.py

if ! getent passwd "$BROKER_USER" >/dev/null 2>&1; then
  useradd \
    --system \
    --home-dir "$BROKER_HOME" \
    --create-home \
    --shell /bin/sh \
    "$BROKER_USER"
fi
passwd -l "$BROKER_USER" >/dev/null

install -d -o root -g root -m 0755 "$BROKER_HOME"
install -d -o root -g root -m 0755 "$BROKER_HOME/.ssh"
{
  printf '%s ' 'restrict,command="/usr/bin/sudo -n /usr/local/sbin/qaos-worker-broker"'
  cat /tmp/qaos-worker-transport-ed25519.pub
} > "$BROKER_HOME/.ssh/authorized_keys"
chown root:root "$BROKER_HOME/.ssh/authorized_keys"
chmod 0644 "$BROKER_HOME/.ssh/authorized_keys"

printf '%s\n' \
  'qaos-broker ALL=(root) NOPASSWD: /usr/local/sbin/qaos-worker-broker' \
  > /etc/sudoers.d/qaos-worker-broker
chown root:root /etc/sudoers.d/qaos-worker-broker
chmod 0440 /etc/sudoers.d/qaos-worker-broker
visudo -cf /etc/sudoers.d/qaos-worker-broker >/dev/null

rm -f /tmp/qaos_worker_exchange.py
rm -f /tmp/qaos_worker_broker.py
rm -f /tmp/qaos_worker_transport_rollback.sh
rm -f /tmp/qaos-worker-transport-ed25519.pub
rm -f /tmp/qaos_worker_transport_install.sh

printf '%s\n' 'restricted-transport-installed-with-rollback-armed'
