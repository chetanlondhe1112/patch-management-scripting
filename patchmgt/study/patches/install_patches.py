import subprocess
import sys

def install_patch(patch_id):
    try:
        # Run the wusa command to install the patch
        result = subprocess.run(['wusa', '/quiet', '/norestart', '/kb:{}'.format(patch_id)], capture_output=True, text=True)

        # Check if the command was successful
        if result.returncode == 0:
            print(f"Patch {patch_id} installed successfully.")
        else:
            print(f"Error installing patch {patch_id}:", result.stderr)
        
    except Exception as e:
        print(f"Error installing patch {patch_id}:", e)

def main():
    if len(sys.argv) != 2:
        print("Usage: python install_patch.py <patch_id>")
        sys.exit(1)

    patch_id = sys.argv[1]
    install_patch(patch_id)

if __name__ == "__main__":
    main()