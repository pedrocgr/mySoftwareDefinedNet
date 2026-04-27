#!/usr/bin/env python3
"""
Topologia Fase 1 — Mininet (OpenFlow 1.3)

Requisitos da topologia:
- 2 switches OpenFlow: s1 e s2, com um link entre eles de 100 Mbps
- 4 hosts: h1,h2 ligados a s1; h3,h4 ligados a s2
- Todos os nós na mesma sub-rede 10.0.0.0/24

Validação esperada: sem controlador conectado e com os switches em modo
seguro, `pingall` deve falhar (100% perda) pois não há regras instaladas.
"""

import argparse

from mininet.net import Mininet
from mininet.node import RemoteController, OVSSwitch
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel, info


def build_phase1_topology(use_controller=False, ctrl_ip='127.0.0.1', ctrl_port=6633):
    if use_controller:
        net = Mininet(controller=RemoteController, switch=OVSSwitch, link=TCLink, autoSetMacs=True)
    else:
        net = Mininet(controller=None, switch=OVSSwitch, link=TCLink, autoSetMacs=True)

    info('*** Adicionando hosts (10.0.0.0/24)\n')
    h1 = net.addHost('h1', ip='10.0.0.1/24')
    h2 = net.addHost('h2', ip='10.0.0.2/24')
    h3 = net.addHost('h3', ip='10.0.0.3/24')
    h4 = net.addHost('h4', ip='10.0.0.4/24')

    info('*** Adicionando switches OpenFlow (modo seguro, OpenFlow13)\n')
    # failMode='secure' deixa o switch sem encaminhamento quando não há controlador
    s1 = net.addSwitch('s1', protocols='OpenFlow13', failMode='secure')
    s2 = net.addSwitch('s2', protocols='OpenFlow13', failMode='secure')

    info('*** Conectando nós (link s1-s2 com 100 Mbps)\n')
    net.addLink(h1, s1)
    net.addLink(h2, s1)
    net.addLink(h3, s2)
    net.addLink(h4, s2)
    net.addLink(s1, s2, bw=100)

    if use_controller:
        info('*** Construindo e iniciando a rede (com RemoteController %s:%s)\n' % (ctrl_ip, ctrl_port))
    else:
        info('*** Construindo e iniciando a rede (sem controlador)\n')

    net.build()
    if use_controller:
        c0 = net.addController('c0', controller=RemoteController, ip=ctrl_ip, port=int(ctrl_port))
        c0.start()
        s1.start([c0])
        s2.start([c0])
    else:
        # iniciar switches sem controladores (passar lista vazia)
        s1.start([])
        s2.start([])

    info('*** CLI — execute `pingall` para validar (deve falhar)\n')
    CLI(net)

    info('*** Parando a rede\n')
    net.stop()


def parse_args():
    parser = argparse.ArgumentParser(description='Topologia Fase 1 (Mininet)')
    parser.add_argument('--with-controller', action='store_true', help='Conectar a um RemoteController')
    parser.add_argument('--ctrl-ip', default='127.0.0.1', help='IP do controlador (default: 127.0.0.1)')
    parser.add_argument('--ctrl-port', default=6633, help='Porta do controlador (default: 6633)')
    return parser.parse_args()


if __name__ == '__main__':
    setLogLevel('info')
    args = parse_args()
    build_phase1_topology(use_controller=args.with_controller, ctrl_ip=args.ctrl_ip, ctrl_port=args.ctrl_port)
