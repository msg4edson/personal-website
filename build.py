#!/usr/bin/env python3
"""
Build and Optimization Script
Optimizes HTML, CSS, and JavaScript files for production deployment.
"""

import os
import shutil
from pathlib import Path
import click
import htmlmin
import cssmin
import jsmin
import json
from bs4 import BeautifulSoup

class WebsiteBuilder:
    def __init__(self, source_dir='.', build_dir='dist'):
        self.source_dir = Path(source_dir)
        self.build_dir = Path(build_dir)
        
    def clean_build_dir(self):
        """Clean the build directory."""
        if self.build_dir.exists():
            shutil.rmtree(self.build_dir)
        self.build_dir.mkdir(exist_ok=True)
        click.echo(f"🧹 Cleaned build directory: {self.build_dir}")
    
    def copy_assets(self):
        """Copy static assets to build directory."""
        # Copy images, fonts, and other assets
        asset_patterns = ['*.png', '*.jpg', '*.jpeg', '*.gif', '*.svg', '*.ico', '*.woff', '*.woff2', '*.ttf']
        
        for pattern in asset_patterns:
            for file_path in self.source_dir.glob(pattern):
                dest_path = self.build_dir / file_path.name
                shutil.copy2(file_path, dest_path)
                click.echo(f"📁 Copied: {file_path.name}")
    
    def minify_html(self):
        """Minify HTML files."""
        html_files = list(self.source_dir.glob('*.html'))
        
        for html_file in html_files:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Minify HTML
            minified = htmlmin.minify(
                content,
                remove_comments=True,
                remove_empty_space=True,
                remove_all_empty_space=False,
                reduce_empty_attributes=True,
                reduce_boolean_attributes=True,
                remove_optional_attribute_quotes=False,
                convert_charrefs=True,
                keep_pre=True
            )
            
            # Write to build directory
            dest_path = self.build_dir / html_file.name
            with open(dest_path, 'w', encoding='utf-8') as f:
                f.write(minified)
            
            original_size = len(content)
            minified_size = len(minified)
            savings = ((original_size - minified_size) / original_size) * 100
            
            click.echo(f"🗜️  Minified {html_file.name}: {original_size} → {minified_size} bytes ({savings:.1f}% savings)")
    
    def minify_css(self):
        """Minify CSS files."""
        css_dir = self.source_dir / 'css'
        if not css_dir.exists():
            return
        
        build_css_dir = self.build_dir / 'css'
        build_css_dir.mkdir(exist_ok=True)
        
        for css_file in css_dir.glob('*.css'):
            with open(css_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Minify CSS
            minified = cssmin.cssmin(content)
            
            # Write to build directory
            dest_path = build_css_dir / css_file.name
            with open(dest_path, 'w', encoding='utf-8') as f:
                f.write(minified)
            
            original_size = len(content)
            minified_size = len(minified)
            savings = ((original_size - minified_size) / original_size) * 100
            
            click.echo(f"🎨 Minified {css_file.name}: {original_size} → {minified_size} bytes ({savings:.1f}% savings)")
    
    def minify_js(self):
        """Minify JavaScript files."""
        js_dir = self.source_dir / 'js'
        if not js_dir.exists():
            return
        
        build_js_dir = self.build_dir / 'js'
        build_js_dir.mkdir(exist_ok=True)
        
        for js_file in js_dir.glob('*.js'):
            with open(js_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Minify JavaScript
            try:
                minified = jsmin.jsmin(content)
            except Exception as e:
                click.echo(f"⚠️  Warning: Could not minify {js_file.name}: {e}")
                minified = content
            
            # Write to build directory
            dest_path = build_js_dir / js_file.name
            with open(dest_path, 'w', encoding='utf-8') as f:
                f.write(minified)
            
            original_size = len(content)
            minified_size = len(minified)
            savings = ((original_size - minified_size) / original_size) * 100
            
            click.echo(f"⚡ Minified {js_file.name}: {original_size} → {minified_size} bytes ({savings:.1f}% savings)")
    
    def optimize_images(self):
        """Placeholder for image optimization (requires additional tools)."""
        click.echo("📸 Image optimization skipped (requires additional tools like Pillow)")
    
    def generate_build_info(self):
        """Generate build information file."""
        import datetime
        
        build_info = {
            "build_time": datetime.datetime.now().isoformat(),
            "build_tool": "Python Build Script",
            "version": "1.0.0"
        }
        
        with open(self.build_dir / 'build-info.json', 'w') as f:
            json.dump(build_info, f, indent=2)
        
        click.echo("📋 Generated build info")
    
    def build(self):
        """Run the complete build process."""
        click.echo("🏗️  Starting build process...")
        
        self.clean_build_dir()
        self.copy_assets()
        self.minify_html()
        self.minify_css()
        self.minify_js()
        self.optimize_images()
        self.generate_build_info()
        
        click.echo(f"✅ Build completed! Files available in: {self.build_dir}")

@click.command()
@click.option('--source', '-s', default='.', help='Source directory')
@click.option('--build', '-b', default='dist', help='Build directory')
@click.option('--clean-only', is_flag=True, help='Only clean the build directory')
def main(source, build, clean_only):
    """Build and optimize the website for production."""
    
    builder = WebsiteBuilder(source, build)
    
    if clean_only:
        builder.clean_build_dir()
    else:
        builder.build()

if __name__ == '__main__':
    main()
