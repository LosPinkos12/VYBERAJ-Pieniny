import subprocess
import os

def install_wsl():
    # Enable WSL and install Ubuntu
    subprocess.run(["wsl", "--install"], check=True)

def install_gphoto2():
    # Update package lists and install gphoto2 in Ubuntu
    print("Inštaluje gphoto2.")
    subprocess.run(["wsl", "sudo", "apt", "update"], check=True)
    subprocess.run(["wsl", "sudo", "apt", "install", "-y", "gphoto2"], check=True)

def main():
    # Check if WSL is already installed
    wsl_installed = subprocess.run(["wsl", "--list"], capture_output=True, text=True)
    if "Ubuntu" not in wsl_installed.stdout:
        install_wsl()
    
    # Install gphoto2
    install_gphoto2()

    print("gphoto2 nainštalované úspešne.")

if __name__ == "__main__":
    main()
