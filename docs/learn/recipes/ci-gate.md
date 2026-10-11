# Receita — usar o Doctor como gate de CI

**O quê:** `scan` em modo máquina (`--format json`, `--emit sarif`,
`--baseline --new-only`) com exit code que reflete a política.
**Por que:** findings em PR devem ser gate, não ruído — SARIF sobe para a
aba Security do GitHub, `--new-only` falha só no que o PR introduziu.
**Quando:** pipeline de PR/merge num repo de dados.
**Quando não:** diagnóstico interativo — aí é TUI/host, não CI.

## Passo a passo

```bash
forge-doctor-data scan . --format json -o report.json
forge-doctor-data scan . --emit sarif:results.sarif --emit html:report.html
forge-doctor-data scan . --baseline origin/main --new-only   # gate de PR
forge-doctor-data suppressions                              # audita o que está suprimido
```

No workflow (GitHub Actions): rode o scan, suba `results.sarif` com
`github/codeql-action/upload-sarif`, e deixe o exit code do `--new-only`
quebrar o job.

## Saída esperada / interpretação

JSON com `findings[]` citando `CHECK-ID` + evidência; SARIF aceito pelas
ferramentas de code scanning; exit 0 sem violations de erro, 1 com.

## Verificação

Localmente: `scan . --baseline HEAD~1 --new-only; echo exit=$?` — um PR sem
novos findings sai 0.

## Limitações

`--baseline` precisa de history do git (fetch depth >1 no runner). Scan é
estático — não substitui testes de pipeline.

## Erros comuns

| Sintoma | Causa | Ação |
|---|---|---|
| baseline não acha a ref | shallow clone | `fetch-depth: 0` no checkout |
| findings demais no PR | gate sem `--new-only` | adicione `--baseline --new-only` |

## Uso por agentes

O relatório JSON é o artefato que `diff_findings` (MCP) compara entre runs.
