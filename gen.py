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

PLAYLIST_ID = os.getenv("PLAYLIST_ID", "PUT_YOUR_PLAYLIST_ID_HERE")
API_KEY     = os.getenv("API_KEY", "PUT_YOUR_API_KEY_HERE")
VAULT_NAME  = os.getenv("VAULT_NAME", "Moi_Gioi_BDS_Vault")

GROUPS = {
    "00_Dau_Khach": {
        "name": "Ky nang dau khach - Nam khach mua",
        "description": "Tim khach, loc khach, hen gap, xu ly tu choi, dung tien nguoi khac",
        "video_ids": [
            "4azdZAVtAJ8", "Fww4yKlHfQo", "_otwhnlkdCU", "XFOeh8-UntY",
            "UsFB_4_NQdc", "QkXKId4TciA", "3sxQ3Vum9cs", "A4UkQnoh9po",
            "8NjO0oJaPKU", "4E3o23y1PxY", "XFGhe8-UntY", "tGyGSzdqlxY",
            "XFGhe8-UntY"
        ]
    },
    "01_Dau_Chu": {
        "name": "Ky nang dau chu - Kho hang va chinh chu",
        "description": "Tim chinh chu, kho nha, dam phan phi, xu ly chu nha, doc quyen",
        "video_ids": [
            "YtCixJMPFjk", "otLFcsLcLh4", "BjF4miWd-_I", "lgqA_G-Cdc8",
            "m0KoIHw2b_I", "ngE9ESDFA9w", "FaRQXY9inTc", "sUNnjs6kAPI",
            "GEYlriwCuts", "RdyC1xgo83E", "1E4Im_iIl_E", "6cVGJPbJg3o",
            "_uanh3bLKd4", "2mUxPbfx8ts", "_NjxG9GlcUk", "YGqA_G-Cdc8",
            "Ovqiuy5P7Ac", "iUws6V8A5vU", "A2Q7VXXw4fg", "sp90Y6TxjzY",
            "zQGuvxlfraA", "ZP4XSuOwFo4", "DYJV0pjfmpk", "zSxr-U9wBx0"
        ]
    },
    "02_Tu_Duy": {
        "name": "Tu duy nghe & tu duy thu nhap",
        "description": "Mindset nghe, thu nhap, chon phan khuc, nguoi di cung",
        "video_ids": [
            "5GfA9Rr_X5E", "XxbHjskkMZc", "p0NjNzyFEbM", "RwIlSX2LMc0",
            "nMZxKyLEQr8", "qSdT1o1wfrQ", "gpWnRyybkDA", "l5Tb4E5eaZM",
            "zNof37BnNxs", "BU6GjTG3JXU", "D3kpI12M1uQ", "5iRpdcfZKho",
            "_WqWajozEk8", "8joQSWKiqfg",
            "zNof37BnNxs", "25_RV4qcFPI"
        ]
    },
    "03_Phap_Ly": {
        "name": "Phap ly & thu tuc",
        "description": "Thue, hop dong, so do, rui ro phap ly, thu tuc mua ban",
        "video_ids": [
            "yHURxstqOPU", "V1OnKt_7Dz0", "E24CkzErhjw", "c5Gd656sp4A",
            "59Z_jBUc7xc", "alITw78xb1o"
        ]
    },
    "04_Nghiep_Vu": {
        "name": "Ky nang nghiep vu tong quat",
        "description": "Quan ly kho, chong cat phi, quan ly thong tin, phoi hop",
        "video_ids": [
            "VMPO3WS1RqE", "XSGaRYJ1lrk", "8hvNcvWPrY8", "9twKfTB4PMY",
            "b_6kjdo15C0", "b-NQmpR0Pak", "sR6ASGnvPsM", "wX3tzp5xD1A",
            "7g7xVnFm2JQ", "yWIrNzI4HJk", "OxnyyjKVvLo",
            "xoL5iOYoM9o", "Yip0EDKXGzk", "gCtIRw0audg", "NvxkbHX07r4",
            "Yip0EDKXGzk"
        ]
    },
    "05_Chien_Luoc": {
        "name": "Chien luoc & dau tu",
        "description": "Chon san pham, phan khuc, chien luoc mua ban, marketing",
        "video_ids": [
            "SQoDnFvD_L8", "7FES0jA2FGQ", "euwumHAv0IU", "627FSFKXBHM",
            "2DuyDn0b5HI", "-GF-lLgZbtY", "V5DKyqce1nw", "Ml5kQAlBqz0",
            "tGyGSzdqlxY", "bmWdSuEuqOo", "lr1nyPfuBiM",
            "prlpmICm-hY"
        ]
    },
    "06_Chot_Sale": {
        "name": "Ky nang chot sale & chot phi",
        "description": "Chot giao dich, chot phi, ky thuat cuoi quy trinh",
        "video_ids": [
            "uT71-v03JFI", "1E4Im_iIl_E", "5cV7gjwDc", "E8Ohp4wFoOA",
            "cGbdoi_r6eQ", "4E3o23y1PxY", "YT5cV7gjwDc",
            "wKdet96ojUc"
        ]
    }
}

def slugify(text):
    text = text.lower().strip()
    text = ''.join(c for c in text if c.isalnum() or c in ' -')
    text = text.replace(' ', '-')
    text = ''.join(c for c in text if c.isalnum() or c == '-')
    text = '-'.join(filter(None, text.split('-')))
    return text[:80]

def create_safe_filename(title):
    return f"{slugify(title)}.md"

def to_wikilink(filename):
    name = Path(filename).stem
    return f"[[{name}]]"

def get_toc_filename(group_key):
    parts = group_key.split('_')
    name_parts = parts[1:] if len(parts) > 1 else parts
    return "Muc_Luc_" + "_".join(name_parts) + ".md"

def fetch_playlist_videos(playlist_id, api_key):
    if not api_key or api_key == "PUT_YOUR_API_KEY_HERE":
        print(">> Khong co API Key, dung demo data.")
        return []
    if not HAS_API:
        print(">> Chuong trinh chua cai dat thu vien. Dung demo data.")
        print(">> Cu: pip install -r requirements.txt")
        return []

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
        return []
    return videos

def filter_video_by_group(video_id, groups):
    for key, info in groups.items():
        if video_id in info.get("video_ids", []):
            return key
    return "02_Tu_Duy"

def generate_video_markdown(video, vault_path, all_files, groups):
    title       = video["title"]
    video_id    = video["id"]
    group_key   = filter_video_by_group(video_id, groups)
    group_name  = groups[group_key]["name"]
    description = video.get("description", "")
    filename    = create_safe_filename(title)
    filepath    = vault_path / filename

    toc_links = [f"- {to_wikilink(get_toc_filename(k))}" for k in groups.keys()]

    content_lines = [
        f"# {title}",
        f"*Nhom: {group_name}*",
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
    content_lines.extend(["", "## Quay lai Muc luc nhom"])
    content_lines.extend(toc_links)
    content_lines.extend([
        "",
        "---",
        f"*Auto-generated by gen.py | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*",
        "",
    ])
    content = "\n".join(content_lines)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    return filename

def create_group_toc(group_key, group_info, videos_in_group, vault_path, groups):
    group_name = group_info["name"]
    filename   = get_toc_filename(group_key)
    filepath   = vault_path / filename

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
        title     = video["title"]
        video_id  = video["id"]
        file_name = create_safe_filename(title)
        yt_link   = f"https://www.youtube.com/watch?v={video_id}"
        content_lines.append(
            f"| {idx} | {title} | [Xem]({yt_link}) | {to_wikilink(file_name)} |"
        )
    other_links = [f"- {to_wikilink(get_toc_filename(k))}" for k in groups.keys() if k != group_key]
    content_lines.extend(["", "## Dieu huong den nhom khac"])
    content_lines.extend(other_links)
    content_lines.extend([
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
    all_files = []
    for video in videos:
        group_key = filter_video_by_group(video["id"], groups)
        group_videos[group_key].append(video)

    print(">> Dang tao file markdown cho cac videos...")
    for video in videos:
        filename = generate_video_markdown(video, vault_path, all_files, groups)
        all_files.append(filename)

    group_toc_files = []
    print(">> Dang tao Muc luc cho cac nhom...")
    for group_key, group_info in groups.items():
        filename = create_group_toc(group_key, group_info, group_videos[group_key], vault_path, groups)
        group_toc_files.append(filename)

    index_file = create_index_file(group_toc_files, group_videos, vault_path, groups)
    metadata = {
        "vault_name": vault_name,
        "playlist_id": playlist_id,
        "total_videos": len(videos),
        "generated_at": datetime.now().isoformat(),
        "groups": {k: {"name": v["name"], "video_count": len(group_videos[k])} for k, v in groups.items()},
        "files": all_files
    }
    with open(vault_path / "vault_metadata.json", "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)

    total = len(all_files) + len(group_toc_files) + 2
    print(f"\n===== HOAN THANH =====")
    print(f"Da tao {total} files trong: {vault_path}")
    for k in groups.keys():
        print(f"  {groups[k]['name']}: {len(group_videos[k])} videos")
    print("========================")

def create_index_file(group_toc_files, group_videos, vault_path, groups):
    filename  = "Tong_Muc_Luc.md"
    filepath  = vault_path / filename
    total_videos = sum(len(v) for v in group_videos.values())
    total_files  = total_videos + len(groups) + 2

    content_lines = [
        "# Tong Muc Luc - Moi Gioi BDS",
        "",
        f"*Thu vien markdown cho playlist YouTube Moi Gioi BDS | {datetime.now().strftime('%Y-%m-%d')}*",
        "",
        "## Dieu huong nhanh",
        "",
    ]
    for group_key in groups.keys():
        toc_file = get_toc_filename(group_key)
        info = groups[group_key]
        count = len(group_videos.get(group_key, []))
        content_lines.append(f"- {to_wikilink(toc_file)} - {info['name']} ({count} videos)")

    content_lines.extend(["", "## Tong quan", "Ban co the duyet qua toan bo noi dung theo cac nhom chinh:"])
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
        f"- Tong so videos: {total_videos}",
        f"- Tong so file: {total_files} ({total_videos} video + {len(groups)} Muc luc + 1 Index + 1 Metadata)",
        "",
        "---",
        f"*Auto-generated by gen.py | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*",
        "",
    ])
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(content_lines))
    return filename

if __name__ == "__main__":
    if HAS_DOTENV:
        load_dotenv()    
        print(">> Da load bien moi truong tu .env")
    print("===========================================")
    print(" MOI GIOI BDS VAULT GENERATOR")
    print("===========================================")
    print()
    if API_KEY == "PUT_YOUR_API_KEY_HERE":
        print(">> Chu y: Ban chua nhap API Key.")
        print("> Lay API Key tai: https://console.cloud.google.com/")
        print()
    if PLAYLIST_ID == "PUT_YOUR_PLAYLIST_ID_HERE":
        print(">> Chu y: Ban chua nhap PLAYLIST_ID.")
        print("> Script se dung demo data.")
        print()
    build_vault(PLAYLIST_ID, API_KEY, VAULT_NAME, GROUPS)
