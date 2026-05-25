# Moi Gioi BDS Vault

Tao thu vien markdown tu YouTube playlist cho khoa hoc Moi Gioi Bat Dong San, tu dong phan loai va generate Obsidian-style vault.

![Python](https://img.shields.io/badge/Python-3.7+-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Obsidian](https://img.shields.io/badge/Compatible-Obsidian-7B68EE)

---

## Chuc nang chinh

- **Phan loai tu dong**: Phan loai tieu de video vao 3 nhom chinh + 12 sub-folder dua tren tu khoa
- **Auto-generate Markdown**: Tao file `.md` cho moi video voi tieu de, mo ta, link YouTube
- **Obsidian-style Linking**: `[[Wiki links]]` giua cac file, folder, va index de dung Graph View
- **Export CSV/JSON**: Xuat ket qua phan loai ra CSV hoac JSON
- **Notion-Compatible**: Co the xuat theo style Notion voi metadata YAML

---

## Cau truc 3 Nhom Chinh

| Nhom | Mo ta | Sub-folders |
|------|-------|-------------|
| **01_Dau_Khach** | Quy trinh khai thac, hen gap, phuc vu khach hang | Tim_Khach, Hen_Gap, Phap_Ly, Quan_He_Khach |
| **02_Dau_Chu** | Tim nguon hang, tham dinh, lien ket doi tac | Tim_Nguon_Hang, Tham_Dinh, Quan_He_Doi_Tac |
| **03_Ky_Nang_Nghiep_Vu** | Ky nang, nghiep vu, cong cu chung | Quy_Trinh_Ban_Hang, Ky_Nang_Mem, Kien_Thuc_Thi_Truong, Cong_Cu, Case_Study_Thuc_Te |

---

## Quy trinh 2 Buoc

### Buoc 1: Phan loai video (classify.py)

```bash
python classify.py --input sample_data.json --output classification.json --stats
```

Hoac xuat CSV:
```bash
python classify.py --input sample_data.json --output classification.csv --stats
```

### Buoc 2: Generate Obsidian vault (gen_vault.py)

```bash
python gen_vault.py --input classification.json --output vault
```

### Chay toan bo quy trinh voi du lieu mau:

```bash
python classify.py --input sample_data.json --output classification.json --stats
python gen_vault.py --input classification.json --output vault
```

---

## Cai dat

```bash
# Clone repo
git clone https://github.com/ketoanhostech-creator/moi-gioi-bds-vault.git
cd moi-gioi-bds-vault

# Cai dat dependencies
pip install -r requirements.txt
```

---

## File cau truc

```
moi-gioi-bds-vault/
├── classify.py          # Script phan loai video (Buoc 1)
├── gen_vault.py         # Script generate Obsidian vault (Buoc 2)
├── gen.py               # Script generate markdown co ban (legacy)
├── sample_data.json     # Du lieu mau (danh sach video)
├── classification.json  # Ket qua phan loai (sau khi chay classify.py)
├── vault/               # Output vault sau khi chay gen_vault.py
│   ├── index.md         # Trang chu vault
│   ├── 01_Dau_Khach/
│   │   ├── index.md
│   │   ├── tim-khach/
│   │   │   ├── index.md
│   │   │   └── *.md     # File video
│   │   └── .../
│   ├── 02_Dau_Chu/
│   │   └── ...
│   └── 03_Ky_Nang_Nghiep_Vu/
│       └── ...
├── requirements.txt
├── README.md
└── LICENSE
```

---

## Huong dan su dung voi du lieu thuc te

### 1. Chuan bi danh sach video

Tao file `videos.json` voi danh sach video YouTube:

```json
[
  {"id": "v001", "title": "Tieu de video 1", "url": "https://youtube.com/watch?v=xxx"},
  {"id": "v002", "title": "Tieu de video 2", "url": "https://youtube.com/watch?v=yyy"}
]
```

Hoac dung `sample_data.json` co san de test.

### 2. Phan loai video

```bash
python classify.py --input videos.json --output classification.json --stats
```

Khi co `--stats`, script se in ra thong ke phan loai.

### 3. Generate obsidian vault

```bash
python gen_vault.py --input classification.json --output vault
```

### 4. Mo vault trong Obsidian

1. Mo Obsidian
2. Open folder as vault > chon folder `vault/` da duoc generate
3. Mo `index.md` de xem tong quan
4. Dung Graph View de xem cau truc lien ket giua cac file

---

## Mo rong: Xuat cho Notion

```bash
python gen_vault.py --input classification.json --output notion_vault --style notion
```

---

## License

MIT License - xem file [LICENSE](LICENSE)
