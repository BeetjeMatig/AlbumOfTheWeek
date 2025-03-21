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
