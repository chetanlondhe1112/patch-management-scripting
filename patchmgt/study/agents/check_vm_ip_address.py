import winrm

# Connect to the Windows VM
vm_host = "192.168.245.75"
username = "Chetanl.ext"
password = "Wonder@#$098765"
session = winrm.Session(vm_host, auth=(username, password))

# Construct PowerShell command to get IP address
ps_script = "(Get-NetIPAddress | Where-Object {$_.AddressFamily -eq 'IPv4'}).IPAddress"

# Execute PowerShell command
result = session.run_ps(ps_script)
if result.status_code == 0:
    ip_addresses = result.std_out.strip().split('\n')
    for ip in ip_addresses:
        print(f"IP Address: {ip}")
else:
    print("Failed to get IP address.")