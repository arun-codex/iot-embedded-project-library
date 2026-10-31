# Publish this library to GitHub

Suggested repository: `arun-codex/iot-embedded-project-library`.

The connected GitHub integration available during preparation could inspect and modify existing repositories, but it did not expose a create-repository action. Therefore this local package has **not** been published remotely. Create the empty GitHub repository once, then push this folder.

## Option A — GitHub web UI + Git

1. Open [GitHub new repository](https://github.com/new).
2. Set the repository name to `iot-embedded-project-library`.
3. Choose Public or Private according to your preference.
4. Do not initialize it with a README, `.gitignore` or license (this folder already contains them).
5. Extract this ZIP and open a terminal in the extracted `iot-embedded-project-library` directory.
6. Run:

```bash
git init -b main
git add .
git commit -m "Initial build-first IoT and embedded project library"
git remote add origin https://github.com/arun-codex/iot-embedded-project-library.git
git push -u origin main
```

Git may prompt you to authenticate in a browser or through a credential manager. Do not put a password or personal access token in the command or commit it to the repository.

## Option B — GitHub CLI (`gh`)

After installing and authenticating GitHub CLI (`gh auth login`), run from the repository root:

```bash
git init -b main
git add .
git commit -m "Initial build-first IoT and embedded project library"
gh repo create arun-codex/iot-embedded-project-library --source=. --remote=origin --push
```

GitHub CLI will ask for visibility if it is not provided. You can also add `--public` or `--private` explicitly.
