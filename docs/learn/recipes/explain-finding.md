# Receita — por que este finding disparou?

**O quê:** `forge-doctor-data explain <CHECK-ID>` mostra a cadeia de
evidência e a regra por trás de um finding.
**Por que:** finding sem porquê é ruído; evidence-first é o contrato.
**Quando:** triagem de findings, disputa de falso-positivo, aprendizado.
**Quando não:** silenciar — explain explica, `--ignore`/suppression silencia.

## Passo a passo

```bash
forge-doctor-data scan .                    # coleta os CHECK-IDs
forge-doctor-data explain <CHECK-ID>
```

## Interpretação

Regra + evidência + rationale — o explain justifica; se a evidência estiver
errada, o finding está errado (reporte; o catálogo é versionado).

## Verificação

A evidência citada existe no projeto — o explain aponta arquivo/linha.

## Limitações

Explain cobre a regra disparada — contexto de negócio ("é intencional")
continua decisão humana; nesse caso use suppression declarada, não
`--ignore` repetido.

## Erros comuns

| Sintoma | Causa | Ação |
|---|---|---|
| explain vazio | CHECK-ID de outra versão | `checks` da sua versão |
| finding recorrente | causa-raiz não tratada | explain mostra o pattern |

## Uso por agentes

Agente deve citar `CHECK-ID` + a evidência do explain — nunca parafrasear
a regra de memória.
