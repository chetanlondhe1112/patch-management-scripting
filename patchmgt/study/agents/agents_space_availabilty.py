import win32com.client

def get_available_patches():
    try:
        # Create a Windows Update Agent object
        update_session = win32com.client.Dispatch("Microsoft.Update.Session")
        
        # Create a Windows Update Searcher object
        update_searcher = update_session.CreateUpdateSearcher()
        
        # Search for updates
        search_result = update_searcher.Search("IsInstalled=0")
        
        # List available updates along with their sizes
        count=0
        total_patch_size=0
        print("All Available Patches:")
        for update in search_result.Updates:
            count+=1
            print(f"\t{count})")
            print(f"\tUpdate Title: {update.Title}")
            print(f"\tUpdate ID: {update.Identity.UpdateID}")
            print(f"\tUpdate Size: {int(update.MaxDownloadSize)/1024/1024:.2f} MB")
            total_patch_size+=int(update.MaxDownloadSize)
            print("--------------------")
        print(f"Total Size of Patches :{int(total_patch_size)/1024/1024:.2f} MB")
        return total_patch_size
    except Exception as e:
        print("Error:", e)
        return 0

if __name__ == "__main__":
    get_available_patches()