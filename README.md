# Proxy Checker

A simple and fast Python script that reads proxies from a text file, checks whether they work, shows a live progress percentage, and saves working proxies into separate output files by type.

## Features

- Reads proxies from `proxies.txt`
- Supports HTTP/HTTPS, SOCKS4, and SOCKS5
- Supports proxies with or without authentication
- Shows live progress while checking
- Saves working proxies into separate text files
- Uses multithreading for faster checking

## Supported Input Formats

```text
ip:port
ip:port:user:pass
http://ip:port
http://user:pass@ip:port
socks4://ip:port
socks5://ip:port
socks5://user:pass@ip:port
```

## Project Structure

```text
proxy-checker/
├── proxy_checker.py
├── proxies.txt
├── requirements.txt
├── .gitignore
├── LICENSE
└── README.md
```

## Installation

```bash
pip install -r requirements.txt
```

## Usage

1. Put your proxies in `proxies.txt`
2. Run the script:

```bash
python proxy_checker.py
```

## Output Files

After checking, the script creates:

- `http_https.txt`
- `socks4.txt`
- `socks5.txt`

## Example `proxies.txt`

```text
192.168.1.10:8080
192.168.1.20:8080:user:pass
http://192.168.1.30:3128
http://user:pass@192.168.1.31:8080
socks4://192.168.1.40:1080
socks5://192.168.1.50:1080
socks5://user:pass@192.168.1.60:1080
```

## Notes

- Proxies without a scheme are treated as HTTP by default.
- Some proxies may work for one site and fail for another depending on restrictions.
- You can change `TEST_URL`, `TIMEOUT`, and `MAX_WORKERS` in the script if needed.

## GitHub Description

**Fast Python proxy checker with file input, live progress, and separate output files for HTTP/HTTPS, SOCKS4, and SOCKS5.**

## License

This project is licensed under the MIT License.
