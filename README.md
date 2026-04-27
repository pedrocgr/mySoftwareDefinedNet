# Projeto SDN — Redes Definidas por Software (Exercício)

Objetivo
-------
Este projeto tem como objetivo proporcionar uma experiência prática com o paradigma
de Redes Definidas por Software (SDN). O desenvolvimento será incremental e dividido
em fases; na fase 1 construiremos a infraestrutura (topologia) com Mininet e um
controlador centralizado (Ryu) usando OpenFlow 1.3.

Ferramentas recomendadas
- Mininet (Ubuntu/Linux)
- Ryu Controller (Python)
- OpenFlow 1.3
- Wireshark (opcional)

Estrutura inicial criada
- `README.md` — este arquivo
- `setup_env.sh` — script para instalar dependências (Ubuntu/Debian)
- `requirements.txt` — dependências Python (Ryu)
- `topology.py` — script Mininet de exemplo (OpenFlow 1.3)

Começando (rápido)
------------------
1. Torne o script executável e execute (requer `sudo`):

```bash
sudo bash setup_env.sh
```

2. Em um terminal, inicie o controlador Ryu (exemplo com app simples OpenFlow1.3):

```bash
ryu-manager ryu.app.simple_switch_13
```

3. Em outro terminal, execute a topologia Mininet:

```bash
sudo python3 topology.py
```

Observações
- O `setup_env.sh` tenta instalar pacotes via `apt` e `pip3` em distribuições Debian/Ubuntu.
- Mininet e Ryu tipicamente exigem privilégios de root para emulação de rede.
- Edite `topology.py` para ajustar a topologia conforme as instruções da fase seguinte.

Próximo passo
- Implementar a topologia específica solicitada e documentar o procedimento de teste.
