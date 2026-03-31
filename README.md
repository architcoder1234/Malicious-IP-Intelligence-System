# 🛡️ Malicious IP Intelligence System

A Python-based cybersecurity tool that checks whether IP addresses are malicious and generates detailed AI-powered threat intelligence reports using **AbuseIPDB** and **OpenAI**.

---

## 🚀 Features

- 🔍 Checks multiple IPs against the AbuseIPDB threat database
- 🤖 Uses OpenAI GPT to generate human-readable threat intelligence reports
- 📊 Exports results to a CSV report
- ⚡ Fast and easy to use from the terminal

---

## 🖥️ Demo

```
Enter IPs to scan → Tool checks AbuseIPDB → OpenAI generates report → Results saved to report.csv
```

---

## 🔧 Requirements

- Python 3.8+
- An **AbuseIPDB** API key
- An **OpenAI** API key

Install dependencies:
```bash
pip install openai requests python-dotenv
```

---

## 🔑 How to Get the API Keys

### 1. AbuseIPDB API Key (Free)
1. Go to 👉 [https://www.abuseipdb.com/register](https://www.abuseipdb.com/register)
2. Create a free account
3. After logging in, go to **Account → API**
4. Click **"Create Key"**
5. Copy your API key

> Free plan allows **1,000 checks/day** — enough for most use cases.

---

### 2. OpenAI API Key
1. Go to 👉 [https://platform.openai.com/signup](https://platform.openai.com/signup)
2. Create an account (or log in)
3. Go to **API Keys** section: [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
4. Click **"Create new secret key"**
5. Copy your key immediately — you won't see it again!

> ⚠️ OpenAI requires adding credits to your account for API usage. Go to **Settings → Billing** to add a payment method.

---

## ⚙️ Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/architcoder1234/Malicious-IP-Intelligence-System.git
cd Malicious-IP-Intelligence-System
```

### 2. Install dependencies
```bash
pip install openai requests python-dotenv
```

### 3. Create a `.env` file
In the project folder, create a file named `.env` and add your API keys:
```
OPENAI_API_KEY=your-openai-key-here
ABUSEIPDB_API_KEY=your-abuseipdb-key-here
```

> ⚠️ Never share your `.env` file or push it to GitHub!

### 4. Add IPs to scan
Edit the `ips.txt` file and add the IP addresses you want to check, one per line:
```
192.168.1.1
8.8.8.8
45.33.32.156
```

### 5. Run the tool
```bash
python main.py
```

Results will be saved to `report.csv`.

---

## 📁 Project Structure

```
Malicious-IP-Intelligence-System/
├── main.py          # Main entry point
├── app1.py          # Core logic & API integrations
├── config.py        # Configuration settings
├── ips.txt          # List of IPs to scan
├── .gitignore       # Files excluded from git
└── README.md        # You're reading this!
```

---

## 🔒 Security Notice

- Never hardcode API keys in your source code
- Always use a `.env` file to store secrets
- Make sure `.env` is listed in your `.gitignore`

---

## 👨‍💻 Author

**Archit** — [@architcoder1234](https://github.com/architcoder1234)

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
