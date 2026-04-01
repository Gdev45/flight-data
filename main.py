#!/usr/bin/env python3
# main.py

import requests
from datetime import datetime, timezone
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from rich.panel import Panel
from rich.text import Text

console = Console()


def header():
    txt = Text(
        "✈ Flight Data — Terminal Edition ✈",
        justify="center",
        style="bold white on blue"
    )
    console.print(Panel(txt, border_style="bright_magenta", title="Welcome"))


def find_flights(q):
    url = "https://opensky-network.org/api/states/all"

    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        data = r.json()
    except Exception as err:
        console.print(f"[red]Failed to fetch data:[/red] {err}")
        return

    results = []

    for s in data.get("states", []):
        callsign = (s[1] or "").strip()

        if not callsign or q.upper() not in callsign.upper():
            continue

        try:
            last_seen = datetime.fromtimestamp(s[4], timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
        except:
            last_seen = "N/A"

        results.append({
            "callsign": callsign,
            "icao": s[0],
            "country": s[2],
            "alt": s[7] if s[7] else "N/A",
            "seen": last_seen,
            "lat": s[6],
            "lon": s[5],
        })

    if not results:
        console.print(f"[yellow]No flights found for '{q}'[/yellow]")
        return

    table = Table(title=f"Flights matching '{q}'", show_lines=True)

    cols = ["Callsign", "ICAO24", "Country", "Altitude (m)", "Last Seen", "Latitude", "Longitude"]
    for c in cols:
        table.add_column(c, justify="center")

    for f in results:
        table.add_row(
            f["callsign"],
            f["icao"],
            f["country"],
            str(f["alt"]),
            f["seen"],
            str(f["lat"]),
            str(f["lon"]),
        )

    console.print(table)


def main():
    header()

    while True:
        q = Prompt.ask("\nCallsign (or 'exit')")
        if q.lower() == "exit":
            console.print("[green]bye[/green]")
            break

        find_flights(q)


if __name__ == "__main__":
    main()
