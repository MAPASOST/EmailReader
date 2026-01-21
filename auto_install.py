"""
Auto-installer for Email Reader dependencies.
Checks and installs required packages automatically.
"""
import subprocess
import sys


def install_package(package):
    """Install a package using pip."""
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])


def check_and_install_dependencies():
    """Check for required packages and install if missing."""
    required_packages = {
        'anthropic': 'anthropic==0.42.0',
        'dotenv': 'python-dotenv==1.0.0',
        'schedule': 'schedule==1.2.0',
        'msgraph': 'msgraph-sdk==1.5.4',
        'azure.identity': 'azure-identity==1.15.0'
    }

    missing_packages = []

    # Check which packages are missing
    for package_name, package_spec in required_packages.items():
        try:
            __import__(package_name)
        except ImportError:
            missing_packages.append(package_spec)

    # Install missing packages
    if missing_packages:
        print("Installing required dependencies...")
        print("This may take a minute...\n")

        for package in missing_packages:
            try:
                print(f"Installing {package}...")
                install_package(package)
                print(f"✓ {package} installed successfully")
            except Exception as e:
                print(f"✗ Failed to install {package}: {e}")
                return False

        print("\n✓ All dependencies installed successfully!")
        return True
    else:
        return True


if __name__ == "__main__":
    success = check_and_install_dependencies()
    if success:
        print("All dependencies are ready!")
    else:
        print("Some dependencies failed to install.")
        sys.exit(1)
