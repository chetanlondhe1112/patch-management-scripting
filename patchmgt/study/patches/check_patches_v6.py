#using win32com
import win32com.client

def check_available_updates():
    # Create a Windows Update Agent object
    update_agent = win32com.client.Dispatch("Microsoft.Update.Session")

    # Create a Windows Update Searcher object
    update_searcher = update_agent.CreateUpdateSearcher()

    # Search for available updates
    search_result = update_searcher.Search("IsInstalled=0")
    print(search_result)
    # Print available updates
    if search_result.Updates.Count > 0:
        print("Available updates:")
        for update in search_result.Updates:
            print(update)
            #print(f"{update.Title}: {update.KBArticleIDs[0]}")
    else:
        print("No available updates found.")

if __name__ == "__main__":
    check_available_updates()