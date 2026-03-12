import os
from datetime import datetime
from jinja2 import Environment, FileSystemLoader

def generate_html_report(target_url, scan_results, fuzz_results, output_filename="report.html"):
    print("\n[*] Generating HTML Report...")
    
    try:
        # 1. Setup Jinja2 Environment to look in the 'templates' folder
        template_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates')
        env = Environment(loader=FileSystemLoader(template_dir))
        
        # 2. Load the template file
        template = env.get_template('report_template.html')
        
        # 3. Render the template with our data
        scan_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        html_content = template.render(
            target_url=target_url,
            scan_date=scan_date,
            scan_results=scan_results,
            fuzz_results=fuzz_results
        )
        
        # 4. Save to a file
        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
            
        print(f"[+] Report successfully generated: {os.path.abspath(output_filename)}")
        return True
        
    except Exception as e:
        print(f"[!] Failed to generate report: {e}")
        return False