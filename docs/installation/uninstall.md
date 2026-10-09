# Uninstall — forge-doctor-data

```bash
forge-doctor-data uninstall            # remove só arquivos gerenciados
forge-doctor-data uninstall --purge    # + remove o estado local (.forge-doctor-data/install/)
```

O ledger SHA-256 decide ownership: arquivos que você criou ou modificou
depois da instalação ficam no lugar (reportados como `kept`). Diretórios
que esvaziam são podados; os seus permanecem.
