# Tutorial — primeira execução real (forge-doctor-data)

Task-first: do zero ao primeiro resultado em minutos. Todos os exemplos
abaixo são classificados — rode os `offline` sem credencial nenhuma.

## 1. Instalar (offline)

```bash
git clone <forge-doctor-data>
cd forge-doctor-data
./setup.sh        # Windows: .\setup.ps1
```

`setup.sh` cria a venv, constrói o wheel e publica o launcher — sem rede
além do download de dependências Python (uma vez).

## 2. Descobrir (offline)

```bash
forge-doctor-data
```

Sem argumentos o CLI mostra o resumo do produto e os comandos mais usados
— nunca um erro, nunca uma mutação. `forge-doctor-data --help` aprofunda.

## 3. Primeiro comando (offline)

```bash
forge-doctor-data scan .
```

varre o projeto e emite findings determinísticos.

## 4. Segundo passo (offline)

```bash
forge-doctor-data checks
```

lista os checks disponíveis.

## 5. Instalar nos hosts (mutação confirmada)

```bash
forge-doctor-data install --dry-run     # plano: nada é escrito
forge-doctor-data install --yes         # aplica após aprovar o plano
```

instala a integração nos hosts. `--dry-run` antes de `--yes` é o padrão do ecossistema.

## 6. Verificar (offline)

```bash
forge-doctor-data install mcp-verify
```

Verificação real: handshake MCP → `tools/list` → `tools/call` segura →
saída limpa do processo. Um `FAIL` aqui vem com `stderr_tail` e
`process.exit_code` — é diagnóstico, não enfeite.

## 7. Próximo passo

```bash
forge-doctor-data explain <CHECK-ID>
```

explica um finding específico.

## Classificação dos exemplos

| Exemplo | Classe |
|---|---|
| setup.sh / clone | offline (precisa rede só p/ deps Python) |
| `forge-doctor-data` bare, help, capabilities | offline |
| analyze/scan/judge locais | offline — nunca toca credencial |
| install --dry-run/--yes | offline, mutação no disco local |
| mcp-verify | offline, spawna o servidor MCP local |
| collect */ chamadas de cloud | **credenciais de cloud necessárias** |
| uso via Claude/Devin/Codex | **requer host instalado** |

## Erros comuns

| Sintoma | Causa | Ação |
|---|---|---|
| `command not found: forge-doctor-data` | launcher fora do PATH ou shell velha | abra terminal novo; rode `./setup.sh` de novo |
| `FORGE-INSTALL-LOCKED` | instalação concorrente/interrompida | lock expira e é recuperado sozinho; repita |
| `FORGE-INSTALL-PLAN-NOT-APPROVED` | mutação sem `--yes` | rode `--dry-run`, depois `--yes` |
| MCP `FAIL` com stderr | dependência ausente (ex.: extra `mcp`) | instale o extra e repita `mcp-verify` |

Mais: [../installation/troubleshooting.md](../installation/troubleshooting.md).
