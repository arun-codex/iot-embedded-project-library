# Validation record — ESP32 Wi-Fi Recon Dashboard workbench

## Status summary

| Component | Status | Evidence |
|---|---|---|
| ESP32 passive scan pipeline | Passed in the supplied test session | Repeated all-channel scans returned changing AP counts. |
| Python collector | Passed in the supplied test session | Completed 10 scans and wrote 45 total observations to CSV. |
| Python CSV output | Passed | Timestamped CSV created. |
| Python visualizations | Passed | \`signal_strength.png\` and \`channel_distribution.png\` created. |
| V3.1 history API | Passed | \`/api/history\` returned HTTP 200 and a scan history record with four AP observations. |
| V3.2 networks/history API | Passed after a scan | \`/api/networks\` and \`/api/history\` returned HTTP 200; history contained four AP observations. |
| V3.3 browser dashboard | **Not passed / unresolved** | Browser still displays “Connecting…” and blank metric cards/table. |

## Python collector test supplied by the user

**Date:** 1 November 2026  
**Host environment:** Fedora Linux, Python virtual environment  
**Command:**

~~~bash
python esp32_wifi_collector.py --host 192.168.4.1 --scans 10 --interval 5
~~~

**Observed output summary:**

~~~text
Collection complete: 10 scans, 45 observations.
CSV saved to: wifi_recon_data/esp32_wifi_scans_20261101_123231.csv
Saved chart: wifi_recon_data/signal_strength.png
Saved chart: wifi_recon_data/channel_distribution.png
~~~

The ten scans reported between two and eight AP observations each. These are observations across scans, not 45 unique access points. The same AP may appear in multiple scans.

Raw SSIDs and BSSIDs are intentionally not reproduced in this public validation record.

## API observations

- The start-scan endpoint returned HTTP 202 Accepted.
- The networks endpoint returned JSON after scan completion.
- The history endpoint returned a stored scan snapshot on V3.1 and V3.2 test sessions.
- In one pre-scan V3.2 request, \`/api/networks\` correctly returned \`count: 0\`; after starting a scan, the history endpoint contained four observations.

These API observations are not proof that the browser UI works.

## Dashboard failure still open

The user's later V3.3 screenshot showed the dashboard title but the connection badge remained at “Connecting…”, metric cards remained blank, and the access-point table showed no data. The dashboard UI has therefore **not** passed end-to-end validation.

Do not mark the dashboard project as complete or add it to the repository's completed-project catalogue until:
1. The root page loads status and network results in the browser.
2. A scan started from the dashboard updates the access-point table and charts.
3. The dashboard history appears after at least two scans.
4. Browser CSV export is checked.
5. The Python collector is rerun against the same final firmware version.

## Local static checks

- \`python3 -m py_compile esp32_wifi_collector.py\`: passed in the authoring environment.
- Physical device test: based on the user's supplied terminal output, not a test performed by the repository maintainer.
- Browser dashboard: unresolved as described above.
