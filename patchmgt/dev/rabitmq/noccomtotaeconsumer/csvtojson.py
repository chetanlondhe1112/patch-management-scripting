import pandas as pd

def csv_to_json(csv_file_path, json_file_path):
    try:
        # Read the CSV file into a DataFrame
        df = pd.read_csv(csv_file_path)
        
        # Convert the DataFrame to a JSON file
        df.to_json(json_file_path, orient='records', lines=True)
        
        print(f"CSV file {csv_file_path} has been converted to JSON and saved to {json_file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
csv_file_path = 'F:/patch-managment-project-16/patch-management-scripting/patchmgt/dev/rabitmq/noccomtotaeconsumer/nccom_demo_data.csv'
json_file_path = 'F:/patch-managment-project-16/patch-management-scripting/patchmgt/dev/rabitmq/noccomtotaeconsumer/nccom_demo_data.json'
csv_to_json(csv_file_path, json_file_path)