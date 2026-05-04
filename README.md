# SDN Project - Software Defined Networking

Goal
- Learn SDN incrementally using Mininet + OpenFlow 1.3 + Ryu.

Main files
- topology.py (Mininet topology)
- empty_controller.py (empty Ryu controller)
- firewall_controller.py (MAC learning + ICMP firewall)
- setup_env.sh (basic network dependencies on Ubuntu)

Basic requirement
- Linux with Mininet installed

Quick setup (Ubuntu)
```bash
sudo bash setup_env.sh
```

Ryu via Docker (recommended)
- Avoids Python conflicts on the host.

# Phase 1 - Topology without controller
```bash
sudo python3 topology.py
```
In the Mininet prompt:
```bash
pingall
```
Expected: 100% loss (no flow rules on switches).

# Phase 2 - Topology with empty controller

Terminal 1 - Empty Ryu controller
```bash
sudo docker run --rm --net=host -v "$PWD:/app" -w /app -e PYTHONPATH=/app osrg/ryu ryu-manager empty_controller
```

Terminal 2 - Mininet
```bash
sudo python3 topology.py --with-controller --ctrl-ip 127.0.0.1 --ctrl-port 6633
```

In the Mininet prompt:
```bash
dump
pingall
```
Expected: 100% loss, but Ryu logs the switches handshake.

# Phase 3 - MAC learning (simple_switch_13)

Terminal 1 - Ryu MAC learning switch
```bash
sudo docker run --rm --net=host osrg/ryu ryu-manager ryu.app.simple_switch_13
```

Terminal 2 - Mininet
```bash
sudo python3 topology.py --with-controller --ctrl-ip 127.0.0.1 --ctrl-port 6633
```

In the Mininet prompt:
```bash
pingall
```
Expected: 0% loss (all pings succeed).

Check flows installed by the controller:
```bash
sh ovs-ofctl -O OpenFlow13 dump-flows s1
sh ovs-ofctl -O OpenFlow13 dump-flows s2
```

# Phase 4 - Firewall policy (block ICMP h1 -> h4)

Terminal 1 - Ryu controller with firewall policy
```bash
sudo docker run --rm --net=host -v "$PWD:/app" -w /app -e PYTHONPATH=/app osrg/ryu ryu-manager firewall_controller
```

Terminal 2 - Mininet
```bash
sudo python3 topology.py --with-controller --ctrl-ip 127.0.0.1 --ctrl-port 6633
```

Validation (in Mininet):
```bash
h1 ping -c 2 h2
h3 ping -c 2 h4
h1 ping -c 2 h4
```
Expected:
- h1 -> h2 works
- h3 -> h4 works
- h1 -> h4 fails (ICMP blocked)

Verify TCP still works (simple web server on h4):
```bash
h4 python3 -m http.server 80 &
h1 curl -s http://10.0.0.4/ | head -n 1
```
Expected: HTTP content is returned.

Check flows installed by the controller:
```bash
sh ovs-ofctl -O OpenFlow13 dump-flows s1
sh ovs-ofctl -O OpenFlow13 dump-flows s2
```

Submission summary
- Topology: 2 OpenFlow switches (s1, s2) linked at 100 Mbps; 4 hosts on 10.0.0.0/24.
- Phase 1: No controller, all pings fail (no flow rules).
- Phase 2: Empty Ryu controller connects; switches handshake; traffic still drops.
- Phase 3: MAC learning (simple_switch_13) enables full L2 connectivity (pingall succeeds).
- Phase 4: Firewall policy drops ICMP from h1 to h4 while allowing other traffic; HTTP from h1 to h4 works.

Tips
- The sch_htb/quantum warning when using 100 Mbps is normal and does not affect validation.
- If Ryu does not start on the host, use the Docker command above.
