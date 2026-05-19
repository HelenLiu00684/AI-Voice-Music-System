# ai_query.py

import yt_dlp


# ============================================
# YOUTUBE SEARCH LAYER
# ============================================
#
# This module performs YouTube music search
# using yt-dlp.
#
# IMPORTANT:
# This module only performs:
#
# - search
# - metadata extraction
# - result ranking
#
# It does NOT:
#
# - download audio
# - play music
# - perform AI analysis
#
# ============================================

def search(query):

    """
    Search YouTube using a semantic query.

    Returns:
        List of:
            [(url, title), ...]
    """

    print("\nSearching YouTube...")

    # ====================================
    # YT-DLP SEARCH CONFIGURATION
    # ====================================

    ydl_opts = {

        # search top 10 candidates
        "default_search": "ytsearch10",

        # suppress console spam
        "quiet": True,

        # metadata only
        "skip_download": True,

        # avoid full playlist extraction
        "noplaylist": True
    }

    try:

        # ====================================
        # SEARCH YOUTUBE
        # ====================================

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:

            info = ydl.extract_info(

                query,

                download=False
            )

        # ====================================
        # EXTRACT SEARCH RESULTS
        # ====================================

        entries = info.get("entries", [])

        results = []

        for entry in entries:

            if not entry:

                continue

            title = entry.get("title")

            url = entry.get("webpage_url")

            # skip invalid results
            if not title or not url:

                continue

            results.append(

                (url, title)
            )

        print(f"\nFound {len(results)} results")

        return results

    except Exception as e:

        print("\nYouTube search failed")

        print(e)

        return []