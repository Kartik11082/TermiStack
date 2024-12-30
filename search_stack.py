import argparse
import json
import subprocess

import requests
from rich.console import Console
from rich.table import Table

from llama_model import LlamaModel

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
    formed_url_1 = "/2.2/search?order=desc"
    formed_url_2 = (
        f"&tagged={tag}&sort=activity&intitle={query}&site={site}&page={page}"
    )
    formed_url = formed_url_1 + formed_url_2  # Combine the two URLs into one.
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
        with open(
            filename,
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(items, file, indent=4)
        console.print(f"[bold green]Results saved to {filename}[/bold green]")
    except Exception as e:
        console.print(f"[bold red]Error saving results: {e}[/bold red]")


def extract_error_message(error_message):
    llamaModel = LlamaModel()
    llamaModel.start_server()
    question = f"What is the error message when running the script and how to solve it. Give me ste by step detailed explanation: {error_message}"
    response = llamaModel.ask_question(question)
    print(f"[bold blue]Detailed explanation: {response}[/bold blue]")
    return "Python module not found"


def execute_script_and_search_error(script_path):
    """
    Executes a Python script and searches StackOverflow if an error occurs.
    """
    try:
        # Run the script using subprocess
        result = subprocess.run(
            ["python", script_path],
            capture_output=True,
            text=True,
            check=True,  # Will raise CalledProcessError if the script fails
            timeout=30,
        )

        # If the script ran successfully, print the output
        console.print(f"[bold green]Script executed successfully![/bold green]")
        console.print(result.stdout)

    except subprocess.CalledProcessError as e:
        # If there was an error, capture the error message
        # Get the error message from stderr
        error_message = extract_error_message(e.stderr.strip())
        # Parse the error message by passing through a fuinction to extract the error message
        console.print(f"[bold red]Error occurred: {error_message}[/bold red]")

        # Search StackOverflow for the error message
        json_response = make_request("python", error_message, "stackoverflow")

        if json_response and "items" in json_response:
            items = json_response["items"]
            print_results(items, 5)  # Print top 5 results

    except subprocess.TimeoutExpired:
        # Handle timeout if the script takes too long
        console.print("[bold red]Error: Script execution timed out.[/bold red]")

    except Exception as e:
        # Catch any other exceptions during script execution
        console.print(
            f"[bold red]An error occurred while executing the script: {str(e)}[/bold red]"
        )


def main():
    """
    Defines command line argument parser.
    Inputs 'search query', 'number of responses to return', 'tags' and 'site'
    from command line arguments. Prints title and link to StackExchange pages.
    """
    try:
        parser = argparse.ArgumentParser()

        # Add arguments
        parser.add_argument("-q", type=str, required=False, help="Search query")
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
        parser.add_argument(
            "-script", type=str, help="Runs the script and searches the error message"
        )

        args = parser.parse_args()

        if args.script:
            print("Running script", args.script)
            # Function call
            execute_script_and_search_error(
                str(args.script),
            )
            return

        # Send request
        if args.q:
            json_response = make_request(args.t, args.q, args.s, args.page)
            if not json_response or "items" not in json_response:
                console.print(
                    "[bold red]No results found or error occurred.[/bold red]"
                )
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
