"""
classify.py - Phan loai tieu de video YouTube vao 3 nhom chinh

Cach su dung:
    python classify.py --input videos.json --output classification.json
    python classify.py --input videos.json --output classification.csv
"""

import json
import csv
import argparse
import re
from pathlib import Path
from collections import defaultdict


# ========== CAU TRUC 3 NHOM CHINH + SUB-FOLDER ==========
GROUPS = {
    "01_Dau_Khach": {
        "label": "Dau Khach",
        "subfolders": {
            "Tim_Khach": ["tim", "tim khach", "lead", "prospecting", "khach hang", "timkiem", "thu hut khach", "marketing", "content", "facebook", "zalo", "seo"],
            "Hen_Gap": ["hen", "gap", "cuoc hen", "lien he", "call", "telesale", "svn", "script", "kichcham", "chat truoc"],
            "Phap_Ly": ["phap ly", "phaply", "so do", "giay to", "cong chung", "hop dong", "chuyen nhuong", "sang ten", "thue", "nghia vu tai chinh"],
            "Quan_He_Khach": ["quan he", "cham khach", "cskh", "bao duong", "loyalty", "gioi thieu", "referral", "review", "danh gia"],
        }
    },
    "02_Dau_Chu": {
        "label": "Dau Chu",
        "subfolders": {
            "Tim_Nguon_Hang": ["tim", "lay", "nguon hang", "bat hang", "ds", "database", "chu nha", "co chu", "contract", "ky hop dong", "doc quyen"],
            "Tham_Dinh": ["tham dinh", "dinh gia", "appraisal", "gia tri", "so sanh", "market value", "thuc te", "khao sat"],
            "Quan_He_Doi_Tac": ["doi tac", "chu dau tu", "CĐT", "co chu dau tu", "lien ket", "秸秆 du an", "nha phat trien", "developer"],
        }
    },
    "03_Ky_Nang_Nghiep_Vu": {
        "label": "Ky Nang / Nghiep Vu Chung",
        "subfolders": {
            "Quy_Trinh_Ban_Hang": ["quy trinh", "proces", "ban hang", "closing", "chot sale", "sales pipeline", "funnel", "CRM"],
            "Ky_Nang_Mem": ["ky nang", "giao tiep", "thuyet phuc", "dam phan", "tu duy", "mindset", "luong tam nghe", "dao duc", "tinh than"],
            "Kien_Thuc_Thi_Truong": ["thi truong", "bat dong san", "BDS", "kinh te", "lua tai", "phi rut", "xu huong", "dinh gia vung", "cap nhat thi truong"],
            "Cong_Nu": ["cong cu", "tool", "CRM", "phần mềm", "app", "automation", "auto", "Zalo OA", "phan mem"],
            "Case_Study_Thuc_Te": ["case study", " thuc te", "kinh nghiem", "bai hoc", "that bai", "thanh cong", "cau chuyen", "review du an"],
        }
    },
}

# ========== HAM PHAN LOAI ==========
def normalize_text(text):
    return re.sub(r'[^\w\s]', '', text.lower())

def classify_title(title):
    title_lower = normalize_text(title)
    matches = []  # List of (group_key, subfolder_key, num_matched_keywords)

    for gk, gdata in GROUPS.items():
        for sfk, keywords in gdata["subfolders"].items():
            count = sum(1 for kw in keywords if kw in title_lower)
            if count > 0:
                matches.append((gk, sfk, count))

    if not matches:
        return {
            "group": "00_Chua_Phan_Loai",
            "group_label": "Chua Phan Loai",
            "subfolder": "Uncategorized",
            "subfolder_label": "Can xem thu cong",
            "matched_keywords": [],
        }

    matches.sort(key=lambda x: -x[2])
    best = matches[0]
    gk, sfk, _ = best
    return {
        "group": gk,
        "group_label": GROUPS[gk]["label"],
        "subfolder": sfk,
        "subfolder_label": sfk.replace("_", " "),
        "matched_keywords": [
            kw for kw in GROUPS[gk]["subfolders"][sfk] if kw in title_lower
        ],
    }

def classify_videos(videos):
    for v in videos:
        title = v.get("title", "")
        cl = classify_title(title)
        v["classification"] = cl
    return videos


def to_csv(results, outpath):
    rows = []
    for v in results:
        rows.append({
            "id": v.get("id", ""),
            "title": v.get("title", ""),
            "url": v.get("url", ""),
            "group": v["classification"]["group"],
            "group_label": v["classification"]["group_label"],
            "subfolder": v["classification"]["subfolder"],
            "matched_keywords": "|".join(v["classification"]["matched_keywords"]),
        })
    with open(outpath, "w", encoding="utf-8", newline="") as f:
        fieldnames = ["id", "title", "url", "group", "group_label", "subfolder", "matched_keywords"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"[CSV] Da xuat: {outpath} ({len(rows)} dong)")


def main():
    parser = argparse.ArgumentParser(description="Phan loai tieu de video Moi Gioi BDS")
    parser.add_argument("--input", required=True, help="Input JSON (danh sach video)")
    parser.add_argument("--output", required=True, help="Output file (.json hoac .csv)")
    parser.add_argument("--stats", action="store_true", help="In thong ke")
    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        videos = json.load(f)

    print(f"[INFO] Da doc {len(videos)} video tu {args.input}")
    results = classify_videos(videos)

    suffix = Path(args.output).suffix.lower()
    if suffix in (".json", ):
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"[JSON] Da xuat: {args.output}")
    elif suffix == ".csv":
        to_csv(results, args.output)
    else:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"[JSON] Da xuat: {args.output}")

    if args.stats:
        stats = defaultdict(int)
        for v in results:
            key = f"{v['classification']['group']} / {v['classification']['subfolder']}"
            stats[key] += 1
        for k, c in sorted(stats.items()):
            print(f"  {k}: {c}")
        print(f"Tong: {len(results)} video")


if __name__ == "__main__":
    main()
