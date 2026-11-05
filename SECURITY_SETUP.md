# Security setup
Only HTTPS hh.ru and its subdomains, port 443, are accepted. All resolved addresses must be public. The connection uses the checked IP and verifies the original hostname's TLS certificate. Redirects and compressed responses are rejected. HTML is limited to 2 MiB, socket operations to 5 seconds and the download loop to 20 seconds (DNS lookup depends on the operating system resolver).
If HH redirects, paste the final allowed URL. Arbitrary sources are intentionally no longer accepted.
Before deployment, require user authentication at the hosting layer and configure provider spending limits. Resume contents are sent to the AI provider; obtain the necessary permission and minimize personal information.
