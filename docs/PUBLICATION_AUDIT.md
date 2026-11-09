# Pre-publication audit

Checked on **9 November 2026** for a private GAS4 coursework collaboration repository.

## Publication set

Keep the master notebook, personal model entries/common module, course CSV, dependency locks, run/build utilities, bilingual documentation, original brief/templates, allocation figures and actual experiment outputs. The one dataset is shared under `data/` in a Git checkout; each standalone ZIP includes an identical copy.

The private Moodle screenshot, original full-machine package inventory and pre-cleanup backup/history are local-only under `.local_private/`, which Git ignores. The full inventory contained unrelated ROS packages; it is not required to install or run CW2. Caches, virtual environments and duplicate extracted starter directories are ignored.

## Privacy changes

- Removed personal screenshot from the publishable snapshot.
- Redacted home-directory prefixes in recorded and future runtime/provenance output as `<home>`; retained Python/package versions, hardware/thread information and real numerical measurements.
- Configured this repository's Git author email to the matching public account's ID-based GitHub no-reply form. Global Git settings were not changed.
- Replaced the single unpublished initial commit so the reachable publication history does not retain the original private email or excluded screenshot/inventory. Original local history is recoverable from an ignored backup; it is not a remote ref.
- Kept member display names (such as Wenyi and Kiki) because they are used for the requested allocation and contribution record. The repository is not anonymous.

Credential-pattern, email/home-path, suspicious-filename and embedded-archive checks found no publication-blocking credentials in the final tracked content. This records the checks performed rather than a claim that any scanner proves the absence of every possible secret.

## Completeness and execution

- Master notebook: 15 code cells executed successfully in a separate standalone directory, using a fresh Python kernel. No CW1 project files were needed; the installed interpreter's library environment was used.
- Five OLS development metrics reproduce the existing reference within numerical tolerance.
- Shared evaluator reproduces the same metrics after path/privacy-only changes.
- All three personal notebook entries run with training disabled from both a Git-style directory and a ZIP-only directory. No candidate was trained for this audit.
- Every ZIP passes integrity and code/data-content checks; dataset SHA-256 is unchanged.
- Local Markdown links resolve; notebooks validate; Python sources parse.
- Final held-out testing remains unrun. The pending final-test implementation is coursework work, not a missing dependency in this starter repository.

The checks were run on local Linux/Python 3.12, not directly on Windows/macOS/Colab. Machine-readable results are in [publication_audit.json](publication_audit.json).

The original course brief and templates remain useful to the private group. Their presence is not permission to redistribute them publicly. Publish as a **private repository** and invite the group.
