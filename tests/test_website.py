#!/usr/bin/env python3
"""
Website Testing Suite
Comprehensive tests for HTML validation, CSS validation, JavaScript linting,
accessibility, and performance testing.
"""

import os
import sys
import pytest
import requests
from pathlib import Path
from bs4 import BeautifulSoup
import html5lib
import cssutils
import json
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

class TestWebsiteStructure:
    """Test the basic structure and files of the website."""
    
    def test_required_files_exist(self):
        """Test that all required files exist."""
        required_files = [
            'index.html',
            'css/style.css',
            'js/main.js'
        ]
        
        for file_path in required_files:
            assert Path(file_path).exists(), f"Required file {file_path} does not exist"
    
    def test_html_structure(self):
        """Test HTML structure and required elements."""
        with open('index.html', 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        
        # Test basic HTML structure
        assert soup.find('html'), "HTML tag not found"
        assert soup.find('head'), "HEAD tag not found"
        assert soup.find('body'), "BODY tag not found"
        assert soup.find('title'), "TITLE tag not found"
        
        # Test meta tags
        assert soup.find('meta', {'charset': True}), "Charset meta tag not found"
        assert soup.find('meta', {'name': 'viewport'}), "Viewport meta tag not found"
        
        # Test required sections
        required_sections = ['hero', 'about', 'skills', 'projects', 'contact']
        for section in required_sections:
            assert soup.find(id=section), f"Section #{section} not found"
        
        # Test navigation
        nav = soup.find('nav')
        assert nav, "Navigation not found"
        nav_links = nav.find_all('a')
        assert len(nav_links) >= 4, "Not enough navigation links"
    
    def test_html_validation(self):
        """Test HTML5 validation."""
        with open('index.html', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse with html5lib (strict HTML5 parser)
        try:
            html5lib.parse(content, strict=True)
        except Exception as e:
            pytest.fail(f"HTML5 validation failed: {e}")
    
    def test_css_syntax(self):
        """Test CSS syntax validation."""
        css_file = Path('css/style.css')
        assert css_file.exists(), "CSS file not found"
        
        with open(css_file, 'r', encoding='utf-8') as f:
            css_content = f.read()
        
        # Parse CSS
        cssutils.log.setLevel('ERROR')  # Only show errors
        sheet = cssutils.parseString(css_content)
        
        # Check for CSS errors
        assert len(sheet.cssRules) > 0, "No CSS rules found"
    
    def test_javascript_syntax(self):
        """Test JavaScript syntax by attempting to parse it."""
        js_file = Path('js/main.js')
        assert js_file.exists(), "JavaScript file not found"
        
        # Try to run JSHint if available
        try:
            result = subprocess.run(['node', '-c', str(js_file)], 
                                  capture_output=True, text=True)
            if result.returncode != 0:
                pytest.fail(f"JavaScript syntax error: {result.stderr}")
        except FileNotFoundError:
            # Node.js not available, skip syntax check
            pytest.skip("Node.js not available for JavaScript syntax checking")

class TestWebsiteContent:
    """Test website content and SEO elements."""
    
    def test_meta_tags(self):
        """Test essential meta tags for SEO."""
        with open('index.html', 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        
        # Test title
        title = soup.find('title')
        assert title and title.text.strip(), "Title is empty"
        assert len(title.text) <= 60, "Title too long for SEO"
        
        # Test description (if present)
        description = soup.find('meta', {'name': 'description'})
        if description:
            assert len(description.get('content', '')) <= 160, "Description too long for SEO"
    
    def test_images_have_alt_text(self):
        """Test that all images have alt text for accessibility."""
        with open('index.html', 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        images = soup.find_all('img')
        
        for img in images:
            assert img.get('alt') is not None, f"Image {img.get('src', 'unknown')} missing alt text"
    
    def test_links_are_valid(self):
        """Test that internal links point to valid sections."""
        with open('index.html', 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        internal_links = soup.find_all('a', href=lambda x: x and x.startswith('#'))
        
        for link in internal_links:
            href = link.get('href')[1:]  # Remove #
            target = soup.find(id=href)
            assert target, f"Link target #{href} not found"

class TestResponsiveDesign:
    """Test responsive design and mobile compatibility."""
    
    @pytest.fixture(scope="class")
    def driver(self):
        """Setup Chrome driver for testing."""
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        try:
            driver = webdriver.Chrome(options=chrome_options)
            yield driver
            driver.quit()
        except Exception:
            pytest.skip("Chrome driver not available")
    
    def test_mobile_viewport(self, driver):
        """Test mobile viewport responsiveness."""
        # Start local server for testing
        import threading
        import http.server
        import socketserver
        
        PORT = 8001
        Handler = http.server.SimpleHTTPRequestHandler
        
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            server_thread = threading.Thread(target=httpd.serve_forever)
            server_thread.daemon = True
            server_thread.start()
            
            time.sleep(1)  # Wait for server to start
            
            try:
                # Test desktop view
                driver.set_window_size(1920, 1080)
                driver.get(f"http://localhost:{PORT}")
                
                # Test mobile view
                driver.set_window_size(375, 667)  # iPhone size
                time.sleep(1)
                
                # Check if navigation is responsive
                nav = driver.find_element(By.TAG_NAME, "nav")
                assert nav.is_displayed(), "Navigation not visible on mobile"
                
            finally:
                httpd.shutdown()
    
    def test_navigation_functionality(self, driver):
        """Test navigation functionality."""
        import threading
        import http.server
        import socketserver
        
        PORT = 8002
        Handler = http.server.SimpleHTTPRequestHandler
        
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            server_thread = threading.Thread(target=httpd.serve_forever)
            server_thread.daemon = True
            server_thread.start()
            
            time.sleep(1)
            
            try:
                driver.get(f"http://localhost:{PORT}")
                
                # Test navigation links
                nav_links = driver.find_elements(By.CSS_SELECTOR, "nav a[href^='#']")
                assert len(nav_links) > 0, "No navigation links found"
                
                # Test clicking a navigation link
                if nav_links:
                    nav_links[0].click()
                    time.sleep(1)  # Wait for smooth scroll
                
            finally:
                httpd.shutdown()

class TestPerformance:
    """Test website performance metrics."""
    
    def test_file_sizes(self):
        """Test that files are not too large."""
        size_limits = {
            'index.html': 50 * 1024,  # 50KB
            'css/style.css': 100 * 1024,  # 100KB
            'js/main.js': 100 * 1024,  # 100KB
        }
        
        for file_path, max_size in size_limits.items():
            if Path(file_path).exists():
                file_size = Path(file_path).stat().st_size
                assert file_size <= max_size, f"{file_path} is too large: {file_size} bytes (max: {max_size})"
    
    def test_css_optimization(self):
        """Test CSS for potential optimizations."""
        css_file = Path('css/style.css')
        if css_file.exists():
            with open(css_file, 'r', encoding='utf-8') as f:
                css_content = f.read()
            
            # Check for common optimization opportunities
            assert '/* ' not in css_content or css_content.count('/* ') < 10, "Too many CSS comments (consider minification)"

class TestAccessibility:
    """Test website accessibility features."""
    
    def test_semantic_html(self):
        """Test for semantic HTML elements."""
        with open('index.html', 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        
        # Test for semantic elements
        semantic_elements = ['nav', 'main', 'section', 'article', 'header', 'footer']
        found_semantic = [elem for elem in semantic_elements if soup.find(elem)]
        
        assert len(found_semantic) >= 3, f"Not enough semantic elements found: {found_semantic}"
    
    def test_heading_hierarchy(self):
        """Test proper heading hierarchy."""
        with open('index.html', 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        
        # Should have at least one h1
        h1_count = len([h for h in headings if h.name == 'h1'])
        assert h1_count >= 1, "Should have at least one h1 element"
        assert h1_count <= 1, "Should have only one h1 element per page"
    
    def test_form_labels(self):
        """Test that form inputs have proper labels."""
        with open('index.html', 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        inputs = soup.find_all(['input', 'textarea', 'select'])
        
        for input_elem in inputs:
            input_type = input_elem.get('type', 'text')
            if input_type not in ['hidden', 'submit', 'button']:
                # Check for label, placeholder, or aria-label
                has_label = (
                    input_elem.get('placeholder') or
                    input_elem.get('aria-label') or
                    soup.find('label', {'for': input_elem.get('id')})
                )
                assert has_label, f"Input element missing label: {input_elem}"

if __name__ == '__main__':
    # Run tests
    pytest.main([__file__, '-v'])
