import argparse
import sys
import os
from colorama import init, Fore, Style
from modules.scanner import check_security_headers
from modules.fuzzer import run_fuzzer
from modules.reporter import generate_html_report

# Khởi tạo colorama (autoreset=True để màu tự reset sau mỗi dòng print)
init(autoreset=True)

def print_banner():
    banner = f"""{Fore.CYAN}{Style.BRIGHT}
  _   _       _          _____                                  
 | | | |     | |        / ____|                                 
 | | | |_   _| | _ __  | (___   ___ __ _ _ __  _ __   ___ _ __  
 | | | | | | | || '_ \  \___ \ / __/ _` | '_ \| '_ \ / _ \ '__| 
 | |_| | |_| | || | | | ____) | (_| (_| | | | | | | |  __/ |    
  \___/ \__,_|_||_| |_||_____/ \___\__,_|_| |_|_| |_|\___|_|    
    {Fore.YELLOW}Automated Misconfig & Directory Fuzzer v1.0
    {Fore.WHITE}Author: tunadafish | Target: Educational Purposes Only
    """
    print(banner)

def main():
    parser = argparse.ArgumentParser(description="Web Pentest Automation Tool - Misconfig & Directory Scanner")
    parser.add_argument("-u", "--url", help="Target URL (e.g., https://example.com)", required=True)
    parser.add_argument("-w", "--wordlist", help="Path to the wordlist file", default="wordlists/common.txt")
    parser.add_argument("-t", "--threads", help="Number of concurrent threads", type=int, default=10)
    parser.add_argument("-d", "--depth", help="Fuzzing depth levels (default: 2)", type=int, default=2)
    parser.add_argument("-o", "--output", help="Output report filename", default="report.html")
    
    args = parser.parse_args()
    target_url = args.url
    
    print_banner()
    
    try:
        # --- PHASE 1: SCAN HTTP HEADERS ---
        print(f"{Fore.MAGENTA}[--- PHASE 1: HTTP SECURITY HEADERS SCAN ---]")
        scan_results = check_security_headers(target_url)
        if scan_results:
            for vuln in scan_results:
                # Tô màu theo mức độ (Severity)
                if vuln['severity'] == 'High':
                    color = Fore.RED
                elif vuln['severity'] == 'Medium':
                    color = Fore.YELLOW
                else:
                    color = Fore.CYAN
                    
                print(f"  {color}[{vuln['severity']}] {vuln['name']}: {vuln['detail']}")
        elif scan_results is not None:
            print(f"  {Fore.GREEN}[Info] No common header misconfigurations found.")
                
        # --- PHASE 2: DIRECTORY FUZZING ---
        print(f"\n{Fore.MAGENTA}[--- PHASE 2: DIRECTORY/FILE FUZZING ---]")
        fuzz_results = run_fuzzer(target_url, args.wordlist, args.threads, args.depth)
        
        # --- SUMMARY ---
        print(f"\n{Fore.BLUE}" + "=" * 60)
        print(f"{Fore.BLUE}{Style.BRIGHT} SCAN COMPLETED! SUMMARY:")
        if scan_results is not None:
            print(f" - Header/Misconfig issues found: {len(scan_results)}")
        print(f" - Hidden assets discovered: {len(fuzz_results)}")
        
        if fuzz_results:
            print(f"\n{Fore.GREEN} [DISCOVERED ASSETS:]")
            for result in sorted(fuzz_results, key=lambda x: x['url']):
                color = Fore.RED if result['status'] == 200 else Fore.YELLOW
                print(f"   {color}[{result['status']}] {result['url']} ({result['severity']})")
        
        print(f"{Fore.BLUE}" + "=" * 60)

        # --- PHASE 3: REPORTING ---
        generate_html_report(target_url, scan_results, fuzz_results, args.output)

    except KeyboardInterrupt:
        # Xử lý khi người dùng bấm Ctrl+C (Graceful Exit)
        print(f"\n{Fore.RED}[!] Nhận tín hiệu ngắt từ người dùng (Ctrl+C). Đang dừng chương trình...")
        
        # Thoát hoàn toàn chương trình, cắt đứt mọi luồng (threads) đang chạy
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

if __name__ == "__main__":
    main()