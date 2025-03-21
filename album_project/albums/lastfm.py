import re
from xml.dom.minidom import parseString

import pylast
from django.conf import settings


def get_lastfm_network():
    """Initializes and returns the Last.fm network object."""
    return pylast.LastFMNetwork(
        api_key=settings.LASTFM_API_KEY,
        api_secret=settings.LASTFM_SHARED_SECRET
    )

def search_albums(query, limit=5):
    """Searches for albums on Last.fm and returns the top 'limit' results."""
    network = get_lastfm_network()
    try:
        results = network.search_for_album(query).get_next_page()
        return results[:limit]  # Limit to top 5 results
    except Exception as e:
        print(f"⚠ Last.fm API Error (search_albums): {e}")
        return []

def get_album_info(artist_name, album_title):
    """Fetches album details from Last.fm, including genre, release year, and cover image."""
    network = get_lastfm_network()

    try:
        album_obj = network.get_album(artist_name, album_title)
    except Exception as e:
        print(f"⚠ Last.fm API Error (get_album_info): {e}")
        return None

    # 🏷 Extract Genre (Top Tag)
    try:
        tags = album_obj.get_top_tags()
        genre = tags[0].item.name if tags else "Unknown"
    except Exception:
        genre = "Unknown"

    # 📅 Extract Release Year
    try:
        release_date_raw = album_obj._request("album.getInfo", True)
        release_date = extract_release_year(release_date_raw.toxml())  # Uses XML parsing
    except Exception as e:
        print(f"⚠ Error fetching release date: {e}")
        release_date = "Unknown"

    return {
        "title": album_obj.get_title(),
        "artist": album_obj.get_artist().get_name(),
        "url": album_obj.get_url(),
        "image": album_obj.get_cover_image(),
        "genre": genre,
        "release_year": release_date,  # 🎯 Now properly extracted
        "mbid": album_obj.get_mbid(),
    }

def extract_release_year(xml_response):
    """
    Extracts the release year from Last.fm's album.getInfo XML response.
    Falls back to "Unknown" if missing.
    """
    try:
        doc = parseString(xml_response)
        release_date_node = doc.getElementsByTagName("releasedate")
        
        if release_date_node and release_date_node[0].firstChild:
            release_date = release_date_node[0].firstChild.nodeValue.strip()
            match = re.search(r"\b(\d{4})\b", release_date)
            return match.group(1) if match else "Unknown"
    except Exception as e:
        print(f"⚠ XML Parsing Error: {e}")
    
    return "Unknown"
