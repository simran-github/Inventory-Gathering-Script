import base64
import maskpass

def auth():

    username = input("Enter Username: ")
    password = maskpass.askpass(mask="")
    creds = f"{username}:{password}"

    authby = creds.encode("ascii")
    base64_bytes = base64.b64encode(authby) 
    base64_string = base64_bytes.decode("ascii")
    
    return base64_string