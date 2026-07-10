import requests
import json
import os
import sys
import time

# ==========================================
# 1. UI COLORS & ASSETS
# ==========================================
G = '\033[92m'  # Neon Green
C = '\033[96m'  # Cyan
R = '\033[91m'  # Red
Y = '\033[93m'  # Yellow
W = '\033[0m'   # Reset

BANNER = f"""        
{G}           🜲 𝙂𝙊𝘿 𝘼𝙉𝙏𝙄𝙁𝙄𝙀𝘿𝙉𝙐𝙇𝙇 🜲{W}
{Y}              Made by @cvnze{W}
{C}=========================================================={W}
"""

# ==========================================
# 2. ANIMATIONS & HELPERS
# ==========================================
def spinner(message, delay=0.1, duration=2.5):
    spinner_chars = ['|', '/', '-', '\\']
    end_time = time.time() + duration
    i = 0
    while time.time() < end_time:
        sys.stdout.write(f"\r{Y}[*] {message} {spinner_chars[i % 4]}{W}")
        sys.stdout.flush()
        time.sleep(delay)
        i += 1
    sys.stdout.write(f"\r{G}[+] {message} Done!       {W}\n")

# ==========================================
# 3. CORE API CLIENT
# ==========================================
class AntifiedNullClient:
    def __init__(self, base_url, api_key):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({'Content-Type': 'application/json', 'accept': 'application/json'})

    def init_phase1(self, mobile):
        url = f"{self.base_url}/api/v1/init-phase1?key={self.api_key}"
        try:
            return self.session.post(url, json={"mobile_number": mobile}).json()
        except Exception as e:
            return {"detail": f"Request Failed: {str(e)}"}

    def verify_phase1(self, process_id, otp1):
        url = f"{self.base_url}/api/v1/verify-phase1?key={self.api_key}"
        try:
            return self.session.post(url, json={"process_id": process_id, "otp1": otp1}).json()
        except Exception as e:
            return {"detail": f"Request Failed: {str(e)}"}

    def verify_phase2(self, process_id, otp2, output_filename):
        url = f"{self.base_url}/api/v1/verify-phase2?key={self.api_key}"
        try:
            response = self.session.post(url, json={"process_id": process_id, "otp2": otp2})
            if response.status_code == 200:
                with open(output_filename, "wb") as f:
                    f.write(response.content)
                return {"status": "success", "file": output_filename}
            return response.json()
        except Exception as e:
            return {"detail": f"Request Failed: {str(e)}"}

# ==========================================
# 4. MAIN EXECUTION FLOW
# ==========================================
def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(BANNER)
    
    # Setup
    API_KEY = "demo"
    DOMAIN = "https://antifiednullxosint.com"
    client = AntifiedNullClient(DOMAIN, API_KEY)
    
    print(f"{C}[i] Connecting to Server...{W}")
    time.sleep(1)
    
    # ----------------------------------
    # STEP 1: MOBILE NUMBER ENTRY
    # ----------------------------------
    print("-" * 58)
    mobile = input(f"{G}[?] Enter Target Mobile Number: {W}").strip()
    if not mobile:
        print(f"{R}[!] Mobile number cannot be empty. Exiting.{W}")
        return
        
    spinner("Initializing Phase 1 (Bypassing Captcha)")
    res1 = client.init_phase1(mobile)
    
    if "process_id" not in res1:
        print(f"\n{R}[!] ERROR: {res1.get('detail', res1)}{W}")
        return
        
    process_id = res1['process_id']
    print(f"\n{C}[»] Process ID : {process_id}{W}")
    print(f"{C}[»] Status     : {res1.get('message')}{W}")
    
    # ----------------------------------
    # STEP 2: FIRST OTP (EID)
    # ----------------------------------
    print("-" * 58)
    otp1 = input(f"{Y}[?] Enter EID OTP (Phase 1): {W}").strip()
    
    spinner("Verifying OTP 1 & Extracting Target Info")
    res2 = client.verify_phase1(process_id, otp1)
    
    if "original_name" not in res2:
        print(f"\n{R}[!] ERROR: {res2.get('detail', res2)}{W}")
        return
        
    name = res2['original_name']
    eid = res2['eid_number']
    print(f"\n{G}[✓] TARGET ACQUIRED{W}")
    print(f"{C} ├─ Name : {name}{W}")
    print(f"{C} └─ EID  : {eid}{W}")
    print(f"{C}[»] Status : {res2.get('message')}{W}")
    
    # ----------------------------------
    # STEP 3: SECOND OTP (DOWNLOAD)
    # ----------------------------------
    print("-" * 58)
    otp2 = input(f"{Y}[?] Enter Download OTP (Phase 2): {W}").strip()
    
    safe_name = "".join(c for c in name if c.isalnum())
    pdf_name = f"{safe_name}_Unlocked_Aadhaar.pdf"
    
    spinner("Brute-forcing PDF & Stripping Security")
    res3 = client.verify_phase2(process_id, otp2, pdf_name)
    
    if res3.get("status") == "success":
        print("-" * 58)
        print(f"{G}[★] MISSION ACCOMPLISHED [★]{W}")
        print(f"{C}[✓] File Saved As : {G}{res3['file']}{W}")
        print(f"{C}[✓] Location      : {os.path.abspath(res3['file'])}{W}")
        print("-" * 58)
    else:
        print(f"\n{R}[!] ERROR: {res3.get('detail', res3)}{W}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{R}[!] Process terminated by user.{W}")
        sys.exit()
