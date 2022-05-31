import os

ee_token = os.environ["EARTHENGINE_TOKEN2"]
credential = '{"refresh_token":"%s"}' % ee_token
credential_file_path = os.path.expanduser("~/.config/earthengine/")
os.makedirs(credential_file_path, exist_ok=True)

with open(credential_file_path + "credentials", "w") as file:
    print(credential)
    file.write(credential)