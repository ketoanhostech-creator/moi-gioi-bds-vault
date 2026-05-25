"""
gen_vault.py - Tao Obsidian vault tu ket qua phan loai

Cach su dung:
    python gen_vault.py --input classification.json --output vault
    python gen_vault.py --input classification.json --output vault --style notion
"""

import json
import argparse
from pathlib import Path
from collections import defaultdict


def slugify(text):
    parts = []
    for ch in text:
        if ch.isalnum() or ch in " -_":
            parts.append(ch)
    slug = "".join(parts).strip()
    return slug.replace(" ", "-")


def md_filename(title):
    return slugify(title) + ".md"

def gen_video_md(video):
    title = video.get("title", "")
    url = video.get("url", "")
    cls = video.get("classification", {})
    group = cls.get("group_label", "")
    subfolder = cls.get("subfolder_label", "")
    keywords = cls.get("matched_keywords", [])

    lines = [
        f"---",
        f"tags: [Video]",
        f"group: {group}",
        f"subfolder: {subfolder}",
        f"keywords: {keywords}",
        f"---",
        f"",
        f"# {title}",
        f"",
        f"> [!VIDEO] YouTube",
        f"> {url}",
        f"",
        f"## Thong tin phan loai",
        f"- **Nhom**: {group}",
        f"- **Sub-folder**: {subfolder}",
        f"- **Keywords**: {', '.join(keywords) or 'Khong co'}",
        f"",
    ]
    return "\n".join(lines)

def build_vault(videos, outdir, style="obsidian"):
    outdir = Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    by_group = defaultdict(list)
    by_subfolder = defaultdict(list)
    for v in videos:
        cls = v.get("classification", {})
        glabel = cls.get("group_label", "Uncategorized")
        slabel = cls.get("subfolder_label", "Uncategorized")
        by_group[glabel].append(v)
        by_subfolder[(glabel, slabel)].append(v)

    group_keys = sorted(by_group.keys())

    for glabel, vids in by_group.items():
        gdir = outdir / slugify(glabel)
        gdir.mkdir(parents=True, exist_ok=True)

        sf_by = defaultdict(list)
        for v in vids:
            cls = v.get("classification", {})
            slabel = cls.get("subfolder_label", "Uncategorized")
            sf_by[slabel].append(v)

        for slabel, svids in sf_by.items():
            sfdir = gdir / slugify(slabel)
            sfdir.mkdir(parents=True, exist_ok=True)

            index_md = sfdir / "index.md"
            lines = [f"# {glabel} - {slabel}", f"", f"{len(svids)} video(s) trong folder nay.", f""]
            for sv in svids:
                fn = md_filename(sv["title"])
                lines.append(f"- [[{fn.replace('.md', '')}]]")
            lines.append("")
            lines.append(f"## Danh sach video")
            lines.append(f"")
            lines.append(f"| STT | Tieu de | Link |")
            lines.append(f"|----|-----------|------|")
            for i, sv in enumerate(svids, 1):
                url = sv.get("url", "")
                lines.append(f"| {i} | {sv['title']} | {url} |")
            lines.append("")
            lines.append("---")
            lines.append(f"[[../index]] - Quay ve nhom {glabel}")
            index_md.write_text("\n".join(lines), encoding="utf-8")
            print(f"  [MD] {index_md}")
            for sv in svids:
                fn = md_filename(sv["title"])
                vmd = sfdir / fn
                vmd.write_text(gen_video_md(sv), encoding="utf-8")

        group_index = gdir / "index.md"
        glines = [f"# {glabel}", f"", f"{len(vids)} video(s) trong nhom nay.", f""]
        for slabel, svids2 in sorted(sf_by.items()):
            glines.append(f"## {slabel}")
            glines.append(f"")
            glines.append(f"{len(svids2)} video:")
            glines.append(f"")
            for sv in svids2:
                fn = md_filename(sv["title"])
                glines.append(f"- [[{slugify(slabel)}/{fn.replace('.md', '')}]]")
            glines.append(f"")
        glines.append("---")
        glines.append(f"[[../index]] - Quay ve trang chu")
        group_index.write_text("\n".join(glines), encoding="utf-8")
        print(f"  [MD] {group_index}")
    root_index = outdir / "index.md"
    rlines = ["# Moi Gioi BDS Vault", "", "Tong quan: khong gian luu tru cho playlist Moi Gioi BDS.", ""]
    rlines.append("## Cau truc vault")
    rlines.append("")
    rlines.append("| STT | Nhom | Sub-folders | Tong so video |")
    rlines.append("|-----|------|-------------|---------------|")
    for glabel in group_keys:
        vids = by_group[glabel]
        sfs = set()
        for v in vids:
            cls = v.get("classification", {})
            sfs.add(cls.get("subfolder_label", ""))
        rlines.append(f"| {group_keys.index(glabel)+1} | {glabel} | {len(sfs)} | {len(vids)} |")
    rlines.append("")
    rlines.append("## Danh sach nhom")
    rlines.append("")
    for glabel in group_keys:
        gslug = slugify(glabel)
        rlines.append(f"- [[{gslug}/index]] - {glabel}")
    rlines.append("")
    rlines.append("---")
    rlines.append(f"*Auto-generated by gen_vault.py*")
    root_index.write_text("\n".join(rlines), encoding="utf-8")
    print(f"  [MD] {root_index}")
    print(f"[DONE] Da tao {len(videos)} file MD trong {outdir}")

def main():
    parser = argparse.ArgumentParser(description="Gen Obsidian vault tu ket qua phan loai")
    parser.add_argument("--input", required=True, help="Input JSON (classification result)")
    parser.add_argument("--output", required=True, help="Output folder path")
    parser.add_argument("--style", default="obsidian", choices=["obsidian", "notion"],
                        help="Output style: obsidian or notion")
    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        videos = json.load(f)

    print(f"[INFO] Da doc {len(videos)} video tu {args.input}")
    build_vault(videos, args.output, style=args.style)


if __name__ == "__main__":
    main()
