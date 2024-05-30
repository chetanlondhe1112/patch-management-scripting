import requests

# URL of the FastAPI endpoint
url = "http://103.159.85.174:8443/uploadfile/"

# The form data to be sent
data = {
    "ClientID": "CN001",
    "Status": "True"
}

# The file to be uploaded
file_path = "F:/patch-managment-project-16/patch-management-scripting/patchmgt/dev/apis/taetoagent/study/req.py"
files = {
    "file": open(file_path, "rb")
}

# Sending the POST request
try:
    response = requests.post(url, data=data, files=files)

    # Print the response from the server
    print(response.status_code)
    print(response.json())
except Exception as e:
    print(e)
