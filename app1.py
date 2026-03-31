import streamlit as st
import requests
import pandas as pd
import time
import ipaddress
import matplotlib.pyplot as plt
import matplotlib
from openai import OpenAI

# ─────────────────────────────────────────
#  🔐 API KEYS
# ─────────────────────────────────────────
ABUSEIPDB_API_KEY = "enter your ABUSEIPDB-API-KEY"
OPENAI_API_KEY    = "OPENAI_API_KEY"

client = OpenAI(api_key=OPENAI_API_KEY)

# ─────────────────────────────────────────
#  🎨  PAGE CONFIG
# ─────────────────────────────────────────
st.set_page_config(
    page_title="Malicious IP Intelligence Dashboard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────
#  🎨  GLOBAL CSS  (all selectors verified)
# ─────────────────────────────────────────
HACKER_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');

/* ── Global background & font ── */
html, body, [data-testid="stAppViewContainer"] {
    background-color: #050a0e !important;
    color: #00ff88;
    font-family: 'Share Tech Mono', 'Courier New', monospace;
}

/* ── Animated scanline overlay ── */
[data-testid="stAppViewContainer"]::before {
    content: '';
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background: repeating-linear-gradient(
        0deg,
        transparent,
        transparent 2px,
        rgba(0,255,136,0.015) 2px,
        rgba(0,255,136,0.015) 4px
    );
    pointer-events: none;
    z-index: 9999;
}

/* ── Main content area ── */
[data-testid="stMain"] {
    background: transparent !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0a1628 0%, #050a0e 100%) !important;
    border-right: 1px solid #00ff8833;
}
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] div,
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #00ff88 !important;
}
[data-testid="stSidebar"] [data-baseweb="slider"] div[role="slider"] {
    background: #00ff88 !important;
    border-color: #00ff88 !important;
}

/* ── Headings with gradient text ── */
h1 {
    background: linear-gradient(90deg, #00ff88 0%, #00cfff 50%, #ff00aa 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    text-shadow: none !important;
    filter: drop-shadow(0 0 18px #00ff8855);
}
h2 {
    background: linear-gradient(90deg, #00ff88 0%, #00cfff 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    text-shadow: none !important;
    filter: drop-shadow(0 0 10px #00ff8844);
}
h3 {
    color: #00cfff !important;
    text-shadow: 0 0 8px #00cfff66 !important;
}

/* ── Metric cards with gradient border ── */
[data-testid="metric-container"] {
    background: linear-gradient(135deg, #0a1628 0%, #0d1f0d 100%) !important;
    border: 1px solid transparent !important;
    border-radius: 8px;
    padding: 10px;
    box-shadow: 0 0 12px #00ff8820, inset 0 0 20px #00ff8808;
    position: relative;
}
[data-testid="metric-container"]::before {
    content: '';
    position: absolute;
    inset: 0;
    border-radius: 8px;
    padding: 1px;
    background: linear-gradient(135deg, #00ff88, #00cfff, #ff00aa);
    -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
    -webkit-mask-composite: xor;
    mask-composite: exclude;
    pointer-events: none;
}
[data-testid="metric-container"] label,
[data-testid="metric-container"] div {
    color: #00ff88 !important;
}

/* ── Scan button — gradient glow ── */
.stButton > button {
    background: linear-gradient(90deg, #001a0d, #0a1628) !important;
    color: #00ff88 !important;
    border: 1px solid #00ff8866 !important;
    border-radius: 4px;
    font-family: 'Share Tech Mono', 'Courier New', monospace !important;
    font-weight: bold;
    letter-spacing: 2px;
    transition: all 0.3s;
    box-shadow: 0 0 10px #00ff8822;
}
.stButton > button:hover {
    background: linear-gradient(90deg, #00ff8822, #00cfff22) !important;
    border-color: #00cfff !important;
    box-shadow: 0 0 20px #00cfff66, 0 0 40px #00ff8833;
    color: #00cfff !important;
}

/* ── Download button ── */
.stDownloadButton > button {
    background: linear-gradient(90deg, #001a0d, #00091a) !important;
    color: #00ff88 !important;
    border: 1px solid #00ff8866 !important;
    border-radius: 4px;
    font-family: 'Share Tech Mono', monospace !important;
    font-weight: bold;
    box-shadow: 0 0 10px #00ff8822;
}
.stDownloadButton > button:hover {
    box-shadow: 0 0 20px #00ff8866;
}

/* ── File uploader ── */
[data-testid="stFileUploader"] {
    border: 1px dashed #00ff8855 !important;
    border-radius: 6px;
    background: linear-gradient(135deg, #050a0e, #0a1420) !important;
}
[data-testid="stFileUploader"] span,
[data-testid="stFileUploader"] p,
[data-testid="stFileUploader"] div,
[data-testid="stFileUploader"] small {
    color: #00ff88 !important;
}

/* ── Progress bar — gradient ── */
.stProgress > div > div > div {
    background: linear-gradient(90deg, #00ff88, #00cfff) !important;
    box-shadow: 0 0 8px #00cfff88;
}

/* ── Expander ── */
[data-testid="stExpander"] summary p {
    color: #00cfff !important;
    font-family: 'Share Tech Mono', monospace !important;
}
[data-testid="stExpander"] summary {
    background: linear-gradient(90deg, #0a1628, #050a0e) !important;
    border: 1px solid #00cfff44 !important;
    border-radius: 6px !important;
}
[data-testid="stExpander"] > div:last-child {
    background: linear-gradient(180deg, #0a1628, #050a0e) !important;
    border: 1px solid #00cfff22 !important;
    border-top: none !important;
}

/* ── DataFrame ── */
[data-testid="stDataFrame"] {
    border: 1px solid #00ff8833;
    border-radius: 6px;
    box-shadow: 0 0 20px #00ff8810;
}

/* ── Alert banners ── */
[data-testid="stAlert"] {
    background: linear-gradient(135deg, #001a0d, #00091a) !important;
    border: 1px solid #00ff8855 !important;
    color: #00ff88 !important;
    border-radius: 6px;
    box-shadow: 0 0 10px #00ff8815;
}
[data-testid="stAlert"] p,
[data-testid="stAlert"] div {
    color: #00ff88 !important;
}

/* ── Divider ── */
hr {
    border: none !important;
    height: 1px !important;
    background: linear-gradient(90deg, transparent, #00ff8855, #00cfff55, transparent) !important;
}

/* ── Spinner ── */
[data-testid="stSpinner"] p { color: #00cfff !important; }

/* ── General text ── */
p, li, span, label { color: #00ff88; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: #050a0e; }
::-webkit-scrollbar-thumb {
    background: linear-gradient(180deg, #00ff88, #00cfff);
    border-radius: 3px;
}

/* ── Status badge classes (used via st.markdown) ── */
.badge-malicious {
    display: inline-block;
    padding: 4px 14px;
    border-radius: 20px;
    background: linear-gradient(90deg, #3a0000, #1a0010);
    border: 1px solid #ff4444;
    color: #ff4444;
    font-weight: bold;
    letter-spacing: 1px;
    box-shadow: 0 0 10px #ff444444;
    font-family: 'Share Tech Mono', monospace;
}
.badge-suspicious {
    display: inline-block;
    padding: 4px 14px;
    border-radius: 20px;
    background: linear-gradient(90deg, #1a1400, #100a00);
    border: 1px solid #ffcc00;
    color: #ffcc00;
    font-weight: bold;
    letter-spacing: 1px;
    box-shadow: 0 0 10px #ffcc0044;
    font-family: 'Share Tech Mono', monospace;
}
.badge-safe {
    display: inline-block;
    padding: 4px 14px;
    border-radius: 20px;
    background: linear-gradient(90deg, #001a0d, #00100a);
    border: 1px solid #00ff88;
    color: #00ff88;
    font-weight: bold;
    letter-spacing: 1px;
    box-shadow: 0 0 10px #00ff8844;
    font-family: 'Share Tech Mono', monospace;
}

</style>
"""
st.markdown(HACKER_CSS, unsafe_allow_html=True)


# ─────────────────────────────────────────
#  🧠 HELPER FUNCTIONS
# ─────────────────────────────────────────

def classify_ip(score: int) -> str:
    if not isinstance(score, int):
        return "Error"
    if score > 75:
        return "🔴 Malicious"
    elif score > 30:
        return "🟡 Suspicious"
    return "🟢 Safe"


def status_color(status: str) -> str:
    if "Malicious" in status:
        return "#ff4444"
    if "Suspicious" in status:
        return "#ffcc00"
    return "#00ff88"


def is_private_ip(ip: str) -> bool:
    try:
        return ipaddress.ip_address(ip).is_private
    except Exception:
        return True


def check_ip(ip: str, max_age: int = 90) -> dict:
    url     = "https://api.abuseipdb.com/api/v2/check"
    headers = {"Key": ABUSEIPDB_API_KEY, "Accept": "application/json"}
    params  = {"ipAddress": ip, "maxAgeInDays": max_age}

    try:
        resp = requests.get(url, headers=headers, params=params, timeout=10)
        if resp.status_code != 200:
            return {
                "IP": ip, "Score": "Error", "Country": "-",
                "ISP": "-", "Domain": "-", "Reports": "-",
                "Status": "API Error"
            }
        data  = resp.json().get("data", {})
        score = data.get("abuseConfidenceScore", 0)
        return {
            "IP":      ip,
            "Score":   score,
            "Country": data.get("countryCode", "N/A"),
            "ISP":     data.get("isp", "N/A"),
            "Domain":  data.get("domain", "N/A"),
            "Reports": data.get("totalReports", 0),
            "Status":  classify_ip(score),
        }
    except Exception:
        return {
            "IP": ip, "Score": "Error", "Country": "-",
            "ISP": "-", "Domain": "-", "Reports": "-",
            "Status": "Exception"
        }


def get_ai_mitigation(ip: str, status: str, score) -> str:
    try:
        prompt = (
            f"You are a cybersecurity expert.\n"
            f"IP: {ip} | Status: {status} | Abuse Score: {score}\n\n"
            f"Provide:\n"
            f"1. Why this IP is dangerous (2 lines)\n"
            f"2. Possible attack types (bullet list)\n"
            f"3. Mitigation steps (bullet list)\n"
            f"Keep it concise and practical."
        )
        resp = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[{"role": "user", "content": prompt}],
        )
        return resp.choices[0].message.content
    except Exception:
        return get_basic_mitigation(ip, status, score)


def get_basic_mitigation(ip: str, status: str, score) -> str:
    if "Malicious" in status:
        return (
            f"**🚨 HIGH RISK — Immediate Action Required**\n\n"
            f"- Block `{ip}` in your firewall (iptables / UFW / cloud security group)\n"
            f"- Add to threat blacklist / SIEM watchlist\n"
            f"- Check existing logs for past connections from this IP\n"
            f"- Enable IDS/IPS alert rule for this IP\n"
            f"- Report to AbuseIPDB if not already reported"
        )
    elif "Suspicious" in status:
        return (
            f"**⚠️ SUSPICIOUS — Monitor Closely**\n\n"
            f"- Log all traffic from `{ip}` for 72 hours\n"
            f"- Temporarily restrict inbound access\n"
            f"- Set up threshold-based alerting\n"
            f"- Re-scan after 24 hours"
        )
    return f"✅ `{ip}` appears safe. No action required."


# ─────────────────────────────────────────
#  📊 DASHBOARD HEADER
# ─────────────────────────────────────────

st.markdown("""
<style>
@keyframes gradshift {
  0%   { background-position: 0% 50%; }
  50%  { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}
.cyber-title {
    text-align: center;
    letter-spacing: 4px;
    font-size: 2.2rem;
    font-weight: bold;
    font-family: 'Share Tech Mono', 'Courier New', monospace;
    background: linear-gradient(90deg, #00ff88, #00cfff, #ff00aa, #00ff88);
    background-size: 300% 300%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: gradshift 4s ease infinite;
    filter: drop-shadow(0 0 20px #00ff8855);
}
.cyber-sub {
    text-align: center;
    font-size: 12px;
    letter-spacing: 3px;
    color: #00cfff88;
    font-family: 'Share Tech Mono', monospace;
    margin-top: -6px;
}
</style>
<div class="cyber-title">⬡ MALICIOUS IP INTELLIGENCE SYSTEM ⬡</div>
<div class="cyber-sub">THREAT INTELLIGENCE &nbsp;◈&nbsp; ABUSEIPDB &nbsp;◈&nbsp; AI-POWERED ANALYSIS</div>
""", unsafe_allow_html=True)
st.divider()


# ─────────────────────────────────────────
#  📁 SIDEBAR
# ─────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ Scan Settings")
    max_age  = st.slider("Max Age (days)", 30, 180, 90, 10)
    delay    = st.slider("Request Delay (sec)", 1, 5, 2)
    ai_top_n = st.slider("AI Analysis — Top N Threats", 1, 5, 3)
    st.divider()
    st.markdown("### 🔑 Legend")
    st.markdown("🔴 **Malicious** — score > 75")
    st.markdown("🟡 **Suspicious** — score > 30")
    st.markdown("🟢 **Safe** — score ≤ 30")



# ─────────────────────────────────────────
#  📤 FILE UPLOAD
# ─────────────────────────────────────────
uploaded_file = st.file_uploader(
    "📂 Upload IP list (.txt — one IP per line)",
    type=["txt"],
    help="Plain text file with one IP address per line.",
)

if uploaded_file:
    raw_ips = uploaded_file.read().decode("utf-8").splitlines()

    # ── Fix 2: Input validation — strip comments, blank lines, invalid IPs ──
    def is_valid_ip(ip: str) -> bool:
        ip = ip.strip()
        if not ip or ip.startswith("#"):
            return False
        try:
            ipaddress.ip_address(ip)
            return True
        except ValueError:
            return False

    clean_ips  = [ip.strip() for ip in raw_ips if is_valid_ip(ip.strip())]
    bad_lines  = [ip.strip() for ip in raw_ips if ip.strip() and not is_valid_ip(ip.strip())]
    all_ips    = clean_ips
    public_ips = [ip for ip in all_ips if not is_private_ip(ip)]
    skipped    = len(all_ips) - len(public_ips)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📌 Total IPs",         len(raw_ips))
    col2.metric("🌐 Public IPs",        len(public_ips))
    col3.metric("🔒 Private / Skipped", skipped)
    col4.metric("❌ Invalid Lines",      len(bad_lines))

    if bad_lines:
        with st.expander(f"⚠️ {len(bad_lines)} invalid / skipped line(s) in your file"):
            for b in bad_lines:
                st.markdown(f"`{b}` — not a valid IP address")

    # ── Fix 3: Guard against zero public IPs ──
    if len(public_ips) == 0:
        st.error("❌ No public IP addresses found in the uploaded file. "
                 "All IPs are either private (192.168.x.x, 10.x.x.x, 172.16–31.x.x) "
                 "or invalid. Please upload a file with at least one public IP.")
        st.stop()

    if st.button("🚀  START SCAN", use_container_width=True):
        results            = []
        progress           = st.progress(0, text="Initialising scan…")
        status_placeholder = st.empty()

        for i, ip in enumerate(public_ips):
            status_placeholder.markdown(
                f"<span style='color:#00ff88;'>"
                f"🔍 Scanning {ip} … ({i+1}/{len(public_ips)})</span>",
                unsafe_allow_html=True,
            )
            result = check_ip(ip, max_age)   # max_age from sidebar slider ✓
            results.append(result)
            progress.progress(
                (i + 1) / len(public_ips),
                text=f"Scanned {i+1} / {len(public_ips)}"
            )
            time.sleep(delay)

        status_placeholder.empty()
        df = pd.DataFrame(results)

        st.success("✅ Scan complete!")

        # ── Summary Metrics ───────────────────────────────────────────
        malicious  = df["Status"].str.contains("Malicious").sum()
        suspicious = df["Status"].str.contains("Suspicious").sum()
        safe       = df["Status"].str.contains("Safe").sum()

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("🔴 Malicious",  malicious)
        m2.metric("🟡 Suspicious", suspicious)
        m3.metric("🟢 Safe",       safe)
        m4.metric("📋 Total",      len(df))

        st.divider()

        # ── Colour-coded Table ────────────────────────────────────────
        st.subheader("📊 Scan Results")

        def highlight_row(row):
            color_map = {
                "🔴 Malicious":  "background: linear-gradient(90deg,#3a000088,#1a001088); color:#ff4444; font-weight:bold;",
                "🟡 Suspicious": "background: linear-gradient(90deg,#1a140088,#100a0088); color:#ffcc00; font-weight:bold;",
                "🟢 Safe":       "background: linear-gradient(90deg,#001a0d88,#00100a88); color:#00ff88;",
            }
            style = color_map.get(row["Status"], "")
            return [style] * len(row)

        styled_df = df.style.apply(highlight_row, axis=1)
        st.dataframe(styled_df, use_container_width=True, height=350)

        # ── Threat Score Visual Bars ──────────────────────────────────
        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("🎯 Threat Score Breakdown")

        for _, row in df.iterrows():
            score = row["Score"]
            if not isinstance(score, int):
                continue
            pct   = min(score, 100)
            if score > 75:
                bar_color = "linear-gradient(90deg, #ff0044, #ff4444)"
                badge_cls = "badge-malicious"
                badge_txt = "MALICIOUS"
            elif score > 30:
                bar_color = "linear-gradient(90deg, #ff8800, #ffcc00)"
                badge_cls = "badge-suspicious"
                badge_txt = "SUSPICIOUS"
            else:
                bar_color = "linear-gradient(90deg, #00ff88, #00cfff)"
                badge_cls = "badge-safe"
                badge_txt = "SAFE"

            st.markdown(f"""
<div style="display:flex; align-items:center; gap:12px; margin:6px 0; font-family:'Share Tech Mono',monospace;">
  <span style="min-width:140px; color:#aaa; font-size:12px;">{row['IP']}</span>
  <div style="flex:1; background:#111; border-radius:4px; height:14px; overflow:hidden; border:1px solid #ffffff11;">
    <div style="width:{pct}%; height:100%; background:{bar_color}; border-radius:4px;
                box-shadow:0 0 8px {'#ff444488' if score>75 else '#ffcc0066' if score>30 else '#00ff8866'};"></div>
  </div>
  <span style="min-width:36px; text-align:right; color:#fff; font-size:12px;">{score}</span>
  <span class="{badge_cls}" style="font-size:10px; padding:2px 10px;">{badge_txt}</span>
</div>
""", unsafe_allow_html=True)

        # ── Charts ───────────────────────────────────────────────────
        st.subheader("📈 Classification Summary")

        matplotlib.rcParams.update({
            "figure.facecolor": "#0d0d0d",
            "axes.facecolor":   "#111111",
            "axes.edgecolor":   "#00ff88",
            "axes.labelcolor":  "#00ff88",
            "xtick.color":      "#00ff88",
            "ytick.color":      "#00ff88",
            "text.color":       "#00ff88",
            "grid.color":       "#00ff8822",
        })

        # Fix 6: only draw charts when there is data to plot
        numeric_df = df[df["Score"].apply(lambda x: isinstance(x, int))]
        counts = numeric_df["Status"].value_counts()

        if counts.empty:
            st.warning("⚠️ No valid scores to chart — all IPs returned API errors.")
        else:
            bar_colors = [
                "#ff4444" if "Malicious"  in s else
                "#ffcc00" if "Suspicious" in s else
                "#00ff88"
                for s in counts.index
            ]
            pie_colors = bar_colors

            if len(counts) == 1:
                # Only one category — skip pie chart (looks odd), show bar only
                fig, ax1 = plt.subplots(1, 1, figsize=(6, 4))
                counts.plot(kind="bar", ax=ax1, color=bar_colors, edgecolor="#0d0d0d")
                ax1.set_title("IP Classification", fontsize=13)
                ax1.set_xlabel("Status")
                ax1.set_ylabel("Count")
                ax1.tick_params(axis="x", rotation=0)
                ax1.grid(axis="y", alpha=0.3)
            else:
                fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
                counts.plot(kind="bar", ax=ax1, color=bar_colors, edgecolor="#0d0d0d")
                ax1.set_title("IP Classification", fontsize=13)
                ax1.set_xlabel("Status")
                ax1.set_ylabel("Count")
                ax1.tick_params(axis="x", rotation=15)
                ax1.grid(axis="y", alpha=0.3)
                ax2.pie(
                    counts,
                    labels=counts.index,
                    colors=pie_colors,
                    autopct="%1.0f%%",
                    textprops={"color": "#00ff88"},
                    wedgeprops={"edgecolor": "#0d0d0d"},
                )
                ax2.set_title("Distribution", fontsize=13)

            plt.tight_layout()
            st.pyplot(fig)

        st.divider()

        # ── AI Analysis ───────────────────────────────────────────────
        st.subheader("🤖 AI-Based Threat Analysis")

        threats = df[df["Status"].str.contains("Malicious|Suspicious")].head(ai_top_n)

        if threats.empty:
            st.info("No significant threats detected. All IPs appear safe.")
        else:
            for _, row in threats.iterrows():
                color = status_color(row["Status"])
                with st.expander(
                    f"🔥 {row['IP']}  |  {row['Status']}  |  Score: {row['Score']}"
                ):
                    st.markdown(
                        f"<span style='color:{color}; font-weight:bold;'>"
                        f"Country: {row['Country']} &nbsp;|&nbsp; "
                        f"ISP: {row['ISP']} &nbsp;|&nbsp; "
                        f"Reports: {row['Reports']}</span>",
                        unsafe_allow_html=True,
                    )
                    with st.spinner("Generating AI analysis…"):
                        analysis = get_ai_mitigation(
                            row["IP"], row["Status"], row["Score"]
                        )
                    st.markdown(analysis)

        st.divider()

        # ── Quick Mitigations ─────────────────────────────────────────
        st.subheader("🛡️ Quick Mitigation Guide")

        action_needed = df[df["Status"].str.contains("Malicious|Suspicious")]

        if action_needed.empty:
            st.success("✅ No threats found — network appears clean.")
        else:
            for _, row in action_needed.iterrows():
                if "Malicious" in row["Status"]:
                    card_bg    = "linear-gradient(135deg, #1a0008, #0d0005)"
                    card_bord  = "#ff4444"
                    card_glow  = "#ff444433"
                    icon       = "🚨"
                else:
                    card_bg    = "linear-gradient(135deg, #1a1000, #0d0900)"
                    card_bord  = "#ffcc00"
                    card_glow  = "#ffcc0033"
                    icon       = "⚠️"

                st.markdown(f"""
<div style="background:{card_bg}; border:1px solid {card_bord};
            border-left:4px solid {card_bord}; border-radius:8px;
            padding:14px 18px; margin:10px 0;
            box-shadow:0 0 16px {card_glow}; font-family:'Share Tech Mono',monospace;">
  <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
    <span style="color:{card_bord}; font-size:14px; font-weight:bold; letter-spacing:1px;">
      {icon} &nbsp; {row['IP']}
    </span>
    <span style="font-size:11px; color:#888;">
      Score: <b style="color:{card_bord};">{row['Score']}</b> &nbsp;|&nbsp;
      Country: {row['Country']} &nbsp;|&nbsp;
      Reports: {row['Reports']}
    </span>
  </div>
  <hr style="border:none; height:1px; background:linear-gradient(90deg,{card_bord}44,transparent); margin:6px 0 10px;">
</div>
""", unsafe_allow_html=True)
                st.markdown(get_basic_mitigation(row["IP"], row["Status"], row["Score"]))

        st.divider()

        # ── CSV Download ──────────────────────────────────────────────
        st.subheader("💾 Export Report")
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download CSV Report",
            data=csv,
            file_name=f"ip_threat_report_{timestamp}.csv",
            mime="text/csv",
            use_container_width=True,
        )
