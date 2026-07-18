from rich.console import Console
import time

console = Console()

with console.status("Loading..."):
    time.sleep(3)  # your actual work goes here