import subprocess

def check_patch_agents():
    try:
        # Run the command to list running services/processes
        result = subprocess.run(['tasklist'], capture_output=True, text=True)
        if result.returncode == 0:
            running_processes = result.stdout.split('\n')
            patch_agents = [process.strip() for process in running_processes if is_patch_agent(process)]
            if patch_agents:
                print("Patch agents available on the system:")
                for agent in patch_agents:
                    print(agent)
            else:
                print("No patch agents found on the system.")
        else:
            print("Error:", result.stderr)
    except Exception as e:
        print("Error:", e)

def is_patch_agent(process_name):
    # Define keywords commonly associated with patch agents
    patch_agent_keywords = ["WSUS", "SCCM", "Patch Manager", "PatchAgent", "PatchService", "UpdateManager", "PatchUpdate"]
    # Check if any keyword matches the process name
    for keyword in patch_agent_keywords:
        if keyword in process_name:
            return True
    return False

if __name__ == "__main__":
    check_patch_agents()