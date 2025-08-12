#!/usr/bin/env python3
"""
Personal Website Project Setup
Handles virtual environment setup, dependency installation, and project initialization.
"""

import os
import sys
import subprocess
import venv
from pathlib import Path
import click
import json

class ProjectSetup:
    def __init__(self, project_dir='.'):
        self.project_dir = Path(project_dir).resolve()
        self.venv_dir = self.project_dir / 'venv'
        self.requirements_file = self.project_dir / 'requirements.txt'
        
    def create_virtual_environment(self):
        """Create a Python virtual environment."""
        if self.venv_dir.exists():
            click.echo(f"🔄 Virtual environment already exists at: {self.venv_dir}")
            return True
        
        click.echo("🐍 Creating Python virtual environment...")
        try:
            venv.create(self.venv_dir, with_pip=True)
            click.echo(f"✅ Virtual environment created at: {self.venv_dir}")
            return True
        except Exception as e:
            click.echo(f"❌ Failed to create virtual environment: {e}", err=True)
            return False
    
    def get_pip_command(self):
        """Get the pip command for the virtual environment."""
        if os.name == 'nt':  # Windows
            return str(self.venv_dir / 'Scripts' / 'pip.exe')
        else:  # Unix-like
            return str(self.venv_dir / 'bin' / 'pip')
    
    def get_python_command(self):
        """Get the Python command for the virtual environment."""
        if os.name == 'nt':  # Windows
            return str(self.venv_dir / 'Scripts' / 'python.exe')
        else:  # Unix-like
            return str(self.venv_dir / 'bin' / 'python')
    
    def install_dependencies(self):
        """Install project dependencies."""
        if not self.requirements_file.exists():
            click.echo(f"❌ Requirements file not found: {self.requirements_file}", err=True)
            return False
        
        pip_cmd = self.get_pip_command()
        click.echo("📦 Installing dependencies...")
        
        try:
            subprocess.run([
                pip_cmd, 'install', '-r', str(self.requirements_file)
            ], check=True, cwd=self.project_dir)
            click.echo("✅ Dependencies installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            click.echo(f"❌ Failed to install dependencies: {e}", err=True)
            return False
    
    def create_directories(self):
        """Create necessary project directories."""
        directories = [
            'tests/reports',
            'dist',
            'logs'
        ]
        
        for dir_path in directories:
            full_path = self.project_dir / dir_path
            full_path.mkdir(parents=True, exist_ok=True)
            click.echo(f"📁 Created directory: {dir_path}")
    
    def create_env_file(self):
        """Create a .env file template."""
        env_file = self.project_dir / '.env'
        if env_file.exists():
            click.echo("🔧 .env file already exists")
            return
        
        env_content = """# AWS Configuration
AWS_REGION=us-east-1
AWS_PROFILE=default

# Development Server
DEV_HOST=localhost
DEV_PORT=8000

# Build Configuration
BUILD_DIR=dist

# Deployment Configuration
BUCKET_NAME=edson-personal-website
DOMAIN_NAME=
ENVIRONMENT=production
"""
        
        with open(env_file, 'w') as f:
            f.write(env_content)
        
        click.echo("✅ Created .env file template")
    
    def create_gitignore(self):
        """Create a .gitignore file."""
        gitignore_file = self.project_dir / '.gitignore'
        if gitignore_file.exists():
            click.echo("📝 .gitignore file already exists")
            return
        
        gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtual Environment
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Logs
logs/
*.log

# Environment variables
.env
.env.local

# Test reports
tests/reports/
.coverage
htmlcov/
.pytest_cache/

# Build output
dist/
build/

# Terraform
terraform/.terraform/
terraform/terraform.tfstate*
terraform/.terraform.lock.hcl
terraform/terraform.tfvars

# AWS
.aws/

# Deployment
deploy_config.json
"""
        
        with open(gitignore_file, 'w') as f:
            f.write(gitignore_content)
        
        click.echo("✅ Created .gitignore file")
    
    def create_activation_script(self):
        """Create an activation script for easy development."""
        if os.name == 'nt':  # Windows
            script_name = 'activate.bat'
            script_content = f"""@echo off
echo Activating Personal Website Development Environment...
call "{self.venv_dir}\\Scripts\\activate.bat"
echo.
echo Available commands:
echo   python dev_server.py     - Start development server
echo   python deploy.py --help  - Deploy to AWS
echo   python build.py          - Build for production
echo   pytest                   - Run tests
echo.
"""
        else:  # Unix-like
            script_name = 'activate.sh'
            script_content = f"""#!/bin/bash
echo "Activating Personal Website Development Environment..."
source "{self.venv_dir}/bin/activate"
echo
echo "Available commands:"
echo "  python dev_server.py     - Start development server"
echo "  python deploy.py --help  - Deploy to AWS"
echo "  python build.py          - Build for production"
echo "  pytest                   - Run tests"
echo
"""
        
        script_path = self.project_dir / script_name
        with open(script_path, 'w') as f:
            f.write(script_content)
        
        if os.name != 'nt':
            os.chmod(script_path, 0o755)
        
        click.echo(f"✅ Created activation script: {script_name}")
    
    def setup_project(self):
        """Run the complete project setup."""
        click.echo("🚀 Setting up Personal Website project...")
        click.echo("=" * 50)
        
        success = True
        
        # Create virtual environment
        if not self.create_virtual_environment():
            success = False
        
        # Install dependencies
        if success and not self.install_dependencies():
            success = False
        
        # Create directories
        self.create_directories()
        
        # Create configuration files
        self.create_env_file()
        self.create_gitignore()
        self.create_activation_script()
        
        if success:
            click.echo("\n" + "=" * 50)
            click.echo("✅ Project setup completed successfully!")
            click.echo("\n🎯 Next steps:")
            click.echo("1. Activate the virtual environment:")
            if os.name == 'nt':
                click.echo("   activate.bat")
            else:
                click.echo("   source activate.sh")
            click.echo("2. Start development server:")
            click.echo("   python dev_server.py")
            click.echo("3. Run tests:")
            click.echo("   pytest")
            click.echo("4. Deploy to AWS:")
            click.echo("   python deploy.py --action apply")
        else:
            click.echo("\n❌ Project setup failed!")
            return False
        
        return True

@click.command()
@click.option('--project-dir', '-d', default='.', help='Project directory')
@click.option('--force', is_flag=True, help='Force recreation of virtual environment')
def main(project_dir, force):
    """Setup the Personal Website project."""
    
    setup = ProjectSetup(project_dir)
    
    if force and setup.venv_dir.exists():
        import shutil
        click.echo("🗑️  Removing existing virtual environment...")
        shutil.rmtree(setup.venv_dir)
    
    setup.setup_project()

if __name__ == '__main__':
    main()
