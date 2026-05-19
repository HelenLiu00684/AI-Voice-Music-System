# ai_query.py

import yt_dlp


# ============================================
# BAD VIDEO WORDS
# ============================================

BAD_WORDS = [

    "highlight",

    "reaction",

    "interview",

    "trailer",

    "gameplay",

    "live stream",

    "stream",

    "tutorial",

    "news",

    "analysis",

    "press conference",

    "match",

    "vs",

    "full movie"
]


# ============================================
# GOOD MUSIC WORDS
# ============================================

GOOD_WORDS = [

    "audio",

    "lyrics",

    "lyric",

    "music",

    "song",

    "topic"
]


# ============================================
# SEARCH
# ============================================

def search(query):

    ydl_opts = {

        # IMPORTANT
        # search more results

        "default_search": "ytsearch10",

        "quiet": True,

        "skip_download": True,

        "noplaylist": True
    }

    results = []

    try:

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:

            info = ydl.extract_info(query, download=False)

            if not info:
                return []

            entries = info.get("entries", [])

            # ====================================
            # FILTER RESULTS
            # ====================================

            for entry in entries:

                title = entry.get("title", "")

                url = entry.get("url", "")

                lower_title = title.lower()

                # ====================================
                # SKIP BAD RESULTS
                # ====================================

                skip = False

                for bad in BAD_WORDS:

                    if bad in lower_title:

                        skip = True

                        break

                if skip:
                    continue

                # ====================================
                # MUSIC SCORE
                # ====================================

                score = 0

                for good in GOOD_WORDS:

                    if good in lower_title:

                        score += 1

                # ====================================
                # save
                # ====================================

                results.append({

                    "url": url,

                    "title": title,

                    "score": score
                })

            # ====================================
            # SORT BY SCORE
            # ====================================

            results.sort(

                key=lambda x: x["score"],

                reverse=True
            )

            # ====================================
            # FINAL RESULTS
            # ====================================

            final_results = []

            for r in results:

                final_results.append(

                    (r["url"], r["title"])
                )

            return final_results

    except Exception as e:

        print("\nYouTube search failed")
        print(e)

        return []