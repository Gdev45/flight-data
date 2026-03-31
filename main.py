# flight_data_terminal_boxed.py
import requests
from datetime import datetime, timezone
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from rich.panel import Panel
from rich.text import Text

console = Console()

def display_header():
    header_text = Text("✈ Flight Data — Terminal Edition ✈", justify="center", style="bold white on blue")
    panel = Panel(header_text, expand=True, border_style="bright_magenta", title="[bold yellow]Welcome![/bold yellow]")
    console.print(panel)

def search_flights_by_callsign(query):
    url = "https://opensky-network.org/api/states/all"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        console.print(f"[red]Error fetching data:[/red] {e}")
        return

    matches = []
    for state in data.get("states", []):
        callsign = (state[1] or "").strip()
        icao24 = state[0]
        origin_country = state[2]
        lat = state[6]
        lon = state[5]
        altitude = state[7]
        last_seen = state[4]

        if callsign and query.upper() in callsign.upper():
            last_seen_time = datetime.fromtimestamp(last_seen, timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
            matches.append({
                "Callsign": callsign,
                "ICAO24": icao24,
                "Country": origin_country,
                "Altitude (m)": altitude if altitude else "N/A",
                "Last Seen": last_seen_time,
                "Latitude": lat,
                "Longitude": lon
            })

    if not matches:
        console.print(f"[yellow]No airborne flights found for callsign containing '{query}'.[/yellow]")
        return

    table = Table(title=f"Airborne Flights Matching '{query}'", show_lines=True)
    for col in ["Callsign", "ICAO24", "Country", "Altitude (m)", "Last Seen", "Latitude", "Longitude"]:
        table.add_column(col, justify="center")
    
    for f in matches:
        table.add_row(
            f["Callsign"],
            f["ICAO24"],
            f["Country"],
            str(f["Altitude (m)"]),
            f["Last Seen"],
            str(f["Latitude"]),
            str(f["Longitude"])
        )

    console.print(table)

def main():
    display_header()
    while True:
        query = Prompt.ask("\nEnter callsign (or part of it) or 'exit' to quit")
        if query.lower() == "exit":
            console.print("[green]Goodbye![/green]")
            break
        search_flights_by_callsign(query)

if __name__ == "__main__":
    main()


    #!/usr/bin/env python3
def main():
    print("Flight Data CLI running!")
    # your existing code here

if __name__ == "__main__":
    main()