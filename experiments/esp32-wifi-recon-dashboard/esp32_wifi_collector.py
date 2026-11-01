#!/usr/bin/env python3
"""Collect ESP32 Wi-Fi scan history into CSV and create local visualizations.

Uses only Python's standard library for collection. matplotlib is optional and
is used only to render PNG charts after collection.

Example:
  python3 esp32_wifi_collector.py --host 192.168.4.1 --scans 10 --interval 5
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
import time
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

CSV_FIELDS = [
    "timestamp_local",
    "scan_number",
    "uptime_ms",
    "ssid",
    "bssid",
    "rssi_dbm",
    "channel",
    "auth",
]


def api_get(base_url: str, endpoint: str, timeout: float) -> dict[str, Any]:
    request = Request(f"{base_url}{endpoint}", headers={"Accept": "application/json"})
    with urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def api_post(base_url: str, endpoint: str, timeout: float) -> dict[str, Any]:
    request = Request(
        f"{base_url}{endpoint}",
        data=b"",
        method="POST",
        headers={"Accept": "application/json"},
    )
    try:
        with urlopen(request, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        try:
            detail = json.loads(body)
        except json.JSONDecodeError:
            detail = {"error": body or str(exc)}
        raise RuntimeError(detail.get("error", f"HTTP {exc.code}")) from exc


def wait_for_scan(base_url: str, timeout: float, poll_interval: float = 0.75) -> dict[str, Any]:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        data = api_get(base_url, "/api/networks", timeout=min(timeout, 5.0))
        if not data.get("scanRunning", False):
            return data
        time.sleep(poll_interval)
    raise TimeoutError(f"ESP32 scan did not finish within {timeout:.0f} seconds")


def append_scan(writer: csv.DictWriter, scan: dict[str, Any]) -> int:
    timestamp = datetime.now().astimezone().isoformat(timespec="seconds")
    count = 0
    for network in scan.get("networks", []):
        writer.writerow(
            {
                "timestamp_local": timestamp,
                "scan_number": scan.get("scanNumber", ""),
                "uptime_ms": scan.get("uptimeMs", ""),
                "ssid": network.get("ssid", ""),
                "bssid": network.get("bssid", ""),
                "rssi_dbm": network.get("rssi", ""),
                "channel": network.get("channel", ""),
                "auth": network.get("auth", ""),
            }
        )
        count += 1
    return count


def create_visualizations(csv_path: Path, output_dir: Path) -> None:
    try:
        import matplotlib.dates as mdates
        import matplotlib.pyplot as plt
    except ImportError:
        print("\nmatplotlib is not installed; CSV collection succeeded, charts skipped.")
        print("Install it in a virtual environment: python -m pip install matplotlib")
        return

    with csv_path.open("r", newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        print("No network observations were collected; no charts generated.")
        return

    by_bssid: dict[str, list[tuple[datetime, int, str]]] = defaultdict(list)
    latest_scan_number = max(int(row["scan_number"]) for row in rows if row["scan_number"])
    latest_rows = [row for row in rows if int(row["scan_number"]) == latest_scan_number]

    for row in rows:
        try:
            observed_at = datetime.fromisoformat(row["timestamp_local"])
            rssi = int(row["rssi_dbm"])
            bssid = row["bssid"]
            if bssid:
                by_bssid[bssid].append((observed_at, rssi, row.get("ssid", "")))
        except (ValueError, KeyError):
            continue

    # Plot up to six APs with the most observations to keep the chart readable.
    selected = sorted(by_bssid.items(), key=lambda item: len(item[1]), reverse=True)[:6]
    if selected:
        fig, ax = plt.subplots(figsize=(11, 5.5))
        for bssid, observations in selected:
            observations.sort(key=lambda item: item[0])
            label = observations[-1][2] or "Hidden SSID"
            label = f"{label[:18]} ({bssid[-5:]})"
            ax.plot(
                [point[0] for point in observations],
                [point[1] for point in observations],
                marker="o",
                linewidth=1.5,
                label=label,
            )
        ax.set_title("ESP32 Wi-Fi signal strength over time")
        ax.set_xlabel("Collection time")
        ax.set_ylabel("RSSI (dBm) — closer to 0 is stronger")
        ax.grid(True, alpha=0.3)
        ax.legend(loc="best", fontsize=8)
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M:%S"))
        fig.autofmt_xdate()
        fig.tight_layout()
        signal_path = output_dir / "signal_strength.png"
        fig.savefig(signal_path, dpi=150)
        plt.close(fig)
        print(f"Saved chart: {signal_path}")

    channel_counts = Counter()
    for row in latest_rows:
        try:
            channel_counts[int(row["channel"])] += 1
        except (ValueError, KeyError):
            continue
    if channel_counts:
        fig, ax = plt.subplots(figsize=(9, 4.5))
        channels = sorted(channel_counts)
        ax.bar([str(channel) for channel in channels], [channel_counts[channel] for channel in channels])
        ax.set_title(f"Access points by channel — scan #{latest_scan_number}")
        ax.set_xlabel("2.4 GHz channel")
        ax.set_ylabel("Number of access points")
        ax.grid(axis="y", alpha=0.3)
        fig.tight_layout()
        channel_path = output_dir / "channel_distribution.png"
        fig.savefig(channel_path, dpi=150)
        plt.close(fig)
        print(f"Saved chart: {channel_path}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Collect Wi-Fi scan observations from your ESP32 dashboard."
    )
    parser.add_argument("--host", default="192.168.4.1", help="ESP32 AP address (default: 192.168.4.1)")
    parser.add_argument("--scans", type=int, default=10, help="Number of scans to collect (default: 10)")
    parser.add_argument("--interval", type=float, default=5.0, help="Seconds between completed scans (default: 5)")
    parser.add_argument("--timeout", type=float, default=60.0, help="Maximum seconds to wait for each scan")
    parser.add_argument("--output-dir", default="wifi_recon_data", help="Folder for CSV and PNG outputs")
    args = parser.parse_args()

    if args.scans < 1:
        parser.error("--scans must be at least 1")
    if args.interval < 0 or args.timeout <= 0:
        parser.error("--interval must be >= 0 and --timeout must be > 0")

    base_url = f"http://{args.host.strip().rstrip('/')}"
    output_dir = Path(args.output_dir).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_path = output_dir / f"esp32_wifi_scans_{stamp}.csv"

    print(f"ESP32 endpoint: {base_url}")
    print(f"CSV output:     {csv_path}")
    print("Make sure this laptop is connected to the ESP32-LAB-04 Wi-Fi network.\n")

    try:
        health = api_get(base_url, "/api/status", timeout=5.0)
        print(f"Connected. ESP32 uptime: {health.get('uptimeMs', 0) / 1000:.1f}s")
    except (URLError, TimeoutError, OSError, json.JSONDecodeError) as exc:
        print(f"Cannot reach ESP32 at {base_url}: {exc}", file=sys.stderr)
        print(
            "Check that you are connected to the ESP32 hotspot and that the API responds.",
            file=sys.stderr,
        )
        return 2

    total_observations = 0
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_FIELDS)
        writer.writeheader()
        for index in range(args.scans):
            print(f"[{index + 1}/{args.scans}] Starting passive all-channel scan…")
            try:
                api_post(base_url, "/api/scan", timeout=5.0)
                result = wait_for_scan(base_url, timeout=args.timeout)
            except (RuntimeError, URLError, TimeoutError, OSError, json.JSONDecodeError) as exc:
                print(f"Scan failed: {exc}", file=sys.stderr)
                return 3

            found = len(result.get("networks", []))
            total_observations += append_scan(writer, result)
            handle.flush()
            print(f"     Scan #{result.get('scanNumber')}: {found} access points observed")
            if index < args.scans - 1 and args.interval:
                time.sleep(args.interval)

    print(f"\nCollection complete: {args.scans} scans, {total_observations} observations.")
    print(f"CSV saved to: {csv_path}")
    create_visualizations(csv_path, output_dir)
    print("\nDone. The ESP32 firmware also provides browser CSV export at /export.csv.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
