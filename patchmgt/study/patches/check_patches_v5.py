#wapt using argument
import sys
import wapt

def check_available_updates(kb_number=None):
    # Create a WindowsUpdate object
    update = wapt.WindowsUpdate()

    # Check for available updates
    if kb_number:
        updates = update.get_available_updates(filter_kb=kb_number)
    else:
        updates = update.get_available_updates()

    # Print available updates
    if updates:
        print("Available updates:")
        for update_info in updates:
            print(f"KB{update_info['kb']}: {update_info['title']}")
    else:
        print("No available updates found.")

if __name__ == "__main__":
    # Check if KB number provided as command-line argument
    if len(sys.argv) > 1:
        kb_number = sys.argv[1]
    else:
        kb_number = None

    check_available_updates(kb_number)