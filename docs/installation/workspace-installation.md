# Instalação em workspace — forge-doctor-data

Monorepo/pasta com vários repositórios. Duas rotas — a CLI própria ou o
orquestrador (The Forge), que resolve a workspace inteira:

```bash
cd ~/minha-workspace
forge-doctor-data install --scope workspace          # rota própria
# ou via orquestrador:
theforge install auto --scope workspace
# ou membro explícito (repetível):
theforge install auto --scope workspace --member sub/repo
```

Descoberta: diretórios com `.git` ou manifesto de projeto (membros sem
Git contam) até 2 níveis; symlinks/junctions nunca são seguidos. Cada
membro mantém seu próprio estado e ledger isolados — nenhum runtime
duplicado.
Precedência: `project > workspace > user` — instalação local do projeto
vence sempre, e conflitos são reportados, nunca sobrescritos.
