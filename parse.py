from urllib.parse import urlparse
import re
def extract_ids(url):
    parsed_url = urlparse(url)
    path_segments = parsed_url.path.split('/')
    
    tournament_slug = None
    set_id = None
    
    for i, segment in enumerate(path_segments):
        if segment == 'tournament':
            if i + 1 < len(path_segments):
                tournament_slug = path_segments[i + 1]
        if segment == 'set':
            if i + 1 < len(path_segments):
                set_id = path_segments[i + 1]
    
    return tournament_slug, set_id
def validate_url(url):
    """
    Validate the given URL to ensure it is properly formed and contains the required path segments.

    Parameters:
    url (str): The URL to validate.

    Returns:
    bool: True if the URL is valid, False otherwise.
    """
    # Basic URL validation using a regex pattern
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  # ...or ipv4
        r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  # ...or ipv6
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    if re.match(regex, url) is None:
        #print("Usage: Enter the url from a start.gg Overwatch match.\nExample: https://www.start.gg/tournament/overwatch-collegiate-championship-spring-2024/events/overwatch-collegiate-championship-spring-2024/set/74300192 \n")
        return False

    # Check for required path segments
    parsed_url = urlparse(url)
    path_segments = parsed_url.path.split('/')
    if 'tournament' not in path_segments or 'set' not in path_segments:
        return False

    return True