# ESP32 Wi-Fi Recon Dashboard — experimental workbench

**Status:** Experimental. The host-side Python collector has been run successfully on the user's hardware. The browser dashboard is still unresolved and is not marked as a completed project.

**Board:** ESP32-DevKitC-32UE / ESP32-WROOM-32UE  
**Radio scope:** Original ESP32 2.4 GHz Wi-Fi only  
**Firmware family tested with the collector:** ESP32 Arduino Wi-Fi AP + HTTP JSON API, exposing \`/api/status\`, \`POST /api/scan\`, and \`/api/networks\`.

This folder is intentionally outside the completed-project catalogue. Do not count it as a verified project until the dashboard UI is fixed and the complete workflow is retested.

## What is here

- \`esp32_wifi_collector.py\` — laptop-side Python collector. It asks the ESP32 to perform passive scans, polls until each scan completes, then appends observations to CSV.
- \`requirements.txt\` — optional chart dependency. Collection itself uses the Python standard library; Matplotlib is used for PNG charts.
- \`VALIDATION.md\` — observed test results and known limitations.

The firmware source is not included in this experiment snapshot because the browser UI has not yet been verified as working. Keep the current local Arduino sketch separately until the firmware/dashboard is ready for a reproducible commit.

## Features verified in the Python collector

- Connects to the ESP32 local HTTP API.
- Starts a passive all-channel scan using \`POST /api/scan\`.
- Polls \`/api/networks\` until \`scanRunning\` becomes false.
- Saves timestamp, scan number, uptime, SSID, BSSID, RSSI, channel and advertised authentication mode to CSV.
- Generates a signal-strength-over-time chart and latest-scan channel distribution when Matplotlib is installed.

The collector records only broadcast access-point metadata. It does not attempt to join networks, capture user traffic, or obtain passwords.

## Prerequisites

- ESP32 firmware running an HTTP server at the configured host address.
- Firmware API contract:
  - \`GET /api/status\` returns JSON including \`uptimeMs\`.
  - \`POST /api/scan\` starts an asynchronous passive scan.
  - \`GET /api/networks\` returns \`scanRunning\`, \`scanNumber\`, \`uptimeMs\`, \`count\`, and a \`networks\` array. Each network object includes \`ssid\`, \`bssid\`, \`rssi\`, \`channel\`, and \`auth\`.
- Python 3.9 or newer.
- Laptop connected to the ESP32 access point or otherwise able to reach its API.

The example host is \`192.168.4.1\`. Change it if your firmware uses a different address. Configure your own AP credentials in the local firmware; do not commit real Wi-Fi passwords or private network inventories.

## Fedora setup

From this folder:

~~~bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
~~~

Run ten scans, spaced five seconds apart:

~~~bash
python esp32_wifi_collector.py --host 192.168.4.1 --scans 10 --interval 5
~~~

For a different collection length:

~~~bash
python esp32_wifi_collector.py --host 192.168.4.1 --scans 20 --interval 10 --timeout 90
~~~

The collector creates a \`wifi_recon_data/\` directory (unless \`--output-dir\` is specified) containing a timestamped CSV and, when Matplotlib is installed and observations exist:

- \`signal_strength.png\`
- \`channel_distribution.png\`

Keep generated CSV files and raw SSID/BSSID observations local. Review and anonymize the data before sharing it.

## Current known issue: browser dashboard

The user's ESP32 scanner/API path and Python collector have produced successful observations. However, the V3.3 browser screenshot still shows **Connecting…**, empty metric cards and an empty network table. Therefore:

- Python collection is validated for the tested API-compatible firmware session.
- The V3.3 browser dashboard is not validated and must not be described as fixed.
- The currently verified scan result history is separate from the browser UI state.
- This workbench must remain outside \`catalog/projects.json\` and \`catalog/PROJECT_INDEX.csv\` until the dashboard is resolved and the whole project is retested.

See [VALIDATION.md](VALIDATION.md) for exact observed evidence and scope.

## Responsible-use and privacy notes

Use passive discovery only on networks and devices where observation is authorized. SSIDs and BSSIDs may reveal nearby homes, people or organizations. Do not publish raw scan inventories, precise location data, AP passwords, tokens or other credentials. No deauthentication, jamming, credential collection or network joining is implemented by this collector.
