"""Vendor a real OSS slice into ``golden/<name>/repo`` (RC hardening, Phase 2).

Real entries are vendored, never fetched at test time. This tool is the
documented way they get in: it downloads a fixed file list from an upstream
repository at a pinned commit SHA, records the SHA-256 of every vendored
byte, fetches the upstream ``LICENSE``, and prints the manifest fragment to
merge into ``golden/manifest.json``.

Provenance is a trust boundary, so nothing is implicit: the file list, the
commit and the license are declared up front, and every byte on disk is
hash-verifiable by ``tests/unit/test_corpus_manifest.py``.

Usage::

    python tools/vendor_golden.py --list
    python tools/vendor_golden.py --slice kafka-cluster-configs
    python tools/vendor_golden.py --all
"""

from __future__ import annotations

import hashlib
import json
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GOLDEN = ROOT / "golden"

_RAW = "https://raw.githubusercontent.com/{repo}/{sha}/{path}"

# name -> upstream repository, pinned commit, file list (upstream-relative
# paths; the slice mirrors the upstream layout inside repo/).
SLICES: dict[str, dict[str, object]] = {
    "spark-py-examples": {
        "upstream_repository": "apache/spark",
        "commit_sha": "f6953f77e61359bffca4e7b11818d05cd724194b",
        "files": [
            "examples/src/main/python/pi.py",
            "examples/src/main/python/wordcount.py",
            "examples/src/main/python/streaming/network_wordcount.py",
            "examples/src/main/python/sql/basic.py",
        ],
    },
    "iceberg-spark-env": {
        "upstream_repository": "databricks/docker-spark-iceberg",
        "commit_sha": "cf617dc29e8672792e76b9bcf6017af52f570020",
        "files": [
            "spark/spark-defaults.conf",
            "spark/.pyiceberg.yaml",
            "spark/requirements.txt",
            "spark/Dockerfile",
        ],
    },
    "kafka-python-clients": {
        "upstream_repository": "confluentinc/confluent-kafka-python",
        "commit_sha": "7f2e72f3db14647b163ee5fa7283d674eda194f3",
        "files": [
            "examples/consumer.py",
            "examples/producer.py",
            "examples/avro_producer.py",
            "examples/avro_consumer.py",
        ],
    },
    "flink-pyflink-examples": {
        "upstream_repository": "apache/flink",
        "commit_sha": "6eeffe83da9c9ac130c7591243b78c6820a8b3ca",
        "files": [
            "flink-python/pyflink/examples/datastream/word_count.py",
            "flink-python/pyflink/examples/datastream/streaming_word_count.py",
            "flink-python/pyflink/examples/datastream/event_time_timer.py",
            "flink-python/pyflink/examples/datastream/state_access.py",
        ],
    },
    "trino-server-dev-etc": {
        "upstream_repository": "trinodb/trino",
        "commit_sha": "ee2cedd174cc28ec1eef756d181a7d7342993ef1",
        "files": [
            "testing/trino-server-dev/etc/config.properties",
            "testing/trino-server-dev/etc/jvm.config",
            "testing/trino-server-dev/etc/log.properties",
            "testing/trino-server-dev/etc/access-control.properties",
            "testing/trino-server-dev/etc/catalog/hive.properties",
            "testing/trino-server-dev/etc/catalog/iceberg.properties",
            "testing/trino-server-dev/etc/catalog/jmx.properties",
            "testing/trino-server-dev/etc/catalog/blackhole.properties",
        ],
    },
    "elasticsearch-terraform-module": {
        "upstream_repository": "cloudposse/terraform-aws-elasticsearch",
        "commit_sha": "0fedd88334c54a67eb73fe7059b6c556ca25060d",
        "files": [
            "context.tf",
            "elasticsearch_domain.tf",
            "opensearch_domain.tf",
            "main.tf",
            "outputs.tf",
            "variables.tf",
            "versions.tf",
        ],
    },
    "glue-terraform-example": {
        "upstream_repository": "cloudposse/terraform-aws-glue",
        "commit_sha": "d53e4934ac7f4d6477ec735b26b86339a2c4fb6b",
        "files": [
            "examples/complete/context.tf",
            "examples/complete/fixtures.us-east-2.tfvars",
            "examples/complete/main.tf",
            "examples/complete/outputs.tf",
            "examples/complete/providers.tf",
            "examples/complete/variables.tf",
            "examples/complete/versions.tf",
            "examples/complete/scripts/data_cleaning.py",
        ],
    },
}


def _fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "forge-doctor-data-vendor"})
    with urllib.request.urlopen(req, timeout=30) as resp:  # pinned public URLs
        return resp.read()


def vendor(name: str) -> dict[str, object]:
    spec = SLICES[name]
    repo = str(spec["upstream_repository"])
    sha = str(spec["commit_sha"])
    files = list(spec["files"])  # type: ignore[arg-type]
    repo_dir = GOLDEN / name / "repo"
    vendored: list[dict[str, str]] = []
    for rel in files:
        url = _RAW.format(repo=repo, sha=sha, path=rel)
        data = _fetch(url)
        target = repo_dir / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        vendored.append(
            {
                "path": rel,
                "upstream_path": rel,
                "sha256": hashlib.sha256(data).hexdigest(),
                "bytes": str(len(data)),
            }
        )
        print(f"  {rel}: {len(data)} bytes")
    license_path = license_data = None
    for candidate in ("LICENSE", "LICENSE.txt", "LICENSE.md"):
        try:
            license_data = _fetch(_RAW.format(repo=repo, sha=sha, path=candidate))
            license_path = candidate
            break
        except urllib.error.HTTPError:
            continue
    if license_data is None or license_path is None:
        raise RuntimeError(f"no LICENSE found at {repo}@{sha}")
    license_target = repo_dir / "LICENSE"
    license_target.write_bytes(license_data)
    vendored.append(
        {
            "path": "LICENSE",
            "upstream_path": license_path,
            "sha256": hashlib.sha256(license_data).hexdigest(),
            "bytes": str(len(license_data)),
        }
    )
    print(f"  LICENSE: {len(license_data)} bytes")
    return {
        "upstream_repository": repo,
        "upstream_url": f"https://github.com/{repo}",
        "commit_sha": sha,
        "vendored_files": vendored,
    }


def main(argv: list[str]) -> int:
    if "--list" in argv:
        for name, spec in SLICES.items():
            print(f"{name}: {spec['upstream_repository']} ({len(spec['files'])} files)")  # type: ignore[arg-type]
        return 0
    selected = sorted(SLICES) if "--all" in argv else []
    if "--slice" in argv:
        name = argv[argv.index("--slice") + 1]
        if name not in SLICES:
            print(f"unknown slice {name!r}; use --list", file=sys.stderr)
            return 2
        selected = [name]
    if not selected:
        print("usage: vendor_golden.py --list | --slice <name> | --all", file=sys.stderr)
        return 2
    for name in selected:
        print(f"vendoring {name} ...")
        fragment = vendor(name)
        print(json.dumps({"name": name, **fragment}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
