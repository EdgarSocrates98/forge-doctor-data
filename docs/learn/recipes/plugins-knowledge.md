# Receita — estender o Doctor com plugins e knowledge packs

**O quê:** `plugins` lista/valida plugins externos; `knowledge` gerencia
packs versionados de conhecimento de plataforma.
**Por que:** o núcleo é fechado e determinístico — extensão entra por
contrato declarado, auditável com `plugins validate`/`knowledge verify`.
**Quando:** regra interna da empresa, plataforma não coberta, ou antes de
confiar num pack de terceiro.
**Quando não:** reportar bug do core — isso é issue, não plugin.

## Passo a passo

```bash
forge-doctor-data plugins                 # categorias built-in + externos descobertos
forge-doctor-data plugins list            # instalados com api_version e trust
forge-doctor-data plugins validate        # reprova plugin incompatível/não-carregável
forge-doctor-data plugins doctor          # saúde por plugin (entry point, api_version)
forge-doctor-data knowledge list          # packs embutidos com proveniência
forge-doctor-data knowledge verify        # integridade + flag de staleness (>90d)
forge-doctor-data knowledge info <domínio>  # o que os packs do domínio cobrem
```

## Saída esperada / interpretação

`plugins` mostra categoria e origem; `validate` aponta campos fora do
contrato. `knowledge list` traz proveniência datada — nada é "confie em mim".

## Verificação

`forge-doctor-data doctor` inclui `plugins` e `knowledge packs` nos checks
de saúde — rode depois de instalar um pack novo.

## Limitações

Plugins ficam fora do caminho MCP por padrão (`scan_project` não os ativa
sem `plugins: true`) — o host decide.

## Erros comuns

| Sintoma | Causa | Ação |
|---|---|---|
| plugin não aparece | diretório fora do path de descoberta | veja `plugins` bare para o layout esperado |
| validate reprova | contrato incompleto | o erro cita o campo ausente |

## Uso por agentes

Knowledge packs são o conhecimento versionado que findings citam —
`explain <CHECK-ID>` mostra a fonte datada.
