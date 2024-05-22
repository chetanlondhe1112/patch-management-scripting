import subprocess

def get_installed_patches():
    try:
        # Run the wmic command to list installed patches
        result = subprocess.run(['wmic', 'qfe', 'list', 'brief'], capture_output=True, text=True)

        # Check if the command was successful
        if result.returncode == 0:
            # Parse the output to extract patch IDs
            installed_patches = set()
            lines = result.stdout.strip().split('\n')
            for line in lines[1:]:  # Skip the header line
                installed_patches.add(line.split()[0])

            return installed_patches

        else:
            print("Error:", result.stderr)
            return None
        
    except Exception as e:
        print("Error:", e)
        return None

def get_available_patches():
    try:
        # Run the wmic command to list available patches
        result = subprocess.run(['wmic', 'qfe', 'list', 'full'], capture_output=True, text=True)

        # Check if the command was successful
        if result.returncode == 0:
            # Parse the output to extract patch IDs
            available_patches = set()
            lines = result.stdout.strip().split('\n')
            for line in lines:
                if line.startswith('HotFixID='):
                    available_patches.add(line.split('=')[1])

            return available_patches

        else:
            print("Error:", result.stderr)
            return None
        
    except Exception as e:
        print("Error:", e)
        return None

def main():
    installed_patches = get_installed_patches()
    available_patches = get_available_patches()

    if installed_patches is not None and available_patches is not None:
        # Calculate available patches that are not installed
        missing_patches = available_patches - installed_patches

        if missing_patches:
            print("Available Patches Not Installed:")
            for patch in missing_patches:
                print(patch)
        else:
            print("All available patches are installed.")
    else:
        print("Failed to retrieve patch information.")

if __name__ == "__main__":
    main()