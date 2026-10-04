# Evidence collectors

Collectors are a boundary around external evidence acquisition:

```text
collector → normalized EvidenceBundle → Forge Doctor Data
```

The core `scan` path never imports cloud SDKs, makes network calls, or invokes
collectors. Optional products can implement `EvidenceCollector.collect(root)`
and emit `forge-doctor-data/evidence-bundle@1` records with source, kind,
subject, attributes, observation time, and provenance.

Validate a bundle offline:

```bash
forge-doctor-data collector validate evidence.json
forge-doctor-data collector validate evidence.json --json
```

The first reference adapter should target AWS Glue, CloudWatch, EMR, Athena,
Lake Formation, Step Functions, and applicable streaming services. It belongs
in a separate distribution and must produce normalized evidence only; it must
not move cloud access into `scan`.
