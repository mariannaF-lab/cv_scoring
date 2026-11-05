import http.client
import ipaddress
import socket
import ssl
import time
from urllib.parse import urlsplit
from types import SimpleNamespace

MAX_BYTES = 2 * 1024 * 1024

def validate_url(url):
    if len(url) > 2048 or any(ord(c) < 33 or ord(c) > 126 for c in url):
        raise ValueError("Invalid URL")
    p = urlsplit(url)
    host = p.hostname or ""
    if (p.scheme != "https" or p.username is not None or p.password is not None
            or p.port not in (None, 443) or p.fragment
            or not (host == "hh.ru" or host.endswith(".hh.ru"))):
        raise ValueError("Only HTTPS hh.ru URLs are allowed")
    addresses = socket.getaddrinfo(host, 443, type=socket.SOCK_STREAM)
    if not addresses or any(not ipaddress.ip_address(a[4][0]).is_global for a in addresses):
        raise ValueError("Non-public address")
    return p, addresses[0]

def get_html(url):
    p, address = validate_url(url)
    deadline = time.monotonic() + 20
    family, kind, proto, _, sockaddr = address
    raw = socket.socket(family, kind, proto)
    conn = http.client.HTTPSConnection(p.hostname, timeout=5)
    try:
        raw.settimeout(5)
        raw.connect(sockaddr)
        # Connect to the checked IP, retaining TLS hostname verification.
        conn.sock = ssl.create_default_context().wrap_socket(raw, server_hostname=p.hostname)
        target = p.path or "/"
        if p.query:
            target += "?" + p.query
        conn.request("GET", target, headers={"User-Agent": "CVScoring/1.0", "Accept-Encoding": "identity"})
        response = conn.getresponse()
        if response.status != 200:
            raise ValueError("Page unavailable; redirects are not followed")
        if response.getheader("Content-Encoding", "identity").lower() != "identity":
            raise ValueError("Compressed responses are not accepted")
        if response.getheader("Content-Type", "").split(";")[0].lower() not in ("text/html", "application/xhtml+xml"):
            raise ValueError("Expected HTML")
        chunks, size = [], 0
        while True:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise TimeoutError("Download deadline exceeded")
            conn.sock.settimeout(min(5, remaining)) if conn.sock else None
            chunk = response.read1(min(65536, MAX_BYTES + 1 - size))
            if not chunk:
                break
            size += len(chunk)
            if size > MAX_BYTES:
                raise ValueError("Page too large")
            chunks.append(chunk)
        return SimpleNamespace(text=b"".join(chunks).decode("utf-8", errors="replace"))
    finally:
        conn.close()
        raw.close()
