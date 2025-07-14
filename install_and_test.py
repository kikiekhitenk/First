#!/usr/bin/env python3
"""
Installation and Testing Script untuk Location Tracker
Script ini akan menginstal dependencies dan menjalankan test sistem
"""

import os
import sys
import subprocess
import platform
import importlib
import time

def print_header(title):
    """Print header dengan formatting"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def print_status(message, status="INFO"):
    """Print status message"""
    icons = {
        "INFO": "ℹ️",
        "SUCCESS": "✅", 
        "ERROR": "❌",
        "WARNING": "⚠️",
        "RUNNING": "🔄"
    }
    print(f"{icons.get(status, 'ℹ️')} {message}")

def check_python_version():
    """Check Python version"""
    print_status("Checking Python version...", "RUNNING")
    
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print_status(f"Python {version.major}.{version.minor}.{version.micro} detected", "ERROR")
        print_status("Python 3.8 or higher required!", "ERROR")
        return False
    else:
        print_status(f"Python {version.major}.{version.minor}.{version.micro} - OK", "SUCCESS")
        return True

def check_system_dependencies():
    """Check system dependencies"""
    print_status("Checking system dependencies...", "RUNNING")
    
    system = platform.system()
    print_status(f"Operating System: {system}", "INFO")
    
    if system == "Linux":
        print_status("Linux detected - checking for build tools...", "INFO")
        
        # Check for common build tools
        tools = ["gcc", "g++", "make", "cmake"]
        missing_tools = []
        
        for tool in tools:
            result = subprocess.run(["which", tool], capture_output=True, text=True)
            if result.returncode != 0:
                missing_tools.append(tool)
        
        if missing_tools:
            print_status(f"Missing build tools: {', '.join(missing_tools)}", "WARNING")
            print_status("Install with: sudo apt-get install build-essential cmake", "INFO")
            return False
        else:
            print_status("Build tools available", "SUCCESS")
    
    return True

def install_requirements():
    """Install Python requirements"""
    print_status("Installing Python requirements...", "RUNNING")
    
    try:
        # Upgrade pip first
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], 
                      check=True, capture_output=True)
        
        # Install requirements
        result = subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                               check=True, capture_output=True, text=True)
        
        print_status("Requirements installed successfully", "SUCCESS")
        return True
        
    except subprocess.CalledProcessError as e:
        print_status(f"Failed to install requirements: {e}", "ERROR")
        print("Error output:", e.stderr)
        return False

def check_imports():
    """Check if all required modules can be imported"""
    print_status("Testing module imports...", "RUNNING")
    
    required_modules = [
        "cv2",
        "numpy", 
        "tensorflow",
        "face_recognition",
        "sklearn",
        "PIL",
        "matplotlib",
        "requests",
        "geopy",
        "folium",
        "exifread",
        "flask"
    ]
    
    failed_imports = []
    
    for module in required_modules:
        try:
            importlib.import_module(module)
            print_status(f"✓ {module}", "INFO")
        except ImportError:
            failed_imports.append(module)
            print_status(f"✗ {module}", "ERROR")
    
    if failed_imports:
        print_status(f"Failed imports: {', '.join(failed_imports)}", "ERROR")
        return False
    else:
        print_status("All modules imported successfully", "SUCCESS")
        return True

def test_location_tracker():
    """Test LocationTracker functionality"""
    print_status("Testing LocationTracker class...", "RUNNING")
    
    try:
        # Import and initialize
        from location_tracker import LocationTracker
        tracker = LocationTracker()
        
        print_status("LocationTracker initialized successfully", "SUCCESS")
        
        # Test basic functionality
        print_status("Testing basic functionality...", "INFO")
        
        # Check if database was created
        if os.path.exists("location_database.json"):
            print_status("Database file created", "SUCCESS")
        else:
            print_status("Database file not found", "WARNING")
        
        # Test model creation
        if hasattr(tracker, 'model') and tracker.model is not None:
            print_status("Deep learning model loaded", "SUCCESS")
        else:
            print_status("Deep learning model not loaded", "WARNING")
        
        return True
        
    except Exception as e:
        print_status(f"LocationTracker test failed: {e}", "ERROR")
        return False

def run_demo():
    """Run demo script"""
    print_status("Running demo script...", "RUNNING")
    
    try:
        result = subprocess.run([sys.executable, "demo_script.py"], 
                               check=True, capture_output=True, text=True)
        print_status("Demo completed successfully", "SUCCESS")
        return True
        
    except subprocess.CalledProcessError as e:
        print_status(f"Demo failed: {e}", "ERROR")
        print("Error output:", e.stderr)
        return False

def test_web_interface():
    """Test web interface (basic import test)"""
    print_status("Testing web interface...", "RUNNING")
    
    try:
        # Import web app
        import web_app
        print_status("Web interface imports successful", "SUCCESS")
        
        # Test template creation
        web_app.create_templates()
        
        if os.path.exists("templates"):
            print_status("Templates created successfully", "SUCCESS")
        else:
            print_status("Templates not created", "WARNING")
        
        return True
        
    except Exception as e:
        print_status(f"Web interface test failed: {e}", "ERROR")
        return False

def cleanup_test_files():
    """Clean up test files"""
    print_status("Cleaning up test files...", "RUNNING")
    
    test_files = [
        "demo_images",
        "demo_map_1.html",
        "demo_map_2.html", 
        "demo_map_3.html",
        "demo_report.json",
        "uploads",
        "static",
        "templates"
    ]
    
    for item in test_files:
        if os.path.exists(item):
            if os.path.isdir(item):
                import shutil
                shutil.rmtree(item)
            else:
                os.remove(item)
    
    print_status("Test files cleaned up", "SUCCESS")

def show_usage_examples():
    """Show usage examples"""
    print_header("USAGE EXAMPLES")
    
    examples = [
        {
            "title": "1. Command Line - Identify Location",
            "command": "python main.py --mode identify --image your_image.jpg"
        },
        {
            "title": "2. Command Line - Add Person",
            "command": "python main.py --mode add_person --image face.jpg --name 'John' --location 'Office' --coordinates '-6.2088,106.8456'"
        },
        {
            "title": "3. Web Interface",
            "command": "python web_app.py"
        },
        {
            "title": "4. Run Demo",
            "command": "python demo_script.py"
        }
    ]
    
    for example in examples:
        print(f"\n{example['title']}:")
        print(f"  {example['command']}")

def main():
    """Main installation and testing function"""
    print_header("LOCATION TRACKER - INSTALLATION & TESTING")
    
    print("This script will:")
    print("• Check system requirements")
    print("• Install Python dependencies") 
    print("• Test core functionality")
    print("• Run demonstration")
    print("• Show usage examples")
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Check system dependencies
    if not check_system_dependencies():
        print_status("System dependencies check failed", "WARNING")
        print_status("Some features may not work properly", "WARNING")
    
    # Install requirements
    if not install_requirements():
        print_status("Installation failed", "ERROR")
        sys.exit(1)
    
    # Check imports
    if not check_imports():
        print_status("Module import test failed", "ERROR")
        sys.exit(1)
    
    # Test LocationTracker
    if not test_location_tracker():
        print_status("LocationTracker test failed", "ERROR")
        sys.exit(1)
    
    # Test web interface
    if not test_web_interface():
        print_status("Web interface test failed", "WARNING")
    
    # Run demo
    print_status("Would you like to run the demo? (y/n): ", "INFO")
    try:
        response = input().lower().strip()
        if response in ['y', 'yes']:
            if run_demo():
                print_status("Demo completed successfully!", "SUCCESS")
            else:
                print_status("Demo failed", "ERROR")
        
        # Clean up
        print_status("Would you like to clean up test files? (y/n): ", "INFO")
        response = input().lower().strip()
        if response in ['y', 'yes']:
            cleanup_test_files()
    
    except KeyboardInterrupt:
        print_status("\nInstallation interrupted by user", "WARNING")
    
    # Show usage examples
    show_usage_examples()
    
    print_header("INSTALLATION COMPLETE")
    print_status("Location Tracker is ready to use!", "SUCCESS")
    print_status("Read README.md for detailed documentation", "INFO")
    print_status("Run 'python web_app.py' to start web interface", "INFO")

if __name__ == "__main__":
    main()