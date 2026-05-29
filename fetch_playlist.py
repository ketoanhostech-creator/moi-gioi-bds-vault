"""
fetch_playlist.py - Lay danh sach video tu YouTube playlist qua API v3

Cach su dung:
    python fetch_playlist.py --playlist-id <PLAYLIST_ID> --output videos.json
    python fetch_playlist.py --playlist-id <PLAYLIST_ID> --output videos.json --api-key YOUR_API_KEY

Khuy nen: Dat API_KEY trong bien moi truong hoac file .env
    YOUTUBE_API_KEY=your_api_key_here

Yeu cau:
    pip install google-api-python-client requests python-dotenv

Ket qua (output JSON):
    [
        {"id": "v001", "title": "Tieu de video", "url": "https://youtube.com/..."},
        ...
    ]
"""

import argparse
import json
import sys
from pathlib import Path

try:
    from googleapiclient.discovery import build
    HAS_API_CLIENT = True
except ImportError:
    HAS_API_CLIENT = False

try:
    from dotenv import load_dotenv
    import os
    HAS_DOTENV = True
except ImportError:
    HAS_DOTENV = False


# ========== NGUON API KEY ==========
def get_api_key(provided_key: str | None = None) -> str:
    """
    Lay API key theo thu tu uu tien:
    1. Tham so --api-key
    2. Bien moi truong YOUTUBE_API_KEY
    3. File .env (neu co)
    """
    if provided_key:
        return provided_key.strip()

    if HAS_DOTENV:
        load_dotenv()

    key = os.environ.get("YOUTUBE_API_KEY", "").strip()
    if key:
        return key

    raise ValueError(
        "Khong tim thay API key. "
        "Vui long dat bien moi truong YOUTUBE_API_KEY "
        "hoac truyen --api-key <KEY>"
    )

# ========== HAM FETCH PLAYLIST ==========
def fetch_playlist_videos(playlist_id: str, api_key: str, max_results: int = 500) -> list[dict]:
    """
    Lay danh sach video tu YouTube playlist.
    Dung pagination de lay du so luong video (max 500).

    Args:
        playlist_id: ID cua YouTube playlist (VD: PLxxxx...)
        api_key: YouTube Data API v3 key
        max_results: So video toi da lay ve (toi da 500)

    Returns:
        Danh sach dict: [{"id": "...", "title": "...", "url": "..."}, ...]
    """
    if not HAS_API_CLIENT:
        raise ImportError(
            "Yeu cau google-api-python-client. "
            "Vui long chay: pip install google-api-python-client"
        )

    youtube = build("youtube", "v3", developerKey=api_key)
    videos = []
    page_token = None
    count = 0

    print(f"[INFO] Bat dau lay video tu playlist: {playlist_id}")

    while count < max_results:
        params = {
            "part": "snippet",
            "playlistId": playlist_id,
            "maxResults": min(50, max_results - count),
        }
        if page_token:
            params["pageToken"] = page_token

        try:
            response = youtube.playlistItems().list(**params).execute()
        except Exception as e:
            print(f"[ERROR] Loi khi goi API: {e}")
            break

        items = response.get("items", [])
        for item in items:
            snippet = item.get("snippet", {})
            vid_id = snippet.get("resourceId", {}).get("videoId", "")
            title = snippet.get("title", "Khong co tieu de")

            if vid_id:
                videos.append({
                    "id": vid_id,
                    "title": title,
                    "url": f"https://www.youtube.com/watch?v={vid_id}",
                })
                count += 1

        page_token = response.get("nextPageToken")
        if not page_token or count >= max_results:
            break

        print(f"  [PROGRESS] Da lay {count} video, tiep tuc...")

    print(f"[INFO] Da lay {len(videos)} video tu playlist.")
    return videos

def save_to_json(videos: list[dict], output_path: str) -> None:
    """
    Luu danh sach video ra file JSON.
    """
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(videos, f, ensure_ascii=False, indent=2)
    print(f"[INFO] Da luu {len(videos)} video vao {out}")


def demo_mode(playlist_id: str, output_path: str, max_results: int = 15) -> None:
    """
    Che do demo: tao du lieu mau khi khong co API key.
    Sinh ra video mau voi playlist_id da cho.
    """
    print("[WARN] Khong co API key - su dung che do DEMO.")
    print(f"[INFO] Sinh {max_results} video mau tu playlist {playlist_id}")

    mau_videos = []
    mau_titles = [
        "Cach tim khach hang BDS online tren Facebook va Zalo hieu qua",
        "Kich ban telesale goi dien moi gap khach hang BDS",
        "Quy trinh phap ly khi mua ban bat dong san can biet",
        "Cach cham khach hang sau khi ban de gioi thieu them",
        "Bi kip tim nguon hang BDS gia tot tu chu dau tu",
        "Phuong phap tham dinh gia bat dong san thuc te",
        "Cach xay dung moi quan voi doi tac chu dau tu",
        "Quy trinh ban hang BDS tu A-Z cho moi gioi moi",
        "Ren luyen tu duy va ky nang giao tiep trong BDS",
        "Cap nhat xu huong thi truong bat dong san 2025",
        "Cong cu CRM quan ly khach hang hieu qua cho moi gioi",
        "Case study thuc te chot sale can ho cao cap",
        "Marketing content thu hut khach hang tren mang xa hoi",
        "Ky thuat chot sale closing trong dam phan BDS",
        "Tim hieu ve giay to phap ly sang ten so do",
    ]

    for i, title in enumerate(mau_titles[:max_results], 1):
        vid_id = f"demo_{playlist_id}_{i:03d}"
        mau_videos.append({
            "id": vid_id,
            "title": title,
            "url": f"https://www.youtube.com/watch?v={vid_id}",
        })

    save_to_json(mau_videos, output_path)
    print("[INFO] Che do DEMO hoan tat. File mau da duoc tao.")

def main():
    """
    Ham chinh: Xu ly doi so, goi API, luu file.
    """
    parser = argparse.ArgumentParser(
        description="Lay danh sach video tu YouTube playlist",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Vi du su dung:
  python fetch_playlist.py --playlist-id PLxxxxxxxxxxx --output videos.json
  python fetch_playlist.py --playlist-id PLxxxxxxxxxxx --output videos.json --api-key ABC123
  python fetch_playlist.py --playlist-id PLxxxxxxxxxxx --output videos.json --max 100

Sau khi co videos.json, chay tiep:
  python classify.py --input videos.json --output classification.json --stats
  python gen_vault.py --input classification.json --output vault
        """
    )
    parser.add_argument(
        "--playlist-id", "-p",
        required=True,
        help="ID cua YouTube playlist (bat dau bang PL...)"
    )
    parser.add_argument(
        "--output", "-o",
        default="videos.json",
        help="Ten file JSON dau ra (mac dinh: videos.json)"
    )
    parser.add_argument(
        "--api-key", "-k",
        default=None,
        help="YouTube Data API v3 key (hoac dat YOUTUBE_API_KEY trong .env)"
    )
    parser.add_argument(
        "--max", "-m",
        type=int,
        default=500,
        help="So video toi da lay ve (toi da 500, mac dinh: 500)"
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Che do demo (khong dung API, sinh du lieu mau)"
    )

    args = parser.parse_args()

    print("=" * 50)
    print("FETCH PLAYLIST - Moi Gioi BDS Vault")
    print("=" * 50)

    # Che do demo: khong can API key
    if args.demo:
        demo_mode(args.playlist_id, args.output, args.max)
        return

    # Lay API key
    try:
        api_key = get_api_key(args.api_key)
        print(f"[INFO] Da tim thay API key.")
    except ValueError as e:
        print(f"[ERROR] {e}")
        print("Co the chay che do demo voi: python fetch_playlist.py -p <ID> -o videos.json --demo")
        sys.exit(1)

    # Fetch video tu playlist
    try:
        videos = fetch_playlist_videos(
            playlist_id=args.playlist_id,
            api_key=api_key,
            max_results=args.max,
        )
    except ImportError as e:
        print(f"[ERROR] {e}")
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] Loi khong xac dinh: {e}")
        sys.exit(1)

    if not videos:
        print("[WARN] Khong tim thay video nao trong playlist.")
        sys.exit(0)

    # Luu ra file
    save_to_json(videos, args.output)

    print("=" * 50)
    print("HOAN TAT! Buoc tiep theo:")
    print(f"  1. Phan loai: python classify.py --input {args.output} --output classification.json --stats")
    print(f"  2. Generate:  python gen_vault.py --input classification.json --output vault")
    print("=" * 50)


if __name__ == "__main__":
    main()
