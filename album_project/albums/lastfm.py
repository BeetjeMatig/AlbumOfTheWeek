import pylast
from django.conf import settings


def get_lastfm_network():
    return pylast.LastFMNetwork(
        api_key=settings.LASTFM_API_KEY,
        api_secret=settings.LASTFM_SHARED_SECRET
    )

def search_albums(query, limit=5):
    network = get_lastfm_network()
    results = network.search_for_album(query).get_next_page()
    return results[:limit]  # limit to top 5 results


def get_top_tag(artist, album):
    network = get_lastfm_network()
    try:
        album_obj = network.get_album(artist, album)
        tags = album_obj.get_top_tags()
        return tags[0].item.name if tags else "Unknown"
    except Exception:
        return "Unknown"
    
def get_album_info(artist_name, album_title):
    network = get_lastfm_network()
    album_obj = network.get_album(artist_name, album_title)

    try:
        tags = album_obj.get_top_tags()
        top_tag = tags[0].item.name if tags else "Unknown"
    except Exception:
        top_tag = "Unknown"

    return {
        "title": album_obj.get_title(),
        "artist": album_obj.get_artist().get_name(),
        "url": album_obj.get_url(),
        "image": album_obj.get_cover_image(),
        "genre": top_tag,
        "release_year": "Unknown",  # Last.fm often lacks release date — we'll handle this
        "mbid": album_obj.get_mbid(),
    }

