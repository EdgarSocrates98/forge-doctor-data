# MCP — forge-doctor-data

Servidor MCP: `forge-doctor-data mcp`

A instalação registra uma entrada gerenciada em `.mcp.json` (chave
`_forge_managed.forge-doctor-data`) — outras entradas suas ficam intactas.

Verificar de verdade (handshake real + tools/list + invocação segura):

```bash
forge-doctor-data install doctor       # saúde da instalação, inclui mcp-handshake
forge-doctor-data install mcp-verify   # só o handshake MCP (PASS/BLOCKED/FAIL)
```

O `install doctor` executa `initialize` → `tools/list` → `tools/call` de
leitura da ferramenta de verificação declarada (`get_execution_baseline`)
e reporta PASS / BLOCKED / FAIL / UNVERIFIED com evidência de processo
(exit, stderr). Nunca infere sucesso de presença de arquivo. O servidor é
stdlib-only — nenhum extra opcional precisa ser instalado.
