import ipaddress
import socket
from urllib.parse import urlparse

class InvalidTarget(ValueError):
    pass

def validate_target_url(value):
    if not isinstance(value, str) or len(value) > 2048:
        raise InvalidTarget("target_url must be a valid URL")
    parsed = urlparse(value)
    if parsed.scheme not in ("http", "https") or not parsed.hostname:
        raise InvalidTarget("only http and https URLs are allowed")
    if parsed.username or parsed.password:
        raise InvalidTarget("URL credentials are not allowed")
    host = parsed.hostname.rstrip(".")
    try:
        addresses = {item[4][0] for item in socket.getaddrinfo(host, parsed.port or 443, type=socket.SOCK_STREAM)}
    except (socket.gaierror, ValueError):
        raise InvalidTarget("target host cannot be resolved")
    for address in addresses:
        ip = ipaddress.ip_address(address)
        if any((ip.is_private, ip.is_loopback, ip.is_link_local, ip.is_multicast, ip.is_reserved, ip.is_unspecified)):
            raise InvalidTarget("private or reserved target addresses are not allowed")
    return value
