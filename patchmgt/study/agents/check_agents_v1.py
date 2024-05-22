import subprocess

def check_installed_agents():
    try:
        # Run the command to list running services/processes
        result = subprocess.run(['tasklist'], capture_output=True, text=True)
        if result.returncode == 0:
            running_processes = result.stdout.split('\n')
            agents = [process.strip() for process in running_processes if 'Agent' in process]
            if agents:
                print("Agents installed on the system:")
                for agent in agents:
                    print(agent)
            else:
                print("No agent found on the system.")
        else:
            print("Error:", result.stderr)
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    check_installed_agents()