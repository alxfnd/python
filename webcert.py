import ssl
import socket
import json

def get_certificate_info(url):      
    try:
        hostname, _ = url.split('://')[1].split('/', 1) 
    
        ssl_ctx = ssl.create_default_context()
        with socket.create_connection((hostname, 443)) as sock:
            with ssl_ctx.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()    
    except Exception as e: 
        print(f"Error: {str(e)}")
        return None
    return cert

def cert_to_json(url):
    certificate_info = get_certificate_info(url)
    if certificate_info: 
        cleaned_cert = {}
        for key, value in certificate_info.items(): 
            if isinstance(value, tuple):
                while isinstance(value[0], tuple):
                    value = value[0]
                cleaned_cert[key] = value[1] if len(value) > 1 else value[0]
            else:
                cleaned_cert[key] = value
        return json.dumps(cleaned_cert, indent=4) 
    else:
        print("Failed to retrieve certificate information.")
        return None

# Example usage:
url = "https://www.google.com/"
json_cert_info = cert_to_json(url) 
if json_cert_info:       
    print(json_cert_info)