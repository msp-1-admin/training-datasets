# training-datasets

Versioned, checksum-verified training datasets for MSP-1 protocol behavior and validation.

## Overview

This repository contains baseline datasets intended to define expected behavior, validation patterns, and edge cases for the MSP-1 protocol.

The datasets are:
- **Model-agnostic** — not tuned to any specific LLM
- **Versioned** — changes are introduced only through new dataset versions
- **Checksum-verified** — integrity can be independently validated
- **Deterministic** — identical inputs produce identical artifacts

This repository is designed to be consumed by humans, tools, and automated systems that require a stable reference for MSP-1 interpretation.

## Repository Structure

training-datasets/
├─ README.md
├─ QUICK_START.md
├─ LICENSE
├─ datasets/
│ └─ baseline/
│ └─ v1.0/
│ ├─ msp1_protocol_behavior_baseline.jsonl
│ ├─ msp1_protocol_validation_subset.jsonl
│ ├─ dataset_metadata.json
│ └─ CHECKSUMS.sha256
└─ tools/
├─ convert_from_existing.py
└─ msp1_protocol_dataset_utils.py


## Dataset Versioning

- Dataset versions are immutable once published.
- Any change requires a new version directory (e.g. `v1.1`, `v2.0`).
- Existing version contents MUST NOT be modified.
- Integrity is verified via the accompanying `CHECKSUMS.sha256` file.


## Integrity Verification

Each dataset version includes a `CHECKSUMS.sha256` file.

Consumers are expected to verify checksums before use to ensure dataset integrity and provenance.

## License

All datasets and tooling in this repository are released under the Apache License, Version 2.0, unless otherwise noted.
