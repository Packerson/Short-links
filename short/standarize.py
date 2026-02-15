def standarize_short_url(short_url):
    """
    Standarize short url
    """

    if not isinstance(short_url, str):
        return short_url

    return short_url.strip()
