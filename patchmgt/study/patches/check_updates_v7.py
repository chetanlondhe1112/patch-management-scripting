# using win
import win32com.client

def install_updates():
    # Create a Windows Update Agent object
    update_agent = win32com.client.Dispatch("Microsoft.Update.Session")

    # Create a Windows Update Searcher object
    update_searcher = update_agent.CreateUpdateSearcher()

    # Search for available updates
    search_result = update_searcher.Search("IsInstalled=0")
    if search_result.Updates.Count > 0:
        print("Available updates:")
        for update in search_result.Updates:
            print(update)
          
    else:
        print("No available updates found.")
    # Install available updates
    if search_result.Updates.Count > 0:
        print("Installing updates...")
        update_installer = update_agent.CreateUpdateInstaller()
        update_installer.Updates = search_result.Updates
        installation_result = update_installer.Install()
        
        # Check installation result
        if installation_result.ResultCode == 2:
            print("Updates installed successfully.")
        else:
            print("Failed to install updates.")
    else:
        print("No updates to install.")

if __name__ == "__main__":
    # Check if running with administrative privileges
    import ctypes
    if ctypes.windll.shell32.IsUserAnAdmin() != 0:
        install_updates()
    else:
        print("Please run this script with administrative privileges.")