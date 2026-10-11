# Receita — usar o Doctor pelo seu host de IA (Devin/Claude/Codex)

**O quê:** `forge-doctor-data mcp` serve MCP (JSON-RPC stdio, zero-dep);
`forge-doctor-data hosts` observa os CLIs de host instalados e abre um no
repo.
**Por que:** a pergunta "analise a qualidade deste repo de dados" deve ser
respondida pelo host chamando tools reais — `scan_project`, `explain_rule`,
`get_host_status` — não por comandos decorados.
**Quando:** depois de `install`, para trabalhar dentro do Devin/Claude/Codex.
**Quando não:** batch/CI — aí é `scan` direto, sem host.

## Passo a passo

```bash
forge-doctor-data hosts                     # estado observado dos 4 hosts
forge-doctor-data hosts devin               # um host: binário, versão, auth, integração
forge-doctor-data hosts devin --launch      # abre o Devin neste repo (pede TTY)
forge-doctor-data install mcp-verify        # handshake real com o servidor MCP
forge-doctor-data mcp                       # servidor stdio (o host chama)
```

Dentro do host, peça em linguagem natural: *"rode scan_project neste repo e
me explique o finding mais grave com explain_rule"*.

## Saída esperada / interpretação

`hosts` retorna por host: `NOT_DETECTED|SUPPORTED|NEEDS_LOGIN|READY` +
`launch_command` + integração (`healthy|unverified`). `READY` = host logado
+ instalação saudável. `NEEDS_LOGIN` vem com `login_hint` oficial — o Doctor
nunca pede credencial.

## Verificação

A cadeia real: `install --yes` → `install mcp-verify` PASS → `hosts` READY →
o host lista `forge-doctor-data` entre seus servidores MCP.

## Limitações

MCP é observação: `get_host_status` nunca lança host — `--launch` é fronteira
humana (CLI + TTY). `copilot` não tem subcomando de status documentado —
`logged_in` fica honestamente `null`.

## Erros comuns

| Sintoma | Causa | Ação |
|---|---|---|
| `NEEDS_LOGIN` | host deslogado | rode o `login_hint` (ex.: `devin auth login`) |
| `NOT_DETECTED` | CLI não está no PATH | instale o host ou ajuste PATH |
| `launch_refused: no_tty` | `--launch` fora de terminal | abra num TTY ou rode o `launch_command` |

## Uso por agentes

Tools MCP: `scan_project`, `explain_rule`, `check_compatibility`,
`get_lineage`, `diagnose_log`, `diff_findings`, `get_execution_baseline`,
`get_regressions`, `get_runtime_correlations`, `get_incident_explanation`,
`get_critical_path`, `get_capacity_signals`, `get_portfolio_summary`,
`get_host_status`. Sandbox: `mcp --root <dir>` confina paths de tool.
