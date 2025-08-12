#!/usr/bin/env python3
"""
Personal Website Project Manager
A unified command-line interface for all project operations.
"""

import click
import subprocess
import sys
from pathlib import Path
import os

@click.group()
@click.version_option(version='1.0.0')
def cli():
    """Personal Website Project Manager - All-in-one tool for development, testing, and deployment."""
    pass

@cli.command()
@click.option('--force', is_flag=True, help='Force recreation of virtual environment')
def setup(force):
    """Setup the project environment and dependencies."""
    click.echo("🚀 Setting up project...")
    cmd = [sys.executable, 'setup.py']
    if force:
        cmd.append('--force')
    subprocess.run(cmd)

@cli.command()
@click.option('--host', '-h', default='localhost', help='Host to bind to')
@click.option('--port', '-p', default=8000, help='Port to bind to')
@click.option('--no-reload', is_flag=True, help='Disable live reload')
@click.option('--no-browser', is_flag=True, help='Don\'t open browser automatically')
def dev(host, port, no_reload, no_browser):
    """Start the development server with live reload."""
    click.echo("🖥️  Starting development server...")
    cmd = [sys.executable, 'dev_server.py', '--host', host, '--port', str(port)]
    if no_reload:
        cmd.append('--no-reload')
    if no_browser:
        cmd.append('--no-browser')
    subprocess.run(cmd)

@cli.command()
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
@click.option('--coverage', '-c', is_flag=True, help='Run with coverage report')
@click.option('--html', is_flag=True, help='Generate HTML report')
def test(verbose, coverage, html):
    """Run the test suite."""
    click.echo("🧪 Running tests...")
    cmd = ['pytest']
    if verbose:
        cmd.append('-v')
    if coverage:
        cmd.extend(['--cov=.', '--cov-report=term-missing'])
    if html:
        cmd.extend(['--html=tests/reports/report.html', '--self-contained-html'])
    subprocess.run(cmd)

@cli.command()
@click.option('--source', '-s', default='.', help='Source directory')
@click.option('--build', '-b', default='dist', help='Build directory')
def build(source, build):
    """Build and optimize the website for production."""
    click.echo("🏗️  Building website...")
    subprocess.run([sys.executable, 'build.py', '--source', source, '--build', build])

@cli.command()
@click.option('--action', '-a', 
              type=click.Choice(['plan', 'apply', 'destroy', 'deploy-files', 'invalidate']),
              default='plan',
              help='Deployment action')
@click.option('--bucket-name', '-b', help='S3 bucket name')
@click.option('--domain-name', '-d', help='Domain name')
@click.option('--region', '-r', help='AWS region')
def deploy(action, bucket_name, domain_name, region):
    """Deploy to AWS infrastructure."""
    click.echo(f"☁️  Running deployment action: {action}")
    cmd = [sys.executable, 'deploy.py', '--action', action]
    if bucket_name:
        cmd.extend(['--bucket-name', bucket_name])
    if domain_name:
        cmd.extend(['--domain-name', domain_name])
    if region:
        cmd.extend(['--region', region])
    subprocess.run(cmd)

@cli.command()
def clean():
    """Clean build artifacts and temporary files."""
    click.echo("🧹 Cleaning project...")
    
    # Directories to clean
    clean_dirs = ['dist', 'build', '__pycache__', '.pytest_cache', 'tests/reports']
    
    for dir_name in clean_dirs:
        dir_path = Path(dir_name)
        if dir_path.exists():
            import shutil
            shutil.rmtree(dir_path)
            click.echo(f"🗑️  Removed: {dir_name}")
    
    # Files to clean
    clean_patterns = ['*.pyc', '*.pyo', '*.log']
    for pattern in clean_patterns:
        for file_path in Path('.').rglob(pattern):
            file_path.unlink()
            click.echo(f"🗑️  Removed: {file_path}")
    
    click.echo("✅ Cleanup completed")

@cli.command()
def status():
    """Show project status and information."""
    click.echo("📊 Project Status")
    click.echo("=" * 30)
    
    # Check virtual environment
    venv_path = Path('venv')
    if venv_path.exists():
        click.echo("✅ Virtual environment: Ready")
    else:
        click.echo("❌ Virtual environment: Not found")
    
    # Check key files
    key_files = [
        'index.html',
        'css/style.css',
        'js/main.js',
        'terraform/main.tf',
        'requirements.txt'
    ]
    
    click.echo("\n📁 Key Files:")
    for file_path in key_files:
        if Path(file_path).exists():
            click.echo(f"✅ {file_path}")
        else:
            click.echo(f"❌ {file_path}")
    
    # Check dependencies
    try:
        import boto3, flask, pytest
        click.echo("\n📦 Dependencies: Ready")
    except ImportError:
        click.echo("\n❌ Dependencies: Missing (run: python manage.py setup)")
    
    # Check AWS credentials
    try:
        import boto3
        boto3.client('sts').get_caller_identity()
        click.echo("☁️  AWS Credentials: Configured")
    except:
        click.echo("❌ AWS Credentials: Not configured")

@cli.command()
def info():
    """Show project information and available commands."""
    click.echo("""
🌐 Personal Website Project Manager
==================================

This is a modern personal website built with:
• HTML5, CSS3, JavaScript (Frontend)
• Python (Development & Deployment Tools)
• AWS S3 + CloudFront (Hosting)
• Terraform (Infrastructure as Code)

📋 Available Commands:
• setup    - Initialize project environment
• dev      - Start development server
• test     - Run test suite
• build    - Build for production
• deploy   - Deploy to AWS
• clean    - Clean build artifacts
• status   - Show project status
• info     - Show this information

🚀 Quick Start:
1. python manage.py setup
2. python manage.py dev
3. python manage.py test
4. python manage.py deploy --action apply

📚 For detailed help on any command:
python manage.py COMMAND --help
""")

if __name__ == '__main__':
    cli()
