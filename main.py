import requests
import pandas as pd
import time
import ipaddress
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# 🔐 Add your API key here
API_KEY = "5938db2d0be00ff0f8853e884647a96061cf20dad2243d619aca7c8e1205dbd7f4b6873db0033e3a"


# 🧠 Classify IP based on score
def classify_ip(score):
    if score > 75:
        return "Malicious"
    elif score > 30:
        return "Suspicious"
    else:
        return "Safe"


# 🚫 Check if IP is private
def is_private_ip(ip):
    try:
        return ipaddress.ip_address(ip).is_private
    except:
        return True


# 🌐 Check IP using AbuseIPDB API
def check_ip(ip):
    url = "https://api.abuseipdb.com/api/v2/check"

    headers = {
        "Key": API_KEY,
        "Accept": "application/json"
    }

    params = {
        "ipAddress": ip,
        "maxAgeInDays": 90
    }

    try:
        response = requests.get(url, headers=headers, params=params)

        # Debug (uncomment if needed)
        # print("DEBUG:", response.status_code, response.text)

        if response.status_code != 200:
            return {
                "IP": ip,
                "Score": "API Error",
                "Country": "-",
                "ISP": "-",
                "Status": "API Error"
            }

        data = response.json().get("data", {})

        score = data.get("abuseConfidenceScore", 0)
        country = data.get("countryCode", "N/A")
        isp = data.get("isp", "N/A")

        status = classify_ip(score)

        return {
            "IP": ip,
            "Score": score,
            "Country": country,
            "ISP": isp,
            "Status": status
        }

    except Exception as e:
        return {
            "IP": ip,
            "Score": "Error",
            "Country": "-",
            "ISP": "-",
            "Status": "Exception"
        }


# 🎨 Colored output
def print_colored(result):
    status = result["Status"]

    if status == "Malicious":
        print(Fore.RED + f"🔴 {result}")
    elif status == "Suspicious":
        print(Fore.YELLOW + f"🟡 {result}")
    elif status == "Safe":
        print(Fore.GREEN + f"🟢 {result}")
    else:
        print(Fore.CYAN + f"⚠️ {result}")


# 🚀 Main execution
def main():
    print(Fore.BLUE + "🔍 Starting Malicious IP Intelligence Scan...\n")

    # 📂 Read IPs (clean + remove empty lines)
    with open("ips.txt") as f:
        ips = [ip.strip() for ip in f if ip.strip()]

    results = []

    for ip in ips:
        print(Fore.WHITE + f"\nChecking {ip}...")

        # 🚫 Skip private IPs
        if is_private_ip(ip):
            print(Fore.CYAN + f"⚠️ Skipping private IP: {ip}")
            continue

        result = check_ip(ip)
        print_colored(result)

        results.append(result)

        time.sleep(2)  # ⏳ avoid API rate limit

    # 📊 Save results
    df = pd.DataFrame(results)
    df.to_csv("report.csv", index=False)

    print(Fore.GREEN + "\n✅ Scan Completed! Report saved as report.csv")


# ▶️ Run program
if __name__ == "__main__":
    main()
