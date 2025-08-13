#!/usr/bin/env python3
"""
Local Development Server with Hot Reload
A Flask-based development server for the personal website with live reload capabilities.
"""

import os
import time
from pathlib import Path
from flask import Flask, send_from_directory, send_file
from flask_cors import CORS
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import webbrowser
import click
import threading
from livereload import Server

class WebsiteHandler(FileSystemEventHandler):
    """File system event handler for website files."""
    
    def __init__(self, reload_callback=None):
        self.reload_callback = reload_callback
        self.last_reload = 0
        
    def on_modified(self, event):
        if event.is_directory:
            return
            
        # Only reload for relevant file types
        relevant_extensions = {'.html', '.css', '.js', '.json'}
        file_path = Path(event.src_path)
        
        if file_path.suffix.lower() in relevant_extensions:
            # Debounce rapid file changes
            current_time = time.time()
            if current_time - self.last_reload > 0.5:  # 500ms debounce
                self.last_reload = current_time
                if self.reload_callback:
                    self.reload_callback()
                print(f"🔄 Reloaded due to change in: {file_path.name}")

class DevServer:
    def __init__(self, host='localhost', port=8000, watch_dirs=None):
        self.host = host
        self.port = port
        self.watch_dirs = watch_dirs or ['.']
        self.app = Flask(__name__)
        CORS(self.app)
        self.setup_routes()
        
    def setup_routes(self):
        """Setup Flask routes for serving static files."""
        
        @self.app.route('/')
        def index():
            return send_file('index.html')
        
        @self.app.route('/<path:filename>')
        def serve_static(filename):
            # Handle different file types
            if filename.endswith('.html'):
                return send_file(filename)
            elif filename.startswith('css/'):
                return send_from_directory('.', filename, mimetype='text/css')
            elif filename.startswith('js/'):
                return send_from_directory('.', filename, mimetype='application/javascript')
            else:
                return send_from_directory('.', filename)
        
        @self.app.errorhandler(404)
        def not_found(error):
            # For SPA routing, return index.html for unknown routes
            return send_file('index.html')
    
    def run_with_livereload(self):
        """Run the development server with live reload using Flask's built-in reloader."""
        print(f"Development server starting...")
        print(f"Local: http://{self.host}:{self.port}")
        print(f"Live reload enabled")
        print(f"Watching: {', '.join(self.watch_dirs)}")
        print(f"Press Ctrl+C to stop")
        
        # Open browser automatically
        threading.Timer(1.0, lambda: webbrowser.open(f'http://{self.host}:{self.port}')).start()
        
        try:
            # Use Flask's built-in development server with reloader
            self.app.run(
                host=self.host, 
                port=self.port, 
                debug=True, 
                use_reloader=True,
                use_debugger=True
            )
        except KeyboardInterrupt:
            print("\nDevelopment server stopped")
    
    def run_simple(self):
        """Run a simple Flask development server."""
        print(f"🚀 Development server starting...")
        print(f"📍 Local: http://{self.host}:{self.port}")
        print(f"⏹️  Press Ctrl+C to stop")
        
        # Open browser automatically
        threading.Timer(1.0, lambda: webbrowser.open(f'http://{self.host}:{self.port}')).start()
        
        try:
            self.app.run(host=self.host, port=self.port, debug=True)
        except KeyboardInterrupt:
            print("\n👋 Development server stopped")

@click.command()
@click.option('--host', '-h', default='localhost', help='Host to bind to')
@click.option('--port', '-p', default=8000, help='Port to bind to')
@click.option('--no-reload', is_flag=True, help='Disable live reload')
@click.option('--no-browser', is_flag=True, help='Don\'t open browser automatically')
def main(host, port, no_reload, no_browser):
    """Start the development server for the personal website."""
    
    # Check if index.html exists
    if not os.path.exists('index.html'):
        click.echo("❌ index.html not found. Make sure you're in the project root directory.", err=True)
        return
    
    server = DevServer(host=host, port=port)
    
    if no_reload:
        server.run_simple()
    else:
        server.run_with_livereload()

if __name__ == '__main__':
    main()
