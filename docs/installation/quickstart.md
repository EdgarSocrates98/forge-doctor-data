# Quickstart — forge-doctor-data

Três comandos:

```bash
git clone <forge-doctor-data repo>
cd forge-doctor-data
./install.sh      # Windows: .\install.ps1 — account runtime + editable CLI
```

Depois, dentro de qualquer projeto:

```bash
cd ~/meu-projeto
forge-doctor-data install
```

Pronto. O que foi instalado: a entrada MCP gerenciada em `.mcp.json`, o
registro `.forge/context/` (manifesto de capacidades + ROUTING) e blocos
`forge:*` nos consumer docs existentes. Os agent specs do forge são
bundled — declarados no manifesto, sem espelho em diretórios de host.

Em diretório vazio, o wizard remove `Current repository` e instala pelo
escopo `Entire workspace`, sem exigir Git ou comandos extras.

## Verificar

```bash
forge-doctor-data install status
forge-doctor-data install doctor
```

Detalhes: [account-installation.md](account-installation.md). Problemas? → [troubleshooting.md](troubleshooting.md)
