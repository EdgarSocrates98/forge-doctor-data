# Update e repair — forge-doctor-data

## Update

```bash
forge-doctor-data install update --to <versão ou tag pinada>
```

`latest` é recusado por contrato — sempre pin a versão. Sem checkout
registrado o update reporta BLOCKED honestamente.

## Repair

```bash
forge-doctor-data install doctor   # mostra o drift da instalação
forge-doctor-data install repair   # reassegura regiões gerenciadas
```

Repair restaura arquivos gerenciados removidos, reassegura o registry
`.forge/context/` (journal, locks velhos, ROUTING.md) e cura blocos
`forge:forge-doctor-data` dentro de arquivos seus — conteúdo fora do bloco nunca
é tocado. Antes de sobrescrever, um snapshot vai para
`<state_dir>/backups/`. Repair é incremental como a instalação: regiões
íntegras não são reescritas — e a chave `.mcp.json` converge para o argv
absoluto (shim ou `python -m forge_doctor_data`) quando uma instalação
antiga ainda aponta para o comando de PATH.
