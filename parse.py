from urllib.parse import urlparse
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
