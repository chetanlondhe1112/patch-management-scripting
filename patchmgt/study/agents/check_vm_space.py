import subprocess

def check_disk_space(vm_host, username, password):
    try:
        # Construct PowerShell command to get disk space
        ps_command = r"Get-WmiObject Win32_LogicalDisk -Filter 'DeviceID=\"C:\"' | Select-Object Size, FreeSpace"

        # Construct PowerShell command with credentials
        ps_command_with_creds = f"$securePassword = ConvertTo-SecureString '{password}' -AsPlainText -Force; " \
                                f"$credential = New-Object System.Management.Automation.PSCredential('{username}', $securePassword); " \
                                f"Invoke-Command -ComputerName {vm_host} -ScriptBlock {{{ps_command}}} -Credential $credential"

        # Execute PowerShell command
        result = subprocess.run(["powershell", "-Command", ps_command_with_creds], capture_output=True, text=True)
        if result.returncode == 0:
            disk_info = result.stdout.strip().split()
            total_size = int(disk_info[0]) / (1024 * 1024 * 1024)  # Convert bytes to GB
            free_space = int(disk_info[1]) / (1024 * 1024 * 1024)  # Convert bytes to GB
            used_space = total_size - free_space
            print(f"Total Disk Space: {total_size:.2f} GB")
            print(f"Used Disk Space: {used_space:.2f} GB")
            print(f"Free Disk Space: {free_space:.2f} GB")
        else:
            print("Failed to get disk space information.")
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    vm_host = input("192.168.248.75")
    username = input("Chetanl.ext")
    password = input("Wonder@#$098765")
    check_disk_space(vm_host, username, password)