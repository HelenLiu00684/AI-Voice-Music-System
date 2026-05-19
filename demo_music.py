import yt_dlp
import mpv
import time
SAD_PLAYLIST = [
    "Adele Someone Like You",
    "Billie Eilish Happier Than Ever",
    "Taylor Swift All Too Well"
]

def search_youtube(song):
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'noplaylist': True,
        'default_search': 'ytsearch1'
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(song, download=False)

        url = info['entries'][0]['url']
        title = info['entries'][0]['title']

    return url, title


def play(song):

    print("Searching:", song)

    url, title = search_youtube(song)

    print("Now Playing:", title)

    player = mpv.MPV(
        input_default_bindings=True,
        input_vo_keyboard=True,
        cache=True,
        cache_secs=20
    )

    player.play(url)

    time.sleep(30)  # 播放30秒再播放下一首
    while True:
        time.sleep(1)


if __name__ == "__main__":

    song = input("Enter song or mood: ")

    if song.lower() == "sad":
        for s in SAD_PLAYLIST:
            play(s)
    else:
        play(song)