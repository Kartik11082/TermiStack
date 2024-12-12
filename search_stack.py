import argparse
import json
from time import sleep

import requests
from rich.console import Console
from rich.table import Table

# Console for better CLI output
console = Console()

# Colors and text styles for terminal texts
UIElements = {
    "style__CBOLD": "\33[1m",
    "style__CITALIC": "\33[3m",
    "style__CURL": "\33[4m",
    "style__CSELECTED": "\33[7m",
    "color__CBEIGE": "\33[36m",
    "color__CWHITE": "\33[37m",
    "color__Lime": "\33[92m",
    "color__CBLUE": "\33[34m",
    "color__CRED": "\33[31m",
    "color__CREDBG": "\33[41m",
    "__CD": "\033[0m",
}


def make_request(tag, query, site, page=1):
    """
    Sends requests to Stackoverflow and returns a JSON response.
    """
    console.print(
        f"[bold blue]Searching in {site} for '{query}' with tag '{tag}'...[/bold blue]"
    )
    base_url = "https://api.stackexchange.com"
    formed_url = f"/2.2/search?order=desc&tagged={tag}&sort=activity&intitle={query}&site={site}&page={page}"
    stackoverflow_url = base_url + formed_url

    try:
        resp = requests.get(stackoverflow_url, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException as e:
        console.print(f"[bold red]Error fetching data: {e}[/bold red]")
        return None


def print_results(items, number):
    """Pretty print results using rich tables."""
    table = Table(title="Search Results", style="bold green")
    table.add_column("Title", style="cyan", justify="left")
    table.add_column("Link", style="magenta", justify="left")
    table.add_column("Answered", style="green", justify="center")

    for item in items[:number]:
        answered = "\u2713" if item.get("is_answered") else "\u274C"
        table.add_row(item["title"], item["link"], answered)

    console.print(table)


def save_results(items, filename):
    """Save results to a JSON file."""
    try:
        with open(filename, "w") as file:
            json.dump(items, file, indent=4)
        console.print(f"[bold green]Results saved to {filename}[/bold green]")
    except Exception as e:
        console.print(f"[bold red]Error saving results: {e}[/bold red]")


def main():
    """
    Defines command line argument parser.
    Inputs 'search query', 'number of responses to return', 'tags' and 'site'
    from command line arguments. Prints title and link to StackExchange pages.
    """
    try:
        parser = argparse.ArgumentParser()

        # Add arguments
        parser.add_argument("-q", type=str, required=True, help="Search query")
        parser.add_argument(
            "-n", type=int, default=10, help="Number of responses to return"
        )
        parser.add_argument(
            "-t", type=str, default="python", help="Tags for filtering results"
        )
        parser.add_argument(
            "-s", type=str, default="stackoverflow", help="StackExchange site"
        )
        parser.add_argument("-o", type=str, help="Output file to save results")
        parser.add_argument(
            "--page", type=int, default=1, help="Page number for pagination"
        )

        args = parser.parse_args()

        # Send request
        json_response = make_request(args.t, args.q, args.s, args.page)
        if not json_response or "items" not in json_response:
            console.print("[bold red]No results found or error occurred.[/bold red]")
            return

        items = json_response["items"]

        # Print results
        print_results(items, args.n)

        # Save results if output file is specified
        if args.o:
            save_results(items, args.o)

    except Exception as e:
        console.print(f"[bold red]An error occurred: {e}[/bold red]")


if __name__ == "__main__":
    main()
