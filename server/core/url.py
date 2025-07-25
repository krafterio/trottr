from urllib.parse import urlparse


def extract_domain(url: str | None) -> str | None:
    """
    Extract the domain from an URL.
    """
    if not url:
        return None

    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url

    parsed_url = urlparse(url)
    domain = parsed_url.netloc

    return domain if domain else None
