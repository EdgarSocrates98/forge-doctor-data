# Receita — "analise este repo de dados" via agente

**O quê:** `forge-doctor-data agent` emite contexto determinístico e com
orçamento para o host — manifest, context bounded, delta de fingerprints,
evidência lazy.
**Por que:** agente bom recebe resumo citado primeiro e expande sob demanda
— nunca o repo inteiro no prompt.
**Quando:** o host precisa de contexto do projeto sem rodar scan manual.
**Quando não:** diagnóstico humano direto — use `scan`/`advise`.

## Passo a passo

```bash
forge-doctor-data agent manifest            # domínios, riscos, capabilities compactos
forge-doctor-data agent context --budget 8000   # resumo-first dentro do orçamento
forge-doctor-data agent evidence <ref>      # expande UMA referência lazy
forge-doctor-data agent delta               # fingerprints novos/removidos
```

## Saída esperada / interpretação

`manifest` é o mapa; `context` é o resumo que cabe; `evidence` resolve uma
referência por vez — cada peça citável de volta ao arquivo.

## Verificação

`agent context --budget` nunca estoura o orçamento declarado; referências
`evidence` resolvem ou retornam recusa nomeada.

## Limitações

Contexto é derivado do último scan/estado — repo sujo sem scan recente
produz contexto honestamente incompleto.

## Erros comuns

| Sintoma | Causa | Ação |
|---|---|---|
| contexto vazio | projeto nunca scaneado | `scan .` primeiro |
| evidence não resolve | ref de scan antigo | re-rodar `agent manifest` |

## Uso por agentes

Estes quatro subcomandos são a superfície agent-first do Doctor — o host
combina `agent manifest` + tools MCP (`scan_project`, `explain_rule`).
