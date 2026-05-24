# Moi Gioi BDS Vault

Tao thu vien markdown tu YouTube playlist cho khoa hoc Moi Gioi Bat Dong San.

![Python](https://img.shields.io/badge/Python-3.7+-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![YouTube API](https://img.shields.io/badge/API-YouTube%20Data%20v3-red)
![Obsidian](https://img.shields.io/badge/Compatible-Obsidian-7B68EE)

---

## Chuc nang chinh

- **Lay data tu YouTube**: Dung YouTube Data API v3 lay danh sach video trong playlist
- **Auto-generate Markdown**: Tao file `.md` cho moi video voi tieu de, mo ta, thumbnail
- **Obsidian-style Linking**: `[[Wiki links]]` giua cac file de dieu huong nhanh
- **3 Nhom Noi Dung**: Phan nhom tu dong (Co Ban / Chuyen Sau / Thuc Chien)
- **Muc luc Auto**: Tao file index va toc cho tung nhom
- **Metadata JSON**: File tong hop thong tin vault

---

## Cai dat

### Tren may local

```bash
# Clone repo
git clone https://github.com/ketoanhostech-creator/moi-gioi-bds-vault.git
cd moi-gioi-bds-vault

# Cai dat dependencies
pip install -r requirements.txt

# Sao che file cau hinh ma (khong bat buoc)
cp .env.example .env
# Dien PLAYLIST_ID va API_KEY vao file .env
```

### Tren Google Colab (Khuyen nghi - nhanh va mien phi)

1. Mo [Google Colab](https://colab.research.google.com/)
2. Upload file `gen.py` len Colab
3. Trong cell, dien: `PLAYLIST_ID = "ID_playlist_cua_ban"` va `API_KEY = "API_key_cua_ban"`
4. Run cell cai dat: `!pip install -r requirements.txt` (hoac `!pip install google-api-python-client requests`)
5. Run cell cua `gen.py`
6. Tai vault ve: `!zip -r vault.zip Moi_Gioi_BDS_Vault` va download

---

## Cau hinh

Mo file `gen.py` va chinh sua cac bien:

| Bien | Mo ta | Vi du |
|------|-------|-------|
| `PLAYLIST_ID` | ID playlist YouTube | `PLxxxxxxxxxxxxxxx` |
| `API_KEY` | Google Cloud API Key | `AIzaSy...` |
| `VAULT_NAME` | Ten thu muc output | `Moi_Gioi_BDS_Vault` |

> **Note**: Neu khong co API Key, script se tu dong dung demo data (5 videos mau).

---

## Cach su dung

### Chay local

```bash
python3 gen.py
```

### Output

Script tao thu muc `Moi_Gioi_BDS_Vault/` bao gom:

| File | Mo ta |
|------|-------|
| `Tong_Muc_Luc.md` | Tong muc luc chinh |
| `Muc_Luc_[Nhom].md` | Muc luc cho tung nhom |
| `[ten-video].md` | File markdown cho moi video |
| `vault_metadata.json` | Metadata tong hop |

### Mo trong Obsidian

1. Chon **"Open folder as vault"**
2. Chon thu muc `Moi_Gioi_BDS_Vault`
3. Mo file `Tong_Muc_Luc.md` de bat dau
4. Dung `Ctrl/Cmd + O` de tim kiem nhanh file

---

## 3 Nhom Noi Dung

Script phan nhom video tu dong theo chi so:

| Nhom | Mo ta | So video du kien |
|------|-------|------------------|
| `00_Co_Ban` | Cac bai co ban ve moi gioi BDS | ~34 videos |
| `01_Chuyen_Sau` | Ky nang chuyen sau nang cao | ~34 videos |
| `02_Thuc_Chien` | Case study va truong hop thuc te | ~35 videos |

---

## Cau truc thu muc

```
moi-gioi-bds-vault/
├── gen.py              # Script chinh
├── requirements.txt    # Python dependencies
├── .gitignore          # Git ignore patterns
├── .env.example        # Template cau hinh
├── README.md           # Tai lieu huong dan
└── Moi_Gioi_BDS_Vault/ # (duoc tao sau khi chay script)
    ├── Tong_Muc_Luc.md
    ├── Muc_Luc_Co_Ban.md
    ├── Muc_Luc_Chuyen_Sau.md
    ├── Muc_Luc_Thuc_Chien.md
    ├── [video-1].md
    ├── [video-2].md
    └── vault_metadata.json
```

---

## Lay YouTube Data API Key

1. Truy cap [Google Cloud Console](https://console.cloud.google.com/)
2. Tao project moi (hoac chon project co san)
3. Bat **YouTube Data API v3** trong **APIs & Services > Library**
4. Tao **API Key** trong **APIs & Services > Credentials**
5. Copy API Key va dien vao `gen.py` hoac file `.env`

---

## Dependencies

| Package | Mo ta |
|---------|-------|
| `google-api-python-client` | Client library cho YouTube Data API v3 |
| `requests` | Thu vien goi HTTP_requests |

---

## License

MIT License
