# Uninstall — forge-doctor-data

```bash
forge-doctor-data install uninstall            # remove só arquivos gerenciados
forge-doctor-data install uninstall --purge    # + remove o estado local (.forge-doctor-data/install/)
```

O ledger SHA-256 decide ownership: arquivos que você criou ou modificou
depois da instalação ficam no lugar (reportados como `kept`). Diretórios
que esvaziam são podados; os seus permanecem.
