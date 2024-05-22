import sys
import win32com.client

def install_update(kb_number):
    # Create a Windows Update Agent object
    update_agent = win32com.client.Dispatch("Microsoft.Update.Session")

    # Create a Windows Update Searcher object
    update_searcher = update_agent.CreateUpdateSearcher()

    # Search for the update with the specified KB number
    search_result = update_searcher.Search(f"IsInstalled=0 and Type='Software' and KBID='{kb_number}'")

    # Check if the update was found
    if search_result.Updates.Count == 0:
        print(f"No update with KB number {kb_number} found.")
        return

    # Install the update
    print(f"Installing update with KB number {kb_number}...")
    update_installer = update_agent.CreateUpdateInstaller()
    update_installer.Updates = search_result.Updates
    installation_result = update_installer.Install()
    
    # Check installation result
    if installation_result.ResultCode == 2:
        print("Update installed successfully.")
    else:
        print("Failed to install update.")

if __name__ == "__main__":
    # Check if a KB number is provided as a command-line argument
    if len(sys.argv) != 2:
        print("Usage: python script.py <KB number>")
        sys.exit(1)

    kb_number = sys.argv[1]
    install_update(kb_number)