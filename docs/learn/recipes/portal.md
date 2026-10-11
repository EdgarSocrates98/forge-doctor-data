# Receita — operar o Forge Doctor Data pelo portal web local

**O quê:** `forge-doctor-data portal` sobe uma UI web opcional em
`127.0.0.1` (com token de sessão) sobre os serviços reais da forja:
estado da instalação, detecção de hosts, verificação MCP, scan do
projeto e grafo de evidência — a mesma verdade que o CLI reporta.
**Por que:** a jornada "instalar → configurar hosts → verificar MCP →
primeira tarefa" fica visível e guiada, sem sair do modelo de recibos e
confirmações do CLI.
**Quando:** explorar e operar visualmente a forja instalada; ensinar o
fluxo a alguém novo; conferir hosts/MCP num painel.
**Quando não:** automação/CI (use os verbos CLI — saem JSON estável);
acesso remoto sem túnel (o portal só escuta em loopback).

## Passo a passo

```bash
forge-doctor-data portal                 # abre o browser na URL com token
forge-doctor-data portal --no-browser    # só imprime a URL (SSH/remoto)
forge-doctor-data portal --port 8790     # porta fixa
forge-doctor-data portal --root ../meu-projeto   # outro workspace
```

## Saída esperada / interpretação

O servidor imprime a URL já com o token de sessão (`?forge_session=…`).
O dashboard mostra `InstallState` honesto — `DEGRADED`/`NOT_INSTALLED`
são respostas reais, não falha do portal. Aba Install planeja e aplica a
instalação (plano → confirmação → recibo), Hosts mostra a sonda real de
cada host, MCP refaz o handshake e Tasks executa tarefas seguras de
leitura — incluindo `scan`, o diagnóstico real do workspace.

## Verificação

Compare o estado do portal com `forge-doctor-data install status` e
`forge-doctor-data doctor` — devem contar a mesma história, porque leem
a mesma ledger.

## Limitações

A forja não embarca skills/agents de host hoje — essas abas aparecem
vazias de propósito (`unsupported`), não é bug. Toda mutação exige
confirmação explícita e plan token assinado; nada acontece por acidente
de navegação.

## Erros comuns

| Sintoma | Causa | Ação |
|---|---|---|
| `FDD-PORTAL-NO-ASSETS` | assets não vendorizados no checkout | rode `python scripts/vendor.py` no forge-portal |
| health `DEGRADED` após install | check do doctor falhou | `forge-doctor-data doctor` mostra qual |
| intent recusado (`FDD-PORTAL-AMBIGUOUS`) | tarefa fora do conjunto seguro | use um dos verbos seguros listados |
