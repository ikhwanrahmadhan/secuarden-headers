"""
Command-line interface for Secuarden Headers.
"""

import sys
import json
import csv
from pathlib import Path
from typing import List, Optional
import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import box

from .scanner import SecurityHeaderScanner, ScanResult
from .headers import get_recommended_headers


console = Console()


def print_banner():
    """Print Secuarden banner."""
    banner = """
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║   ███████╗███████╗ ██████╗██╗   ██╗ █████╗ ██████╗       ║
║   ██╔════╝██╔════╝██╔════╝██║   ██║██╔══██╗██╔══██╗      ║
║   ███████╗█████╗  ██║     ██║   ██║███████║██████╔╝      ║
║   ╚════██║██╔══╝  ██║     ██║   ██║██╔══██║██╔══██╗      ║
║   ███████║███████╗╚██████╗╚██████╔╝██║  ██║██║  ██║      ║
║   ╚══════╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝      ║
║                                                           ║
║            HTTP Security Headers Scanner v2.0             ║
║                  by Secuarden.com                         ║
╚═══════════════════════════════════════════════════════════╝
    """
    console.print(banner, style="bold cyan")


def get_score_color(score: float) -> str:
    """Get color based on security score."""
    if score >= 80:
        return "green"
    elif score >= 60:
        return "yellow"
    elif score >= 40:
        return "orange1"
    else:
        return "red"


def print_result(result: ScanResult, verbose: bool = False):
    """Print scan result in a formatted way."""
    if not result.is_success:
        console.print(f"\n[red]✗[/red] {result.url}")
        console.print(f"  [red]Error: {result.error}[/red]")
        return
    
    score = result.security_score
    score_color = get_score_color(score)
    
    console.print(f"\n[cyan]Target:[/cyan] {result.url}")
    console.print(f"[cyan]Status:[/cyan] {result.status_code}")
    console.print(f"[cyan]Security Score:[/cyan] [{score_color}]{score}/100[/{score_color}]")
    
    # Present headers
    if result.present_headers:
        table = Table(title="✓ Present Security Headers", box=box.ROUNDED, show_header=True)
        table.add_column("Header", style="green")
        table.add_column("Value", style="dim")
        
        for header, value in sorted(result.present_headers.items()):
            display_value = value if verbose else (value[:60] + "..." if len(value) > 60 else value)
            table.add_row(header, display_value)
        
        console.print(table)
    
    # Missing headers
    if result.missing_headers:
        table = Table(title="✗ Missing Recommended Headers", box=box.ROUNDED, show_header=True)
        table.add_column("Header", style="red")
        table.add_column("Description", style="dim")
        
        headers_info = get_recommended_headers()
        for header in sorted(result.missing_headers):
            info = headers_info.get(header)
            desc = info.description if info else "N/A"
            table.add_row(header, desc)
        
        console.print(table)
    
    # Deprecated headers
    if result.deprecated_headers:
        table = Table(title="⚠ Deprecated Headers Found", box=box.ROUNDED, show_header=True)
        table.add_column("Header", style="yellow")
        table.add_column("Value", style="dim")
        
        for header, value in sorted(result.deprecated_headers.items()):
            display_value = value if verbose else (value[:60] + "..." if len(value) > 60 else value)
            table.add_row(header, display_value)
        
        console.print(table)
    
    # Insecure values
    if result.insecure_values:
        table = Table(title="⚠ Insecure Header Values", box=box.ROUNDED, show_header=True)
        table.add_column("Header", style="orange1")
        table.add_column("Insecure Values", style="dim")
        
        for header, values in sorted(result.insecure_values.items()):
            table.add_row(header, ", ".join(values))
        
        console.print(table)


def export_json(results: List[ScanResult], output_file: Path):
    """Export results to JSON."""
    data = []
    for result in results:
        data.append({
            "url": result.url,
            "status_code": result.status_code,
            "security_score": result.security_score,
            "present_headers": result.present_headers,
            "missing_headers": list(result.missing_headers),
            "deprecated_headers": result.deprecated_headers,
            "insecure_values": result.insecure_values,
            "error": result.error,
            "scan_time": result.scan_time.isoformat() if result.scan_time else None
        })
    
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=2)
    
    console.print(f"\n[green]✓[/green] Results exported to {output_file}")


def export_csv(results: List[ScanResult], output_file: Path):
    """Export results to CSV."""
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            "URL", "Status Code", "Security Score",
            "Present Headers", "Missing Headers",
            "Deprecated Headers", "Insecure Values", "Error"
        ])
        
        for result in results:
            writer.writerow([
                result.url,
                result.status_code or "",
                result.security_score,
                "; ".join(result.present_headers.keys()),
                "; ".join(result.missing_headers),
                "; ".join(result.deprecated_headers.keys()),
                "; ".join(f"{k}={v}" for k, v in result.insecure_values.items()),
                result.error or ""
            ])
    
    console.print(f"\n[green]✓[/green] Results exported to {output_file}")


@click.command()
@click.argument('urls', nargs=-1)
@click.option('-f', '--file', type=click.Path(exists=True), help='File containing URLs (one per line)')
@click.option('-o', '--output', type=click.Path(), help='Output file (JSON or CSV)')
@click.option('-t', '--timeout', default=10, help='Request timeout in seconds')
@click.option('-c', '--concurrent', default=10, help='Maximum concurrent requests')
@click.option('--no-verify-ssl', is_flag=True, help='Disable SSL verification')
@click.option('--no-follow-redirects', is_flag=True, help='Do not follow redirects')
@click.option('-v', '--verbose', is_flag=True, help='Verbose output')
@click.option('--no-banner', is_flag=True, help='Hide banner')
def main(
    urls: tuple,
    file: Optional[str],
    output: Optional[str],
    timeout: int,
    concurrent: int,
    no_verify_ssl: bool,
    no_follow_redirects: bool,
    verbose: bool,
    no_banner: bool
):
    """
    Secuarden Headers - HTTP Security Headers Scanner
    
    Scan one or more URLs for security headers.
    
    Examples:
    
        secuarden-headers https://example.com
        
        secuarden-headers https://example.com https://google.com
        
        secuarden-headers -f urls.txt -o results.json
    """
    if not no_banner:
        print_banner()
    
    # Collect URLs
    url_list = list(urls)
    
    if file:
        with open(file, 'r') as f:
            file_urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]
            url_list.extend(file_urls)
    
    if not url_list:
        console.print("[red]Error:[/red] No URLs provided. Use URLs as arguments or --file option.")
        sys.exit(1)
    
    # Initialize scanner
    scanner = SecurityHeaderScanner(
        timeout=timeout,
        follow_redirects=not no_follow_redirects,
        verify_ssl=not no_verify_ssl
    )
    
    # Scan URLs
    if len(url_list) == 1:
        console.print(f"\n[cyan]Scanning {url_list[0]}...[/cyan]")
        result = scanner.scan_url(url_list[0])
        results = [result]
        print_result(result, verbose)
    else:
        console.print(f"\n[cyan]Scanning {len(url_list)} URLs...[/cyan]\n")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Scanning...", total=None)
            results = scanner.scan_urls(url_list, max_concurrent=concurrent)
            progress.update(task, completed=True)
        
        # Print results
        for result in results:
            print_result(result, verbose)
        
        # Print summary
        successful = sum(1 for r in results if r.is_success)
        failed = len(results) - successful
        avg_score = sum(r.security_score for r in results if r.is_success) / max(successful, 1)
        
        summary = Table(title="Scan Summary", box=box.ROUNDED)
        summary.add_column("Metric", style="cyan")
        summary.add_column("Value", style="bold")
        summary.add_row("Total URLs", str(len(results)))
        summary.add_row("Successful", f"[green]{successful}[/green]")
        summary.add_row("Failed", f"[red]{failed}[/red]")
        summary.add_row("Average Score", f"[{get_score_color(avg_score)}]{avg_score:.2f}/100[/{get_score_color(avg_score)}]")
        
        console.print("\n")
        console.print(summary)
    
    # Export results
    if output:
        output_path = Path(output)
        if output_path.suffix.lower() == '.json':
            export_json(results, output_path)
        elif output_path.suffix.lower() == '.csv':
            export_csv(results, output_path)
        else:
            console.print("[yellow]Warning:[/yellow] Unknown output format. Using JSON.")
            export_json(results, output_path.with_suffix('.json'))


if __name__ == '__main__':
    main()
