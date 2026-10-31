# Project lifecycle and inclusion rules

## Single source of truth

The catalogue contains completed work only. The owner explicitly wants ideas that have actually been built—not speculative project lists. A proposed project, bookmark, copied example or untested code is not a catalogue entry.

## Status values

- `in-progress`: a project folder may be used locally during a build, but it must not be added to the completed catalogue/index until the build is complete. Do not commit it as a completed project.
- `built-and-verified`: the intended functionality was tested on the stated physical board or clearly identified simulator, and evidence is recorded.
- `built-with-limitations`: a real build was made but one or more stated requirements did not pass; the limitation is explicit.
- `archived`: a previously documented build is retained but no longer recommended or maintained.

Only `built-and-verified` and `built-with-limitations` belong in the public project catalogue. The current catalogue has one `built-and-verified` project.

## Completion gate

Before a project is added, check all applicable items:

1. Exact board and module recorded.
2. Goal and expected behavior defined.
3. BOM lists quantities and identifies optional parts; India price notes include date/source or say price not recorded.
4. Wiring/pin map is included, or explicitly says no external wiring is needed.
5. Complete source code included and checked against the code used for the build.
6. Installation and step-by-step build instructions are reproducible.
7. Tests, actual results and limitations are written down.
8. Troubleshooting covers observed issues, not invented claims of testing.
9. Official documentation and datasheet references are linked.
10. Metadata and index are updated; validation script passes.

## Evidence discipline

Distinguish `tested`, `not tested`, `not applicable` and `assumed`. Do not report an expected output as an observed result. Do not invent benchmark figures, prices, compatibility or screenshots.

## Price policy (India)

Record INR estimates only when the relevant part was needed for the actual build. Add the date checked and retailer/reference if known. A historic or approximate price must not be presented as a live quote. If a component was already owned and the purchase amount is unknown, write `already owned; price not recorded`.

## Language policy

Use both C/C++ and Python across the library when they fit the project: for example, firmware on a microcontroller and a host-side Python tool. A separate language implementation is not mandatory when it is technically unnecessary. Add each implementation only after it has been built and tested.
