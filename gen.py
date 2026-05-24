#!/usr/bin/env python3
"""
gen.py - Script tao Vault markdown tu YouTube playlist Moi Gioi BDS
Cach su dung:
    python3 gen.py
Yeu cau:
    pip install -r requirements.txt
"""

import os
import json
import shutil
from pathlib import Path
from datetime import datetime

# ============================================
# IMPORT DOTENV (de load bien moi truong)
# ============================================
try:
    from dotenv import load_dotenv
    HAS_DOTENV = True
except ImportError:
    HAS_DOTENV = False

try:
    from googleapiclient.discovery import build
    import requests
    HAS_API = True
except ImportError:
    HAS_API = False

# ============================================
# CAU HINH - Chinh sua phan nay
# ============================================
# Lay tu bien moi truong (cong voi gia tri mac dinh)
PLAYLIST_ID = os.getenv("PLAYLIST_ID", "PUT_YOUR_PLAYLIST_ID_HERE")
API_KEY = os.getenv("API_KEY", "PUT_YOUR_API_KEY_HERE")
VAULT_NAME = os.getenv("VAULT_NAME", "Moi_Gioi_BDS_Vault")

# ============================================
# 3 NHOM NOI DUNG
# ============================================
GROUPS = {
    "00_Co_Ban": {
        "name": "Co Ban - Bat dau tu con so 0",
        "description": "Cac bai co ban ve moi gioi bat dong san",
        "video_ids": []
    },
    "01_Chuyen_Sau": {
        "name": "Chuyen Sau - Ky nang nang cao",
        "description": "Cac ky nang chuyen sau trong moi gioi BDS",
        "video_ids": []
    },
    "02_Thuc_Chien": {
        "name": "Thuc Chien - Case study va kinh nghiem",
        "description": "Cac truong hop thuc te va bai hoc kinh nghiem",
        "video_ids": []
    }
}

# ============================================
# DEMO DATA
# ============================================
DEMO_VIDEOS = [
    {
        "id": "demo_001",
        "title": "Chao mung den voi khoa hoc Moi Gioi BDS",
        "description": "Gioi thieu tong quan ve khoa hoc, muc tieu va lo trinh hoc tap.",
        "thumbnail": "https://i.ytimg.com/vi/demo_001/maxresdefault.jpg"
    },
    {
        "id": "demo_002",
        "title": "Mo hinh kinh doanh moi gioi BDS",
        "description": "Hieu ve cac mo hinh: agent, broker, consultant va cach luong chon.",
        "thumbnail": "https://i.ytimg.com/vi/demo_002/maxresdefault.jpg"
    },
    {
        "id": "demo_003",
        "title": "Ky nang tu van khach hang chuyen nghiep",
        "description": "Cac ky nang giao tiep, lang nghe va tu van cho khach hang.",
        "thumbnail": "https://i.ytimg.com/vi/demo_003/maxresdefault.jpg"
    },
    {
        "id": "demo_004",
        "title": "Phap ly BDS nhung dieu co ban nhat",
        "description": "Tim hieu ve giay to, hop dong va cac van de phap ly co ban.",
        "thumbnail": "https://i.ytimg.com/vi/demo_004/maxresdefault.jpg"
    },
    {
        "id": "demo_005",
        "title": "Xay dung ke hoach kinh doanh ca nhan",
        "description": "Cach thiet lap muc tieu, ke hoach hanh dong va theo doi tien do.",
        "thumbnail": "https://i.ytimg.com/vi/demo_005/maxresdefault.jpg"
    }
]

# ============================================
# HAM XU LY
# ============================================
def slugify(text):
    """Chuyen text sang slug de lam ten file"""
    text = text.lower().strip()
    text = ''.join(c for c in text if c.isalnum() or c in ' -')
    text = text.replace(' ', '-')
    text = ''.join(c for c in text if c.isalnum() or c == '-')
    text = '-'.join(filter(None, text.split('-')))
    return text[:80]

def create_safe_filename(title):
    """Tao ten file an toan tu tieu de video"""
    return f"{slugify(title)}.md"

def to_wikilink(filename):
    """Tao Obsidian-style wiki link"""
    name = Path(filename).stem
    return f"[[{name}]]"

def fetch_playlist_videos(playlist_id, api_key):
    """Lay danh sach videos tu YouTube Data API"""
    if not api_key or api_key == "PUT_YOUR_API_KEY_HERE":
        print(">> Khong co API Key, dung demo data.")
        return DEMO_VIDEOS.copy()
    if not HAS_API:
        print(">> Chuong trinh chua cai dat thu vien. Dung demo data.")
        print(">> Cu: pip install -r requirements.txt")
        return DEMO_VIDEOS.copy()

    videos = []
    try:
        youtube = build("youtube", "v3", developerKey=api_key)
        page_token = None
        while True:
            response = youtube.playlistItems().list(
                part="snippet",
                playlistId=playlist_id,
                maxResults=50,
                pageToken=page_token
            ).execute()

            for item in response.get("items", []):
                snippet = item.get("snippet", {})
                resource_id = snippet.get("resourceId", {})
                video_id = resource_id.get("videoId", "")
                if video_id:
                    videos.append({
                        "id": video_id,
                        "title": snippet.get("title", "Khong co tieu de"),
                        "description": snippet.get("description", ""),
                        "thumbnail": f"https://i.ytimg.com/vi/{video_id}/maxresdefault.jpg"
                    })
            page_token = response.get("nextPageToken")
            if not page_token:
                break
        print(f">> Da lay {len(videos)} videos tu API.")
    except Exception as e:
        print(f">> Loi khi lay video: {e}")
        print(">> Dung demo data.")
        videos = DEMO_VIDEOS.copy()
    return videos

def generate_video_markdown(video, vault_path, all_files):
    """Tao file markdown cho mot video"""
    title = video["title"]
    video_id = video["id"]
    description = video.get("description", "")
    thumbnail = video.get("thumbnail", "")
    filename = create_safe_filename(title)
    filepath = vault_path / filename

    content_lines = [
        f"# {title}",
        "",
        "## Lien ket",
        f"- YouTube: https://www.youtube.com/watch?v={video_id}",
        "",
        "## Mo ta",
        description if description else "*Khong co mo ta.*",
        "",
        "## Tags",
        "#moi-gioi #bat-dong-san #youtube",
        "",
        "## Lien ket Noi bo (Obsidian)",
    ]

    for f in all_files:
        if f != filename:
            content_lines.append(f"- {to_wikilink(f)}")

    content_lines.extend([
        "",
        "## Quay lai Muc luc chinh",
        "- [[Muc_Luc_Co_Ban]]",
        "- [[Muc_Luc_Chuyen_Sau]]",
        "- [[Muc_Luc_Thuc_Chien]]",
        "",
        "---",
        f"*Auto-generated by gen.py | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*",
        "",
    ])

    content = "\n".join(content_lines)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    return filename

def assign_to_group(video_idx, total, groups_config):
    """Phan nhom video theo chi so"""
    group_keys = list(groups_config.keys())
    group_count = len(group_keys)
    if group_count == 0:
        return group_keys[0] if group_keys else ""
    group_idx = (video_idx * group_count) // total
    return group_keys[group_idx]

def create_group_toc(group_key, group_info, videos_in_group, vault_path):
    """Tao file Muc luc cho moi nhom"""
    group_name = group_info["name"]
    filename = f"Muc_Luc_{group_key.split('_')[1]}_{group_key.split('_')[2]}.md"
    filepath = vault_path / filename

    content_lines = [
        f"# {group_name}",
        "",
        f"*{group_info['description']}*",
        "",
        "## Danh sach Videos",
        "",
        "| STT | Ten Video | Lien ket YouTube | Noi bo |",
        "|-----|-----------|-----------------|--------|",
    ]

    for idx, video in enumerate(videos_in_group, 1):
        title = video["title"]
        video_id = video["id"]
        file_name = create_safe_filename(title)
        yt_link = f"https://www.youtube.com/watch?v={video_id}"
        content_lines.append(
            f"| {idx} | {title} | [Xem]({yt_link}) | {to_wikilink(file_name)} |"
        )

    content_lines.extend([
        "",
        "## Dieu huong den nhom khac",
        "- [[Muc_Luc_Co_Ban]]",
        "- [[Muc_Luc_Chuyen_Sau]]",
        "- [[Muc_Luc_Thuc_Chien]]",
        "",
        "## Quay lai Tong Muc Luc",
        "- [[Tong_Muc_Luc]]",
        "",
        "---",
        f"*Auto-generated by gen.py | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*",
        "",
    ])

    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(content_lines))
    return filename

def build_vault(playlist_id, api_key, vault_name, groups):
    """Ham chinh xay dung toan bo vault"""
    vault_path = Path(vault_name)
    if vault_path.exists():
        print(f">> Xoa thu muc cu: {vault_path}")
        shutil.rmtree(vault_path)
    vault_path.mkdir(parents=True)

    print(f">> Dang lay videos tu playlist: {playlist_id}")
    videos = fetch_playlist_videos(playlist_id, api_key)
    if not videos:
        print(">> Khong co video nao!")
        return
    print(f">> Tong cong: {len(videos)} videos")

    group_videos = {k: [] for k in groups.keys()}
    for idx, video in enumerate(videos):
        group_key = assign_to_group(idx, len(videos), groups)
        group_videos[group_key].append(video)

    all_files = []
    print(">> Dang tao file markdown cho cac videos...")
    for video in videos:
        filename = generate_video_markdown(video, vault_path, all_files)
        all_files.append(filename)
        print(f" - {filename}")

    group_toc_files = []
    print(">> Dang tao Muc luc cho cac nhom...")
    for group_key, group_info in groups.items():
        filename = create_group_toc(
            group_key,
            group_info,
            group_videos[group_key],
            vault_path
        )
        group_toc_files.append(filename)
        print(f" - {filename}")

    index_file = create_index_file(group_toc_files, group_videos, vault_path)
    print(f">> Dang tao Tong Muc Luc: {index_file}")

    metadata = {
        "vault_name": vault_name,
        "playlist_id": playlist_id,
        "total_videos": len(videos),
        "generated_at": datetime.now().isoformat(),
        "groups": {
            k: {
                "name": v["name"],
                "video_count": len(videos_list)
            } for k, videos_list in group_videos.items()
        },
        "files": all_files
    }
    with open(vault_path / "vault_metadata.json", "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)

    total_files = len(all_files) + len(group_toc_files) + 2
    print(f"\n===== HOAN THANH =====")
    print(f"Da tao {total_files} files trong thu muc: {vault_path}")
    print(f" - {len(all_files)} file video markdown")
    print(f" - {len(group_toc_files)} file Muc luc nhom")
    print(f" - 1 file Tong Muc Luc (index)")
    print(f" - 1 file metadata JSON")
    print(f"======================")

def create_index_file(group_toc_files, group_videos, vault_path):
    """Tao Tong Muc Luc chinh (file index)"""
    filename = "Tong_Muc_Luc.md"
    filepath = vault_path / filename
    content_lines = [
        "# Tong Muc Luc - Moi Gioi BDS",
        "",
        f"*Thu vien markdown cho playlist YouTube Moi Gioi BDS | {datetime.now().strftime('%Y-%m-%d')}*",
        "",
        "## Dieu huong nhanh",
        "",
    ]

    for group_key in groups.keys():
        toc_file = [f for f in group_toc_files if group_key.replace("_", " ").title().replace(" ", "_") in f or group_key.split("_")[1] in f or group_key.split("_")[2] in f][0]
        info = groups[group_key]
        count = len(group_videos.get(group_key, []))
        content_lines.append(f"- [[{toc_file.replace('.md', '')}]] - {info['name']} ({count} videos)")

    content_lines.extend([
        "",
        "## Tong quan",
        "Ban co the duyet qua toan bo noi dung theo 3 nhom chinh:",
    ])

    for group_key, info in groups.items():
        count = len(group_videos.get(group_key, []))
        content_lines.append(f"- **{info['name']}**: {info['description']} ({count} videos)")

    content_lines.extend([
        "",
        "## Cach su dung",
        "",
        "1. Mo file nay trong Obsidian (hoac bat ky Markdown editor nao)",
        "2. Click vao lien ket Noi bo [[ ]] de chuyen giua cac file",
        "3. Dung `Ctrl/Cmd + O` de timkiem nhanh ten file",
        "4. Xem video tren YouTube qua lien ket da duoc cung cap",
        "",
        "## Thong tin",
        "",
        f"- Tong so videos: {sum(len(v) for v in group_videos.values())}",
        f"- Tong so file: {sum(len(v) for v in group_videos.values())} videos + 3 Muc luc + 1 Tong Muc Luc + 1 Metadata",
        "",
        "---",
        f"*Auto-generated by gen.py | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*",
        "",
    ])

    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(content_lines))
    return filename

# ============================================
# CHAY CHUONG TRINH
# ============================================
if __name__ == "__main__":
    # Load bien moi truong tu file .env neu co
    if HAS_DOTENV:
        load_dotenv()
        print(">> Da load bien moi truong tu .env")

    print("===========================================")
    print(" MOI GIOI BDS VAULT GENERATOR")
    print("===========================================")
    print()

    # Kiem tra API Key
    if API_KEY == "PUT_YOUR_API_KEY_HERE":
        print(">> Chu y: Ban chua nhap API Key.")
        print("> Script se dung demo data (5 videos mau).")
        print("> De lay data thuc te, dien API Key va PLAYLIST_ID.")
        print("> Lay API Key tai: https://console.cloud.google.com/")
        print()

    # Kiem tra Playlist ID
    if PLAYLIST_ID == "PUT_YOUR_PLAYLIST_ID_HERE":
        print(">> Chu y: Ban chua nhap PLAYLIST_ID.")
        print("> Script se dung demo data.")
        print("> Dien ID playlist YouTube de lay data thuc te.")
        print()

    build_vault(PLAYLIST_ID, API_KEY, VAULT_NAME, GROUPS)
