# Receita — rodar um subset de checks com a política certa

**O quê:** `--check`, `--ignore`, `--files`, `--profile` controlam escopo e
severidade do `scan`.
**Por que:** um repo legado pede recorte; CI pede política estável.
**Quando:** filtrar categoria, suprimir check, escanear arquivos-alvo.
**Quando não:** supressão para esconder dívida — `--ignore` é explícito e
auditável; prefira suppressions declaradas no config.

## Passo a passo

```bash
forge-doctor-data checks                      # o catálogo de checks
forge-doctor-data scan . --check <categoria>
forge-doctor-data scan . --profile strict
forge-doctor-data scan . -F path/para/arquivos
```

Profiles reais (do `--help`): `default | strict | security |
spark-performance | glue-migration` — cada um muda a política de severidade.

## Interpretação

`--check` limita a categoria; `--ignore` suprime um id; `--files` ancora o
relatório; `--profile` muda o julgamento sem mudar os facts.

## Verificação

`doctor` reporta `1 suppressions, N rule overrides` — as suppressions
declaradas aparecem lá, não escondidas.

## Limitações

O catálogo é versionado — nomes de checks mudam entre releases;
`checks` lista os ids válidos da sua versão.

## Erros comuns

| Sintoma | Causa | Ação |
|---|---|---|
| `unknown check` | id errado | `checks` lista os válidos |
| profile sem efeito | facts sem trigger da regra | findings dependem de facts |

## Uso por agentes

CI: `--profile <politica> --format json`; local: `scan .` interativo.
