#check the space available or not and then install 
import os
import psutil
import winreg

def create_dummy_file():
    if not os.path.exists(dummy_file_path):
        try:
            os.makedirs(os.path.dirname(dummy_file_path), exist_ok=True)
            with open(dummy_file_path, 'w') as f:
                f.write("This is a dummy patch file.")
            print("Dummy patch file created successfully at:", dummy_file_path)
        except Exception as e:
            print("Error creating dummy patch file:", e)
    else:
        print("Dummy patch file already exists at:", dummy_file_path)

def create_registry_entry():
    key_path = r"SOFTWARE\Patches"
    value_name = "DummyPatchFile"
    dummy_file_path = 'C:\\DemoPatch\\dummy_patch.txt'

    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_WRITE)
    except FileNotFoundError:
        key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, key_path)

    # Set the registry value to the path of the dummy file
    winreg.SetValueEx(key, value_name, 0, winreg.REG_SZ, dummy_file_path)
    winreg.CloseKey(key)
    print("Registry entry created successfully.")

def check_disk_space(required_space):
    disk_usage = psutil.disk_usage('/')
    available_space = disk_usage.free
    print("Available disk space:", available_space, "bytes")
    if available_space >= required_space:
        print("Sufficient disk space available for patch installation.")
        return True
    else:
        print("Insufficient disk space available for patch installation.")
        return False

def main():
    required_space = 1024 * 1024  
    if check_disk_space(required_space):
        create_dummy_file()
        create_registry_entry()

if __name__ == "__main__":
    main()