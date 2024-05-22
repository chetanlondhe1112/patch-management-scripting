#using wapt
import wapt

def check_available_updates():
    # Create a WindowsUpdate object
    update = wapt.WindowsUpdate()

    # Check for available updates
    updates = update.get_available_updates()

    # Print available updates
    if updates:
        print("Available updates:")
        for update_info in updates:
            print(f"KB{update_info['kb']}: {update_info['title']}")
    else:
        print("No available updates found.")

if __name__ == "__main__":
    check_available_updates()