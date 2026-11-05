import socket
import unittest
from unittest.mock import patch
from safe_fetch import validate_url

class SecurityTests(unittest.TestCase):
    def test_rejected_urls(self):
        for url in ["http://hh.ru", "https://localhost", "https://hh.ru.evil.com", "https://hh.ru@evil.com", "https://hh.ru:8443", "https://127.0.0.1", "https://hh.ru/\n"]:
            with self.subTest(url=url), self.assertRaises(ValueError):
                validate_url(url)
    def test_private_dns(self):
        for ip in ["127.0.0.1", "169.254.169.254", "10.0.0.1", "::1"]:
            with patch("safe_fetch.socket.getaddrinfo", return_value=[(socket.AF_INET, socket.SOCK_STREAM, 6, "", (ip, 443))]):
                with self.assertRaises(ValueError):
                    validate_url("https://hh.ru/resume/1")
    def test_public_dns(self):
        with patch("safe_fetch.socket.getaddrinfo", return_value=[(socket.AF_INET, socket.SOCK_STREAM, 6, "", ("8.8.8.8", 443))]):
            self.assertEqual(validate_url("https://spb.hh.ru/vacancy/1")[0].hostname, "spb.hh.ru")
