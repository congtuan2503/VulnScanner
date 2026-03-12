import requests

def check_security_headers(target_url):
    print(f"[*] Checking HTTP Headers configuration for: {target_url}")
    vulnerabilities = []

    try:
        response = requests.get(target_url, timeout=10)
        headers = response.headers

        # INFO DISCLOSURE: Check headers that may leak server or technology information
        if 'Server' in headers:
            vulnerabilities.append({
                "type": "Information Disclosure",
                "name": "Server Version Leaked",
                "detail": f"Server version detected: {headers['Server']}",
                "severity": "Medium"
            })

        if 'X-Powered-By' in headers:
            vulnerabilities.append({
                "type": "Information Disclosure",
                "name": "Technology Stack Leaked",
                "detail": f"Backend technology exposed: {headers['X-Powered-By']}",
                "severity": "Low" 
            })
        
        # SECURITY HEADERS: Check important security headers
        security_headers =[
            "Strict-Transport-Security", # Force browser to use HTTPS
            "X-Frame-Options",           # Protect against Clickjacking attacks
            "Content-Security-Policy"    # Protect against XSS attacks
        ]
        
        for header in security_headers:
            if header not in headers:
                vulnerabilities.append({
                    "type": "Missing Security Header",
                    "name": f"Missing {header}",
                    "detail": f"Website is missing {header} header, which may lead to frontend security risks.",
                    "severity": "Low"
                })
    except requests.exceptions.RequestException as e:
        print(f"[!] Connection error to {target_url}: {e}")
        return None
    
    return vulnerabilities
    