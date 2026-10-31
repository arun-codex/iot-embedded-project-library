# IoT & Embedded Systems Project Library

A build-log-driven catalogue of IoT, electronics, embedded and board projects. **A project is added to the catalogue only after it has actually been built and its results have been checked.** Ideas, wish lists and untested code do not count as projects here.

> Current catalogue: **1 built project**. This is intentionally not padded to a target count. The library grows as projects are completed and documented.

## What this repository is

- A searchable index by board, difficulty, category, technology, language and project name.
- A detailed build record for each completed project: purpose, prerequisites, bill of materials, wiring, code, setup, steps, expected result, testing, troubleshooting and references.
- A consistent template and validation tool so future additions are documented the same way.
- India-aware parts guidance in INR where a project needs hardware. Prices are estimates captured when the project is documented; check seller, shipping and stock before buying.

## Browse the catalogue

| Filter | Current contents |
|---|---|
| Boards | ESP32 has one verified project; ESP8266, Arduino and Raspberry Pi Pico are selected for future use but not yet represented by a completed project. |
| Difficulty | Beginner: 1 |
| Categories | Embedded foundations: 1; the other selected categories currently have no completed entries. |
| Languages | C++ / Arduino framework: 1 |

Open [`catalog/projects.json`](catalog/projects.json) for machine-readable metadata or [`catalog/PROJECT_INDEX.csv`](catalog/PROJECT_INDEX.csv) for a spreadsheet-friendly index.

### Search from the terminal

Requires Python 3.9+; no third-party packages are needed.

```bash
python3 tools/catalog.py --list
python3 tools/catalog.py --board ESP32
python3 tools/catalog.py --difficulty beginner
python3 tools/catalog.py --category "Embedded foundations"
python3 tools/catalog.py --search serial
python3 tools/catalog.py --language C++
python3 tools/catalog.py --tag hello-world
```

## Completed projects

### 1. [Hello, ESP32! — serial bring-up](projects/esp32/01-hello-esp32/README.md)

- **Board:** Espressif ESP32-DevKitC-32UE (ESP32-WROOM-32UE module)
- **Difficulty:** Beginner
- **Status:** Built and verified on 31 October 2026
- **Result:** Firmware uploaded successfully; serial output observed at 115200 baud.

This is a board bring-up exercise, not yet a sensor or networked IoT application. It verifies the development toolchain, USB serial connection, upload process and serial monitor.

## Repository structure

```text
.
├── README.md
├── CONTRIBUTING.md
├── catalog/
│   ├── projects.json
│   ├── PROJECT_INDEX.csv
│   ├── BOARDS.json
│   └── CATEGORIES.md
├── projects/
│   └── esp32/
│       └── 01-hello-esp32/
│           ├── README.md
│           ├── metadata.json
│           ├── VALIDATION.md
│           └── src/hello_esp32.ino
├── docs/
│   ├── BOARD_SUPPORT.md
│   └── PROJECT_LIFECYCLE.md
├── _templates/project/
│   ├── README.md
│   └── metadata.json
└── tools/
    ├── catalog.py
    └── validate_catalog.py
```

## Current board scope

The intended board families are ESP32, ESP8266, Arduino and Raspberry Pi Pico. Only the ESP32-DevKitC-32UE has been used and verified in this repository so far. See [`docs/BOARD_SUPPORT.md`](docs/BOARD_SUPPORT.md) for exact status; selected does not mean tested.

## Add a project

1. Build it on real hardware or in a clearly identified simulator.
2. Capture the exact board/module, framework/core version, wiring, dependencies and test evidence.
3. Copy `_templates/project/` into a new folder under `projects/<board>/`.
4. Complete every applicable section. Mark genuinely inapplicable sections as `Not applicable` and explain why.
5. Add its metadata to `catalog/projects.json` and `catalog/PROJECT_INDEX.csv`.
6. Run `python3 tools/validate_catalog.py` and check that `python3 tools/catalog.py --list` shows the project.
7. Commit the documentation and code together.

Do not add planned projects as catalogue entries. A future idea can stay in a personal note outside the completed-project index until it is built.

## Programming-language policy

Support both C/C++ and Python where each is appropriate and actually tested. Microcontroller firmware may use C/C++ while a laptop-side tool may use Python. Do not create a second-language version just to satisfy a checklist; add it only when it has been built and validated. The current serial bring-up sketch is C++ only.

## License

No license has been selected yet, so this repository intentionally has no `LICENSE` file. Choose a license before inviting reuse or publishing it as an open-source project.

## Safety and responsible use

Wireless/security projects must be tested only on devices and networks you own or have explicit permission to assess. Document the permitted scope and avoid disruption, credential collection, covert surveillance or interference. Record privacy implications whenever a project observes nearby devices or networks.

## Sources and documentation style

Prefer manufacturer documentation, official framework references and component datasheets. Project-specific references are recorded in each project's guide. Never claim a feature was tested merely because it appears in a datasheet or example.
