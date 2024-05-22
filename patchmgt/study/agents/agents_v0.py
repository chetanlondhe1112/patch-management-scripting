#agents
import ctypes
import datetime as dt
import win32com.client
import psutil
import win32serviceutil
import os
import subprocess
import csv
#defaults
time_zone=""
patch_file_path = "C:\demo_patches"  # Replace with the path to your patch file
log_file_path = "log.csv"


def time_collector():
    return dt.datetime.now()

def log_generator(log_time,log_code,log_status):
    file_path=log_file_path
    log_data = {
        "StartTime": log_time,
        "event": log_code,
        "details":log_status,
    }
    # Write the log data to the CSV file
    write_log_to_csv(log_data, file_path)

def write_log_to_csv(log_data, file_path):
    # Define field names for the CSV file
    field_names = ["StartTime", "Event", "Details"]
    
    # Open the CSV file in append mode
    with open(file_path, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=field_names)
        
        # Write header if the file is empty
        if file.tell() == 0:
            writer.writeheader()
        
        # Write log data to the CSV file
        writer.writerow({
            "StartTime": log_data["StartTime"],
            "Event": log_data["event"],
            "Details": log_data["details"]
        })

def check_system_status():
    check_start_time=time_collector()
    try:
        # Call GetTickCount function to get system uptime in milliseconds
        uptime_ms = ctypes.windll.kernel32.GetTickCount()
        
        # If uptime is greater than zero, system is running
        if uptime_ms > 0:
            check_end_time=time_collector()
            print("System is ON.")
            return 1,"System is ON.",{"check_start_time":check_start_time,"check_end_time":check_end_time}
        else:
            check_end_time=time_collector()
            print("System is OFF.")
            return 0,"System is OFF.",{"check_start_time":check_start_time,"check_end_time":check_end_time}
        
    except Exception as e:
        print("Error:", e)
        return 0,e,{"check_start_time":check_start_time,"check_end_time":check_end_time}

def get_available_patches_v3():
    try:
        patches = {}
        
        # Create a Windows Update Agent object
        update_session = win32com.client.Dispatch("Microsoft.Update.Session")
        
        # Create a Windows Update Searcher object
        update_searcher = update_session.CreateUpdateSearcher()
        
        # Search for updates that are not installed
        search_result = update_searcher.Search("IsInstalled=0")
        
        # List available updates along with their KB numbers
        count=0
        total_patch_size=0
        print("All Available Patches:")
        for update in search_result.Updates:
            kb_numbers = ', '.join(update.KBArticleIDs)
            patch_info = {
                'PatchName': update.Title,
                'PatchNumber': kb_numbers,
                'patchID':update.Identity.UpdateID,
                'PatchSize': int(update.MaxDownloadSize) / (1024 ** 2)  # Size in MB
            }

            count+=1
            print(f"\t{count})")
            print(f"\tUpdate Title: {update.Title}")
            print(f"KB id: {kb_numbers}")
            print(f"\tUpdate ID: {update.Identity.UpdateID}")
            print(f"\tUpdate Size: {int(update.MaxDownloadSize)/1024/1024:.2f} MB")

            total_patch_size+=int(update.MaxDownloadSize)

            patches[kb_numbers]=patch_info

            print("--------------------")

        print(f"Total Size of Patches :{int(total_patch_size)/1024/1024:.2f} MB")
        return patches,total_patch_size

    except Exception as e:
        print("Error:", e)
        return 0,0

def get_available_patches_v2():
    try:
        # Create a Windows Update Agent object
        update_session = win32com.client.Dispatch("Microsoft.Update.Session")
        
        # Create a Windows Update Searcher object
        update_searcher = update_session.CreateUpdateSearcher()
        
        # Search for updates that are not installed
        search_result = update_searcher.Search("IsInstalled=0")
        
        # List available updates along with their KB numbers
        
        for update in search_result.Updates:
            kb_numbers = ', '.join(update.KBArticleIDs)
            print(f"Update Title: {update.Title}")
            print(f"KB Numbers: {kb_numbers}")
            print("--------------------")
    except Exception as e:
        print("Error:", e)

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

def check_c_drive_space():
    try:
        # Get disk usage of the C drive
        disk_usage = psutil.disk_usage('C:\\')
        # Convert bytes to GB
        free_space=disk_usage.free
        free_space_gb = free_space/ (1024 ** 3)
        # Print the disk space information
        print("C Drive Space Information:")
        print(f"Free Space: {free_space_gb:.2f} GB")
        return free_space
    except Exception as e:
        print("Error:", e)
        return 0

def check_system_space_available(avl_space,required_space):
    space=avl_space-required_space
    if space>0:
        print(f"C drives Available Space:{int(space)/1024/1024:.2f} MB")
        print("Space Is available")
        return "Space Is available",space
    else:
        print(f"C drives Available Space:{int(space)/1024/1024:.2f} MB")
        print("Space Is not available")
        return "Space Is not available",space
    
def check_windows_update_services():
    try:
        # Check if the Windows Update service is running
        wua_running = win32serviceutil.QueryServiceStatus('wuauserv')[1] == 4

        # Check if the Background Intelligent Transfer Service (BITS) is running
        bits_running = win32serviceutil.QueryServiceStatus('bits')[1] == 4

        # Print status of Windows Update services
        print("Windows Update Service:", "Running" if wua_running else "Not Running")
        print("BITS Service:", "Running" if bits_running else "Not Running")
        return 1
    except Exception as e:
        print("Error:", e)
        return 0
       
def install_patch(kb_number):
    try:
        if not kb_number:
            print("Error: KB number is empty.")
            return 'no patch number','Installation Failed',''

        # Install the patch using wusa.exe
        cmd = f"wusa.exe /quiet /norestart /update {kb_number}"
        subprocess.run(cmd, shell=True, check=True)
        print(f"Patch {kb_number} installed successfully.")
        return kb_number,'Installation Succeed',''
    except subprocess.CalledProcessError as e:
        print(f"Error: Failed to install patch {kb_number}.")
        print("Exit status:", e.returncode)
        return kb_number,'Installation Failed',e.returncode
    except Exception as e:
        print("Error:", e)
        return kb_number,'Installation Failed',e

def download_and_install_patch(patch_file_path):
    try:
        # Check if the patch file exists
        if not os.path.exists(patch_file_path):
            print(f"Patch file '{patch_file_path}' not found.")
            return

        # Install the patch using wusa.exe
        cmd = f"wusa.exe {patch_file_path} /quiet /norestart"
        subprocess.run(cmd, shell=True, check=True)
        print("Patch installed successfully.")
    except subprocess.CalledProcessError as e:
        print("Error:", e)
    except Exception as e:
        print("Error:", e)


# Provide the KB numbers of patches to install

#if __name__ == "__main__":

start_time=time_collector()
log_generator(start_time,"Starting Agent",'')

check_status,mess,check_time=check_system_status()
log_generator('',"System Check",mess)

free_space=check_c_drive_space()
patches,total_patch_size=get_available_patches_v3()
space_mess,space=check_system_space_available(avl_space=free_space,required_space=total_patch_size)
log_generator('',"System Space Availabilty Check",str(space_mess)+":"+str(int(space)/1024/1024/1024)+"GB")

services_status=check_windows_update_services()
if not services_status:
    log_generator('',"Services Check","Service working")

else:
    log_generator('',"System Space Availabilty Check","Service working")

print("Starting Installation:")
for patch in patches:
    print(patch)
    number,status,valid=install_patch(patch)
    log_generator('',"Patch Installation",str( number)+":"+str(status)+":"+str(valid))

end_time=time_collector()
log_generator(end_time,"Agent Stoped",'')




