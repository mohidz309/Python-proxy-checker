import requests
import concurrent.futures
import threading
from urllib.parse import urlparse

# =========================
# Configuration
# =========================
INPUT_FILE = "proxies.txt"          # Input file containing proxies
TIMEOUT = 8                         # Timeout per proxy in seconds
MAX_WORKERS = 50                    # Number of concurrent threads
TEST_URL = "http://httpbin.org/ip"  # URL used to test proxies

# =========================
# Shared data
# =========================
lock = threading.Lock()

working_proxies = {
    "http": [],
    "socks4": [],
    "socks5": []
}

progress = {
    "total": 0,
    "done": 0
}

# =========================
# Helper: Normalize proxy
# =========================
def normalize_proxy(line: str):
    """
    Convert each proxy line into a standard format.
    Returns: (proxy_type, proxy_url) or None

    Supported formats:
    - ip:port
    - ip:port:user:pass
    - http://ip:port
    - http://user:pass@ip:port
    - socks4://ip:port
    - socks5://ip:port
    - socks5://user:pass@ip:port
    """
    line = line.strip()
    if not line or line.startswith("#"):
        return None

    if "://" not in line:
        parts = line.split(":")
        if len(parts) == 2:
            # Default to HTTP if no type is specified
            return ("http", f"http://{line}")
        elif len(parts) == 4:
            ip, port, user, password = parts
            return ("http", f"http://{user}:{password}@{ip}:{port}")
        else:
            return None

    parsed = urlparse(line)
    scheme = parsed.scheme.lower()

    if scheme in ("http", "https"):
        return ("http", line)
    elif scheme == "socks4":
        return ("socks4", line)
    elif scheme == "socks5":
        return ("socks5", line)

    return None

# =========================
# Helper: Show progress
# =========================
def print_progress():
    with lock:
        done = progress["done"]
        total = progress["total"]
        percent = (done / total) * 100 if total else 0
        print(f"\rProgress: {done}/{total} ({percent:.2f}%)", end="", flush=True)

# =========================
# Check one proxy
# =========================
def check_proxy(proxy_type: str, proxy_url: str):
    proxies = {
        "http": proxy_url,
        "https": proxy_url
    }

    is_working = False

    try:
        response = requests.get(TEST_URL, proxies=proxies, timeout=TIMEOUT)
        if response.status_code == 200:
            is_working = True
            with lock:
                working_proxies[proxy_type].append(proxy_url)
    except Exception:
        pass

    with lock:
        progress["done"] += 1

    print_progress()
    return is_working

# =========================
# Save working proxies
# =========================
def save_results():
    output_files = {
        "http": "http_https.txt",
        "socks4": "socks4.txt",
        "socks5": "socks5.txt"
    }

    for proxy_type, filename in output_files.items():
        with open(filename, "w", encoding="utf-8") as f:
            for proxy in working_proxies[proxy_type]:
                f.write(proxy + "\n")

# =========================
# Main function
# =========================
def main():
    try:
        with open(INPUT_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Input file not found: {INPUT_FILE}")
        return

    proxies = []
    for line in lines:
        item = normalize_proxy(line)
        if item:
            proxies.append(item)

    if not proxies:
        print("No valid proxies found in the input file.")
        return

    progress["total"] = len(proxies)

    print(f"Loaded {len(proxies)} proxies from {INPUT_FILE}")
    print("Checking proxies...")

    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [
            executor.submit(check_proxy, proxy_type, proxy_url)
            for proxy_type, proxy_url in proxies
        ]
        concurrent.futures.wait(futures)

    print()  # New line after progress bar
    save_results()

    print("Done.")
    print(f"Working HTTP/HTTPS proxies: {len(working_proxies['http'])}")
    print(f"Working SOCKS4 proxies: {len(working_proxies['socks4'])}")
    print(f"Working SOCKS5 proxies: {len(working_proxies['socks5'])}")
    print("Results saved to:")
    print("- http_https.txt")
    print("- socks4.txt")
    print("- socks5.txt")

if __name__ == "__main__":
    main()
