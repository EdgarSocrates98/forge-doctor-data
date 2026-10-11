# Receita — transformar findings em plano de ação

**O quê:** `advise` ordena os findings do scan numa lista citada de ações;
`fix`/`remediate` aplicam as correções seguras.
**Por que:** 50 warnings sem ordenação é ruído — score = severidade +
confiança + cluster + segurança do fix + blast radius.
**Quando:** depois do primeiro scan, para decidir o que atacar primeiro.
**Quando não:** findings sem evidência — investigue com `explain` antes.

## Passo a passo

```bash
forge-doctor-data advise .              # ranking com citação de fingerprints
forge-doctor-data advise . --top 5      # só o top 5
forge-doctor-data advise . --format json
forge-doctor-data explain <CHECK-ID>    # por que a regra existe, quando OK, como corrigir
forge-doctor-data fix --help            # aplicação governada (não é advise)
```

## Saída esperada / interpretação

Cada linha cita fingerprints e entity ids — o ranking é auditável, não
opinião. `--format json` alimenta automação.

## Verificação

Compare `scan . --quiet` (só problemas) com `advise . --top 5`: o topo do
advise deve ser o que você atacaria primeiro.

## Limitações

`advise` é advisory — nunca aplica nada. `fix`/`remediate` são os verbos de
mutação e têm suas próprias guardas.

## Erros comuns

| Sintoma | Causa | Ação |
|---|---|---|
| advise vazio | scan sem findings | `scan .` para confirmar |
| ordem surpreendente | score pesa cluster/blast | `explain <CHECK-ID>` no topo |

## Uso por agentes

O ranking citado é o contexto que o host precisa para propor mudança —
`agent context` carrega o resumo bounded.
