import wusa
import subprocess

def list_available_patches():
    # Function to list all available patches
    try:
        result = subprocess.run(["wmic", "qfe", "list", "brief"], capture_output=True, text=True)
        lines = result.stdout.splitlines()
        available_patches = [line.split()[1] for line in lines[2:] if line.strip()]
        return available_patches
    except Exception as e:
        print("Error:", e)
        return []

def list_installed_patches():
    # Function to list all installed patches
    try:
        result = subprocess.run(["wmic", "qfe", "list", "brief"], capture_output=True, text=True)
        lines = result.stdout.splitlines()
        installed_patches = [line.split()[1] for line in lines[2:] if line.strip()]
        return installed_patches
    except Exception as e:
        print("Error:", e)
        return []

def download_patch(kb_number):
    # Function to download a patch using wusa library
    try:
        downloader = wusa.Downloader()
        downloader.download(kb_number)
        print(f"Patch {kb_number} downloaded successfully.")
    except Exception as e:
        print(f"Error downloading patch {kb_number}: {e}")

def install_patch(kb_number):
    # Function to install a patch using wusa.exe command
    try:
        cmd = f"wusa.exe /quiet /norestart /update {kb_number}"
        subprocess.run(cmd, shell=True, check=True)
        print(f"Patch {kb_number} installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error installing patch {kb_number}: {e}")
    except Exception as e:
        print(f"Error installing patch {kb_number}: {e}")

def main():
    try:
        # List available and installed patches
        available_patches = list_available_patches()
        installed_patches = list_installed_patches()

        # Find missing patches
        missing_patches = [patch for patch in available_patches if patch not in installed_patches]

        # Download and install missing patches
        if missing_patches:
            print("Downloading and installing missing patches:")
            for patch in missing_patches:
                print(f"Downloading patch {patch}...")
                download_patch(patch)
                print(f"Installing patch {patch}...")
                install_patch(patch)
        else:
            print("No missing patches found.")
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()