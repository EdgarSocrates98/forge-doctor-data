# Receita — instalar o Doctor num projeto

**O quê:** `forge-doctor-data install` projeta o Doctor num escopo
(project|workspace|user): chave MCP gerenciada em `.mcp.json`, marcadores
em AGENTS.md/CLAUDE.md, ledger em `.forge-doctor-data/install/`.
**Por que:** instalação governada com drift auditável e uninstall que só
remove o que o ledger criou.
**Quando:** primeira vez num repo, ou ao adotar em monorepo (workspace).
**Quando não:** experimento rápido — `scan .` funciona sem instalar nada.

## Passo a passo

```bash
forge-doctor-data install --dry-run         # plano, sem escrever
forge-doctor-data install --yes             # aplica no projeto (precisa de repo git)
forge-doctor-data install status            # saúde/drift do que foi instalado
forge-doctor-data install doctor            # checks de saúde da instalação
forge-doctor-data install repair            # restaura assets faltantes do ledger
forge-doctor-data install uninstall         # remove só o que o ledger criou
```

## Saída esperada / interpretação

`install status` retorna `healthy|degraded|broken|unverified` com drift por
arquivo. `unverified` = nunca instalado neste escopo — é estado honesto,
não erro.

## Verificação

`forge-doctor-data install mcp-verify` faz handshake real com o servidor
MCP configurado (PASS/FAIL), não só "arquivo existe".

## Limitações

Sem mirrors de skills/agents hoje — a instalação gerencia a chave MCP e os
marcadores de documentação. Escopo `user` grava em `~/.forge-doctor-data`.

## Erros comuns

| Sintoma | Causa | Ação |
|---|---|---|
| `FORGE-INSTALL-NOT-A-REPO` | fora de repo git | `git init` ou `--root` num repo |
| `FORGE-INSTALL-PLAN-NOT-APPROVED` | faltou `--yes` | revise o dry-run, depois `--yes` |
| drift `modified` | arquivo gerenciado editado à mão | `install repair` (preserva conteúdo de usuário) |

## Uso por agentes

`install mcp-verify` é a prova "MCP configurado → MCP verificado"; hosts
leem `.mcp.json` na raiz do projeto.
