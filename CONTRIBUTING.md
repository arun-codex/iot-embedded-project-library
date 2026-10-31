# Contributing

This is a personal, build-first project notebook. Add a catalogue entry only after a real build has been tested and documented. Do not add brainstorms, proposed builds, copied tutorials or placeholder projects to the completed-project catalogue.

## Before committing a new project

- Use `_templates/project/README.md` and `_templates/project/metadata.json`.
- Include the complete code that was actually built.
- Record exact board/module and framework versions.
- Include wiring or explicitly state that none is required.
- Record tests and evidence honestly; distinguish expected behavior from observed behavior.
- Add the project to both catalogue indexes.
- Run:

```bash
python3 tools/validate_catalog.py
python3 tools/catalog.py --list
```

Keep secrets, Wi-Fi passwords, tokens, private MAC-address inventories and personal data out of commits. Use `.env` files only when needed and never commit them.
