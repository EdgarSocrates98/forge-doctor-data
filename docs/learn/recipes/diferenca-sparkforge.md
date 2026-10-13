# Receita — Doctor Data vs Spark Forge: qual usar?

**O quê:** Forge Doctor Data diagnostica **projetos** de engenharia de
dados (repos com dbt, Airflow, Glue, Iceberg, Kafka, …). Spark Forge
(AWS/Azure) diagnostica **workloads** Spark e sua infra.
**Por que:** escolher a forja errada responde a pergunta errada — repo vs
run, estático vs evidência de runtime.
**Quando:** ao abrir um repo novo e decidir qual forja instalar.
**Quando não:** quando os dois se aplicam — pipeline PySpark no Glue é
diagnosticado pelo Doctor (repo) **e** tunado pelo Spark Forge (job).

## Passo a passo

| Pergunta | Forja | Verbo inicial |
|---|---|---|
| "o que tem de errado neste repo de dados?" | Doctor Data | `forge-doctor-data scan .` |
| "por que este job Glue está lento/caro?" | Spark Forge AWS | `sparkforge-aws analyze …` |
| "e no Azure/Databricks?" | Spark Forge Azure | `sparkforge-azure analyze …` |
| "esta DAG/DAG factory está bem formada?" | Doctor Data | `forge-doctor-data airflow inspect` |

```bash
forge-doctor-data scan .            # repo: checks estáticos, findings citáveis
forge-doctor-data compatibility     # riscos de migração por runtime detectado
```

## Saída esperada / interpretação

Doctor emite findings por check com evidência em arquivo; Spark Forge emite
fatos sobre artefatos de run (plan, event log, cluster dumps).

## Verificação

`forge-doctor-data checks` lista as categorias cobertas — se a pergunta é
sobre código/repo e a categoria existe, é Doctor.

## Limitações

Doctor não conecta em AWS/Azure nem executa pipelines; evidência de runtime
é importada (`runtime`, `collector`) — correlação ≠ causação vale aqui
também.

## Erros comuns

| Sintoma | Causa | Ação |
|---|---|---|
| "scan não achou o gargalo" | gargalo vive no run, não no repo | Spark Forge sobre o event log |
| queria lint de SQL | fora do escopo estático | `quality`/`schema` cobrem contratos |

## Uso por agentes

`the-forge` (hub) roteia "diagnosticar X" para a forja certa; o agente não
precisa escolher à mão.
