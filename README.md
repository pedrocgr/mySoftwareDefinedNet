# SDN Project - Software Defined Networking

Goal
- Learn SDN incrementally using Mininet + OpenFlow 1.3 + Ryu.

Main files
- topology.py (Mininet topology)
- empty_controller.py (empty Ryu controller)
- setup_env.sh (basic network dependencies on Ubuntu)

Basic requirement
- Linux with Mininet installed

Quick setup (Ubuntu)
```bash
sudo bash setup_env.sh
```

Ryu via Docker (recommended)
- Avoids Python conflicts on the host.

Terminal 1 - Empty Ryu controller
```bash
sudo docker run --rm --net=host -v "$PWD:/app" -w /app -e PYTHONPATH=/app osrg/ryu ryu-manager empty_controller
```

Phase 1 - Topology without controller
```bash
sudo python3 topology.py
```
In the Mininet prompt:
```bash
pingall
```
Expected: 100% loss (no flow rules on switches).

Phase 2 - Topology with remote controller
```bash
sudo python3 topology.py --with-controller --ctrl-ip 127.0.0.1 --ctrl-port 6633
```
In the Mininet prompt:
```bash
dump
pingall
```
Expected: 100% loss, but Ryu logs the switches handshake.

Tips
- The sch_htb/quantum warning when using 100 Mbps is normal and does not affect validation.
- If Ryu does not start on the host, use the Docker command above.
