import subprocess

def check_service_status(service_name):
    # Use sc.exe to query the status of the service
    command = f'sc.exe query {service_name}'
    try:
        # Run the command and capture the output
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        # Check if the service exists
        if result.returncode == 0 and service_name in result.stdout:
            # Check if the service is running
            if "STATE" in result.stdout and "RUNNING" in result.stdout:
                print(f"Service '{service_name}' is running.")
                return True
            else:
                print(f"Service '{service_name}' is not running.")
                return False
    except Exception as e:
        print(f"Error checking service '{service_name}': {e}")
        return False

if __name__ == "__main__":
    #Specify the service names you want to check
    service_names = ["wuauserv", "BITS", "Dnscache"]  #Example service names
    #Check the status of each service
    for service_name in service_names:
        check_service_status(service_name)



