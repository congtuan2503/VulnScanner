# VulnScanner - Automated Web Application Security Scanner

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
![Status](https://img.shields.io/badge/Status-Active-success?style=flat-square)
![Build](https://img.shields.io/badge/Build-Passing-success?style=flat-square)

A high-performance, multi-threaded web vulnerability scanner for discovering hidden assets, sensitive files, and HTTP misconfigurations.

[Features](#features) • [Installation](#installation) • [Usage](#usage) • [Configuration](#configuration) • [Examples](#examples)

</div>

---

## 📋 Overview

**VulnScanner** is a professional-grade reconnaissance tool designed for penetration testers and security researchers. It combines aggressive (but smart) fuzzing with intelligent detection mechanisms to uncover hidden assets and security misconfigurations on target web applications.

### Why VulnScanner?

- 🚀 **Lightning-fast**: Multi-threaded fuzzing with 100+ concurrent requests
- 🧠 **Smart Detection**: Automatically detects and avoids false positives from catch-all servers
- 🔍 **Deep Discovery**: Recursive fuzzing through multiple directory levels
- 📊 **Comprehensive Analysis**: HTTP headers, API endpoints, and sensitive files
- 🎯 **Production-Ready**: Graceful error handling and clear reporting
- 🔧 **Flexible**: Highly customizable wordlists and fuzzing parameters

---

## ✨ Key Features

### Core Capabilities

| Feature | Description |
|---------|-------------|
| **Multi-threaded Fuzzing** | Uses `concurrent.futures` for rapid, asynchronous path discovery |
| **Recursive Directory Discovery** | Automatically explores subdirectories based on user-defined depth levels |
| **Smart 404 Detection** | Detects catch-all behavior to prevent reporting false positives |
| **HTTP Header Analysis** | Identifies information disclosure and missing security headers |
| **Customizable Wordlists** | 1,200+ built-in sensitive paths including Spring Boot actuators, API endpoints, and configuration files |
| **Real-time Output** | Immediate terminal feedback as assets are discovered |
| **Severity Scoring** | Rates findings as High, Medium, or Low based on response code and risk level |

### Supported Scanning Techniques

- **Directory Enumeration**: `/admin`, `/api`, `/backup`, etc.
- **File Discovery**: Finds exposed files like `.env`, `config.php`, `backup.zip`
- **API Endpoint Mapping**: Discovers REST, GraphQL, and SOAP endpoints
- **Framework Detection**: Spring Boot actuators, WordPress, Joomla, Drupal paths
- **DevOps Exposure**: Docker, Kubernetes, CI/CD configuration paths
- **Security Header Analysis**: Checks for HSTS, CSP, X-Frame-Options, and more

---

## 🔧 Requirements

- **Python 3.8+** (tested on 3.8, 3.9, 3.10, 3.11)
- **macOS**, **Linux**, **Windows** (WSL recommended for Windows)
- **Stable Internet Connection** (for target connectivity)
- **500 MB** disk space (for wordlists and reports)

---

## 📦 Installation

### Option 1: Clone from Repository

```bash
# Clone the repository
git clone https://github.com/congtuan2503/VulnScanner.git
cd VulnScanner

# Install dependencies
pip install -r requirements.txt
```

### Option 2: Local Installation

```bash
# Create a virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Verify Installation

```bash
python main.py -h
```

---

## 🚀 Quick Start

### Basic Usage

```bash
# Simple scan with defaults (10 threads, depth 2)
python main.py -u https://target.com
```

### Advanced Usage

```bash
# Aggressive scan: 100 threads, 3 levels deep, custom wordlist
python main.py -u https://target.com -t 100 -d 3 -w wordlists/aggressive.txt
```

### With All Options

```bash
python main.py \
  -u https://target.com \
  -w wordlists/common.txt \
  -t 50 \
  -d 2
```

---

## 📖 Configuration & Arguments

### Command-Line Arguments

```
usage: python main.py [-h] -u URL [-w WORDLIST] [-t THREADS] [-d DEPTH]

optional arguments:
  -h, --help                    Show this help message and exit
  -u URL, --url URL             Target URL (REQUIRED)
                                Example: https://example.com
  
  -w WORDLIST, --wordlist       Path to wordlist file
                                Default: wordlists/common.txt
                                
  -t THREADS, --threads         Number of concurrent threads
                                Default: 10
                                (Higher = faster, but more aggressive)
                                
  -d DEPTH, --depth             Fuzzing depth levels
                                Default: 2
                                1 = root paths only
                                2 = root + 1 subdirectory level
                                3+ = deeper recursive scanning
```

### Wordlist Selection Guide

| Wordlist | Size | Use Case |
|----------|------|----------|
| `common.txt` | 1,200+ paths | Default - balanced for speed & coverage |
| `aggressive.txt` | 5,000+ paths | Comprehensive testing (slower) |
| `api-only.txt` | API endpoints | Focus on API discovery |
| `custom.txt` | 100-500 paths | Custom targets (fastest) |

---

## 💡 Usage Examples

### Example 1: Basic Reconnaissance

```bash
$ python main.py -u https://demo.owasp-juice.shop

============================================================
 VULNERABILITY & ASSET SCANNER - INITIALIZED
============================================================

[--- PHASE 1: HTTP SECURITY HEADERS SCAN ---]
[*] Checking HTTP Headers configuration for: https://demo.owasp-juice.shop
  -[Low] Missing Strict-Transport-Security
  -[Low] Missing X-Frame-Options

[--- PHASE 2: DIRECTORY/FILE FUZZING ---]
[*] STARTING FUZZING: https://demo.owasp-juice.shop
[*] Fuzzing depth: 2 levels
[*] Checking if server has Catch-all (Smart 404) mechanism...
[+] Server configuration is standard, starting recursive multi-threaded scan...
[*] Fuzzing depth level 1/2...
[*] Running with 10 threads...
   [+] Response 200 | https://demo.owasp-juice.shop/api
   [+] Response 200 | https://demo.owasp-juice.shop/rest
   [+] Response 200 | https://demo.owasp-juice.shop/admin

[*] Fuzzing depth level 2/2...
[*] Diving deeper into: https://demo.owasp-juice.shop/api
   [+] Response 200 | https://demo.owasp-juice.shop/api/users
   [+] Response 200 | https://demo.owasp-juice.shop/api/products
   [+] Response 403 | https://demo.owasp-juice.shop/api/admin

============================================================
 SCAN COMPLETED! SUMMARY:
 - Header/Misconfig issues found: 2
 - Hidden assets discovered: 6

 [DISCOVERED ASSETS:]
   [200] https://demo.owasp-juice.shop/admin (High)
   [200] https://demo.owasp-juice.shop/api (High)
   [200] https://demo.owasp-juice.shop/api/users (High)
   [200] https://demo.owasp-juice.shop/api/products (High)
   [200] https://demo.owasp-juice.shop/rest (High)
   [403] https://demo.owasp-juice.shop/api/admin (Medium)

============================================================
```

### Example 2: Aggressive API Scanning

```bash
python main.py -u https://api.target.com -t 100 -d 3 -w wordlists/api-only.txt
```

### Example 3: Quick Local Testing

```bash
python main.py -u http://localhost:8080 -t 50 -d 2
```

---

## 📁 Project Structure

```
VulnScanner/
├── main.py                          # Entry point & CLI handler
├── requirements.txt                 # Python dependencies
├── README.md                        # This file
│
├── modules/
│   ├── __init__.py
│   ├── scanner.py                  # HTTP headers & misconfig scanning
│   ├── fuzzer.py                   # Multi-threaded recursive fuzzing
│   └── reporter.py                 # Report generation (future)
│
├── wordlists/
│   └── common.txt                  # 1,200+ paths for fuzzing
│
└── templates/
    └── report_template.html        # HTML report template (future)
```

---

## 🎯 How It Works

### 1. **Initialization Phase**
```
Input Target URL
     ↓
Parse & Validate URL
     ↓
Load Wordlist
```

### 2. **Smart 404 Detection**
```
Send request to fake path: /this_is_a_test_path
     ↓
Check response status code
     ↓
If 200 → Server has Catch-all (STOP - too many false positives)
If 404 → Server is Normal (CONTINUE with fuzzing)
```

### 3. **Multi-threaded Fuzzing**
```
Wordlist [/admin, /api, /backup, ...]
     ↓
Create thread pool (size = --threads)
     ↓
Dispatch: /target.com/admin
          /target.com/api
          /target.com/backup (parallel)
     ↓
Collect responses (200, 403, 301, etc.)
     ↓
Return valid paths
```

### 4. **Recursive Scanning** (if depth > 1)
```
Discovered: /admin, /api, /backup
     ↓
Filter: Skip files (.zip, .php, .sql) ← prevents false descents
     ↓
For each directory:
  - /target.com/admin/ + wordlist
  - /target.com/api/ + wordlist
  - /target.com/backup/ + wordlist
     ↓
Aggregate all results
```

### 5. **Summary & Output**
```
Compile all findings
     ↓
Sort by severity (High → Low)
     ↓
Print terminal report
     ↓
[Future] Generate HTML report
```

---

## ⚙️ Performance Tips

### Recommended Settings by Target Type

| Target Type | Threads | Depth | Wordlist | Est. Time |
|------------|---------|-------|----------|-----------|
| Small site (< 50 paths) | 10 | 2 | common.txt | 30s |
| Medium site (50-200 paths) | 50 | 2 | common.txt | 1-2m |
| Large/Enterprise | 100 | 3 | aggressive.txt | 5-10m |
| API-only | 50 | 3 | api-only.txt | 1-2m |

### Optimization Guide

```bash
# Faster but less thorough (good for quick recons)
python main.py -u https://target.com -t 100 -d 1

# Balanced (default, recommended)
python main.py -u https://target.com -t 10 -d 2

# Thorough but slower (comprehensive testing)
python main.py -u https://target.com -t 50 -d 3 -w wordlists/aggressive.txt
```

### Bandwidth Considerations

- **10 threads**: ~1-5 MB/min
- **50 threads**: ~5-25 MB/min  
- **100 threads**: ~10-50 MB/min

*Adjust based on your network and target's rate limiting*

---

## 🐛 Troubleshooting

### Issue: "Connection timeout" errors

**Solution:**
```bash
# Reduce threads (less concurrent requests)
python main.py -u https://target.com -t 5 -d 1

# Increase timeout in fuzzer.py (modify timeout=10)
```

### Issue: Catch-all server detected

**Meaning:** This target returns 200 OK for any path, making fuzzing unreliable.

**Solutions:**
- Try a different target
- Look for a staging/dev version: `staging.target.com`
- Manually test specific paths you suspect

### Issue: Scanner not finding hidden paths

**Check these:**
1. Is the URL correct? `https://` vs `http://`
2. Is the target accessible from your network?
3. Use a smaller wordlist for testing: `grep "admin\|api" wordlists/common.txt`
4. Try `-d 1` to see if depth 2 is causing issues

### Issue: "Permission denied" on wordlist

```bash
# Fix file permissions
chmod 644 wordlists/common.txt
```

---

## 🔒 Responsible Disclosure

⚠️ **LEGAL WARNING**

This tool is designed for **authorized security testing only**:

✅ **Legal Use Cases:**
- Bug bounty programs (with explicit permission)
- Authorized penetration testing engagements
- Your own applications and infrastructure
- Educational labs (OWASP Juice Shop, HackTheBox, etc.)

❌ **Illegal Use:**
- Scanning targets without authorization
- Unauthorized vulnerability disclosure
- DoS/DDoS attacks (setting high thread counts)
- Data theft or unauthorized access

**The author is not responsible for misuse or damage caused by this tool.**

---

## 📊 What VulnScanner Finds

### High Severity
- Exposed admin panels: `/admin`, `/administrator`
- Accessible APIs: `/api/users`, `/api/admin`, `/api/internal`
- Sensitive files: `backup.zip`, `.env`, `config.php`

### Medium Severity
- Forbidden paths: 403 responses indicating real structures
- Dev endpoints: `/debug`, `/test`, `/dev`
- Authentication bypass: `/login`, `/password/reset`

### Low Severity
- Redirects: Structural information (301/302)
- Framework indicators: `/wp-admin`, `/api/v1`
- Information disclosure: Server version leaks

---

## 🛠️ Development

### Adding Custom Wordlists

1. Create a new file: `wordlists/my-custom.txt`
2. Add paths (one per line):
   ```
   /secret
   /admin/panel
   /api/v2/internal
   ```
3. Run with custom wordlist:
   ```bash
   python main.py -u https://target.com -w wordlists/my-custom.txt
   ```

### Extending the Scanner

```python
# In modules/scanner.py - add new check:
def check_cors_headers(target_url):
    response = requests.get(target_url)
    if 'Access-Control-Allow-Origin' in response.headers:
        # CORS misconfiguration detected
        pass
```

### Contributing

Contributions are welcome! Areas for improvement:
- [ ] HTML report generation
- [ ] Export to JSON/CSV
- [ ] Proxy support
- [ ] Authentication (Basic, OAuth)
- [ ] Custom headers and cookies
- [ ] Payloads for parameter fuzzing

---

## 📄 License
Copyright (c) 2026 [tunadafish]. All rights reserved.

---

## 🔗 References & Resources

### Learning Paths
- [OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
- [HackTheBox](https://www.hackthebox.com/) - Practice targets
- [OWASP Juice Shop](https://demo.owasp-juice.shop/) - Vulnerable app for testing

### Similar Tools
- **Burp Suite**: Full-featured, commercial
- **ZAP**: Free, full-featured
- **Gobuster**: Lightweight, Go-based
- **ffuf**: FastAPI fuzzer, very fast
- **wfuzz**: Flexible Python-based fuzzer

### Security Resources
- [Common Vulnerability Types](https://owasp.org/www-project-top-ten/)
- [API Security Best Practices](https://cheatsheetseries.owasp.org/cheatsheets/REST_API_Security_Cheat_Sheet.html)
- [HTTPD Security Headers](https://securityheaders.com/)

---

## 📞 Support & Contact

- **Report Issues**: [GitHub Issues](https://github.com/congtuan2503/VulnScanner/issues)
- **Security Bugs**: congtuancontact@gmail.com
- **Questions**: congtuancontact@gmail.com

---

<div align="center">

**Made with ❤️ by tunadafish**

[⬆ back to top](#vulnscanner---automated-web-application-security-scanner)

</div>