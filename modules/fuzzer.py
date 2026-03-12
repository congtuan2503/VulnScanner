import requests
import concurrent.futures

def check_catch_all(url):
    """
    Check if the target domain has a catch-all email configuration.
    """
    fake_path = "this_is_a_test_path"
    full_url = f"{url.rstrip('/')}/{fake_path}"

    try:
        r = requests.get(full_url, timeout=5, allow_redirects=False)
        if r.status_code == 200:
            return True # Server returns 200 OK for fake paths (Catch-all behavior)
    except:
        pass
    return False


def check_single_path(url, path):
    """
    Handle a single URL path check.
    """
    full_url = f"{url.rstrip('/')}/{path.strip()}"

    try:
        r = requests.get(full_url, timeout=10, allow_redirects=False)

        status = r.status_code
        if status == 200:
            return {"path": path, "status": 200, "url": full_url, "severity": "High"}
        elif status == 403: # 403 Forbidden: Directory exists but is forbidden (Still valuable info)
            return {"path": path, "status": 403, "url": full_url, "severity": "Medium"}
        elif status in[301, 302]: # Page redirected
            return {"path": path, "status": status, "url": full_url, "severity": "Low"}
        
    except requests.exceptions.RequestException:
        pass # Skip connection errors (timeout, network down) without cluttering output
    return None

def run_fuzzer(target_url, wordlist_path, num_threads=10, max_depth=2):
    """
    Run fuzzer with recursive depth support to scan subdirectories.
    max_depth: How deep to fuzz (1 = only main domain, 2 = domain + one level, etc.)
    """
    print(f"\n[*] STARTING FUZZING: {target_url}")
    print(f"[*] Fuzzing depth: {max_depth} levels")
    
    # 1. Check for Smart 404 (Catch False Positive)
    print("[*] Checking if server has Catch-all (Smart 404) mechanism...")
    if check_catch_all(target_url):
        print("[!] WARNING: This server returns 200 OK for all paths (Catch-all).")
        print("[!] Fuzzing results may be highly inaccurate (False Positive). Stopping Fuzzing!")
        return []
    print("[+] Server configuration is standard, starting recursive multi-threaded scan...")

    # 2. Read wordlist file
    try:
        with open(wordlist_path, 'r') as file:
            paths = [line.strip() for line in file.readlines() if line.strip()]
    except FileNotFoundError:
        print(f"[!] Error: Wordlist file not found at {wordlist_path}")
        return []
    
    found_assets = []
    
    # 3. Recursive fuzzing with multiple depth levels
    def fuzz_recursive(base_url, current_depth=1):
        """Recursively fuzz subdirectories"""
        if current_depth > max_depth:
            return
        
        print(f"[*] Fuzzing depth level {current_depth}/{max_depth}...")
        print(f"[*] Running with {num_threads} threads...")
        
        valid_paths = []
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
            future_to_path = {executor.submit(check_single_path, base_url, path): path for path in paths}
            
            for future in concurrent.futures.as_completed(future_to_path):
                result = future.result()
                if result:
                    found_assets.append(result)
                    valid_paths.append(result['path'])
                    print(f"   [+] Response {result['status']} | {result['url']}")
        
        # Continue fuzzing deeper into discovered paths
        if valid_paths and current_depth < max_depth:
            for valid_path in valid_paths:
                # Only dive deeper if the path looks like a directory 
                # (doesn't have a file extension like .php, .zip, .txt)
                if "." not in valid_path.split('/')[-1]: 
                    next_base = f"{base_url.rstrip('/')}/{valid_path.strip()}"
                    print(f"\n[*] Diving deeper into: {next_base}")
                    fuzz_recursive(next_base, current_depth + 1)
                else:
                    print(f"   [-] Skipping recursion on file: {valid_path}")
    
    # Start recursive fuzzing from root
    fuzz_recursive(target_url)
    
    return found_assets