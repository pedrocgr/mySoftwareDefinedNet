#!/usr/bin/env bash
set -euo pipefail

if [ "$(id -u)" -ne 0 ]; then
  echo "Este script deve ser executado com sudo. Ex: sudo bash setup_env.sh"
  exit 1
fi

apt update
apt install -y git python3-pip python3-setuptools build-essential \
  openvswitch-switch openvswitch-testcontroller mininet

pip3 install --upgrade pip
pip3 install ryu

echo "Instalação concluída. Inicie o controlador com: ryu-manager ryu.app.simple_switch_13"
echo "Depois execute a topologia exemplo: sudo python3 topology.py"
