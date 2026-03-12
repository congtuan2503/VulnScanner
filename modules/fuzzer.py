import requests
import concurrent.futures
import hashlib

def check_catch_all(url):
    """
    Check if the target domain has a catch-all behavior.
    Returns: (is_catchall, baseline_size, baseline_hash)
    - is_catchall: True if server returns 200 for fake paths
    - baseline_size: Response body size of fake path
    - baseline_hash: MD5 hash of fake path response (for smart detection)
    """
    fake_path = "this_is_a_test_path_12345xyz"
    full_url = f"{url.rstrip('/')}/{fake_path}"

    try:
        r = requests.get(full_url, timeout=5, allow_redirects=False)
        baseline_size = len(r.content)
        baseline_hash = hashlib.md5(r.content).hexdigest()
        
        # If 200 OK for fake path, it's catch-all
        if r.status_code == 200:
            return True, baseline_size, baseline_hash
    except:
        pass
    return False, 0, ""


def check_single_path(url, path, baseline_size=0, baseline_hash="", use_size_detection=False, use_hash_detection=False, is_catchall=False):
    """
    Handle a single URL path check with optional response size/hash detection.
    
    Args:
        url: Base URL
        path: Path to check
        baseline_size: Size of fake path response (for size-based detection)
        baseline_hash: MD5 hash of fake path response (for hash-based detection)
        use_size_detection: Enable/disable size-based detection
        use_hash_detection: Enable/disable hash-based detection (MORE ACCURATE)
        is_catchall: Whether the server is detected as catch-all
    """
    full_url = f"{url.rstrip('/')}/{path.strip()}"

    try:
        r = requests.get(full_url, timeout=10, allow_redirects=False)
        response_size = len(r.content)
        response_hash = hashlib.md5(r.content).hexdigest()
        status = r.status_code
        
        # 403 Forbidden: Directory exists but is forbidden (Always valid regardless of catch-all)
        if status == 403:
            return {"path": path, "status": 403, "url": full_url, "severity": "Medium", "size": response_size}
        
        # 301/302 Redirects: Structural information (Always valid)
        if status in [301, 302]:
            return {"path": path, "status": status, "url": full_url, "severity": "Low", "size": response_size}
        
        # For 200 responses, apply smart detection if catch-all is detected
        if status == 200:
            # If catch-all server detected, MUST use intelligent detection
            if is_catchall and (use_hash_detection or use_size_detection):
                # Hash-based detection (MOST ACCURATE - compare content hash)
                if use_hash_detection and baseline_hash:
                    if response_hash != baseline_hash:
                        # Hash is completely different = real path! ✅
                        return {"path": path, "status": 200, "url": full_url, "severity": "High", "size": response_size, "detection": "hash-based"}
                
                # Size-based detection (FALLBACK - compare content size)
                if use_size_detection and baseline_size > 0:
                    size_diff = abs(response_size - baseline_size)
                    size_variance = (size_diff / baseline_size) * 100
                    
                    # If size differs by more than 10%, it's probably a real path ✅
                    if size_variance > 10:
                        return {"path": path, "status": 200, "url": full_url, "severity": "High", "size": response_size, "detection": "size-based"}
                
                # If catch-all detected but no detection method passed, skip this path
                return None
            
            # Normal server (no catch-all): 200 OK is always valid ✅
            else:
                return {"path": path, "status": 200, "url": full_url, "severity": "High", "size": response_size}
        
    except requests.exceptions.RequestException:
        pass # Skip connection errors
    return None

def run_fuzzer(target_url, wordlist_path, num_threads=10, max_depth=2, use_size_detection=False, use_hash_detection=False):
    """
    Run fuzzer with recursive depth support to scan subdirectories.
    max_depth: How deep to fuzz (1 = only main domain, 2 = domain + one level, etc.)
    use_size_detection: If True, bypass catch-all servers using response body size
    use_hash_detection: If True, bypass catch-all servers using response body hash (MORE ACCURATE)
    """
    print(f"\n[*] STARTING FUZZING: {target_url}")
    print(f"[*] Fuzzing depth: {max_depth} levels")
    if use_hash_detection:
        print("[*] Hash-based detection: ENABLED (most accurate method)")
    elif use_size_detection:
        print("[*] Size-based detection: ENABLED (bypass catch-all servers)")
    
    # 1. Check for Smart 404 (Catch False Positive) with size/hash baseline
    print("[*] Checking if server has Catch-all (Smart 404) mechanism...")
    is_catchall, baseline_size, baseline_hash = check_catch_all(target_url)
    
    if is_catchall:
        if use_hash_detection or use_size_detection:
            if use_hash_detection:
                print(f"[!] WARNING: Catch-all detected but hash detection ENABLED!")
                print(f"[*] Will use response body HASH to identify real paths...")
                print(f"[*] Baseline hash: {baseline_hash[:16]}...")
            else:
                print(f"[!] WARNING: Catch-all detected but size detection ENABLED!")
                print(f"[*] Will use response body SIZE to identify real paths...")
                print(f"[*] Baseline size: {baseline_size} bytes")
        else:
            print("[!] WARNING: This server returns 200 OK for all paths (Catch-all).")
            print("[!] Fuzzing results may be highly inaccurate. Run with --hash-detect or --smart-detect to bypass!")
            return []
    else:
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
            future_to_path = {executor.submit(check_single_path, base_url, path, baseline_size, baseline_hash, use_size_detection, use_hash_detection, is_catchall): path for path in paths}
            
            for future in concurrent.futures.as_completed(future_to_path):
                result = future.result()
                if result:
                    found_assets.append(result)
                    valid_paths.append(result['path'])
                    detection_note = f" (detected via {result.get('detection')})" if result.get('detection') else ""
                    print(f"   [+] Response {result['status']} | {result['url']}{detection_note}")
        
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