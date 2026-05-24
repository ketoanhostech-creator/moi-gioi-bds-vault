# Moi Gioi BDS Vault

Tao thu vien markdown tu YouTube playlist cho khoa hoc Moi Gioi Bat Dong San.

## Chuc nang chinh

- **Lay data tu YouTube**: Dung YouTube Data API de lay danh sach video trong playlist
- **Auto-generate Markdown**: Tao file .md cho moi video voi tieu de, mo ta, thumbnail
- **Obsidian-style Linking**: [[Wiki links]] giua cac file de dieu huong nhanh
- **3 Nhom Noi Dung**: Phan nhom tu dong (Co Ban / Chuyen Sau / Thuc Chien)
- **Muc luc Auto**: Tao file index va toc cho tung nhom
- **Metadata JSON**: File tong hop thong tin vault

## Cai dat

### Tren may local

```bash
# Clone repo
git clone https://github.com/ketoanhostech-creator/moi-gioi-bds-vault.git
cd moi-gioi-bds-vault

# Cai dat dependencies
pip install -r requirements.txt
```

### Tren Google Colab (Nhanh - Khuyen nghi)

1. Mo [Google Colab](https://colab.research.google.com)
2. Upload file gen.py len Colab
3. Copy noi dung gen.py vao cell dau tien
4. Trong cell thu 2, dien:
   ```python
   PLAYLIST_ID = "ID_playlist_cua_ban"
   API_KEY = "API_key_cua_ban"
   ```
5. Run cell thu 3:
   ```python
   !pip install google-api-python-client
   ```
6. Run cell cua gen.py (Shift+Enter)
7. Tai vault ve: `!zip -r vault.zip Moi_Gioi_BDS_Vault` va download

## Cau hinh

Mo file `gen.py` va chinh sua cac bien sau:

```python
# Playlist ID tren YouTube
PLAYLIST_ID = "PLxxxxxx"  # Thay bang ID playlist cua ban

# API Key Google (neu khong co, script se dung demo data)
API_KEY = "YOUR_API_KEY"  # Thay bang API key

# Ten thu muc vault se duoc tao
VAULT_NAME = "Moi_Gioi_BDS_Vault"
```

### Lay API Key Google

1. Truy cap [Google Cloud Console](https://console.cloud.google.com/)
2. Tao project moi (hoac chon project co san)
3. Bat YouTube Data API v3
4. Tao API Key trong Credentials
5. Copy key vao bien `API_KEY` trong gen.py

## Lay Playlist ID

1. Mo playlist tren YouTube
2. URL se co dang: `https://www.youtube.com/playlist?list=PLxxxxxx`
3. Copy phan sau `list=` (vi du: `PLxxxxxx`)
4. Dien vao bien `PLAYLIST_ID`

## Cach su dung

### Chay local

```bash
python3 gen.py
```

### Output

Script se tao thu muc `Moi_Gioi_BDS_Vault/` voi cau truc:

```
Moi_Gioi_BDS_Vault/
├── Tong_Muc_Luc.md              # Tong muc luc chinh
├── Muc_Luc_Co_Ban.md            # Muc luc nhom Co Ban
├── Muc_Luc_Chuyen_Sau.md        # Muc luc nhom Chuyen Sau
├── Muc_Luc_Thuc_Chien.md        # Muc luc nhom Thuc Chien
├── [ten-video-1].md             # File markdown cho video 1
├── [ten-video-2].md             # File markdown cho video 2
├── ...                          # Cac file video khac
└── vault_metadata.json          # Metadata JSON
```

### Mo trong Obsidian

1. Mo Obsidian
2. Chon "Open folder as vault" -> chon thu muc `Moi_Gioi_BDS_Vault`
3. Mo file `Tong_Muc_Luc.md` de bat dau

## 3 Nhom Noi Dung

Script se phan nhom cac video thanh 3 nhom chinh:

| Nhom | Mo ta | So video (mau) |
|------|-------|----------------|
| **00_Co_Ban** | Cac bai co ban ve moi gioi bat dong san | ~34 |
| **01_Chuyen_Sau** | Cac ky nang chuyen sau trong moi gioi BDS | ~34 |
| **02_Thuc_Chien** | Cac truong hop thuc te va bai hoc kinh nghiem | ~35 |

**Luu y**: So video trong moi nhom duoc phan tu dong de. Ban co the chinh sua ham `assign_to_group()` trong gen.py de phan nhom tu tay.

## Workflow Lap lai (Them vault moi)

Khi co playlist moi, ban chi can:

1. **Copy gen.py** sang thu muc project moi
2. **Chinh sua bien cau hinh** (PLAYLIST_ID, API_KEY, VAULT_NAME, GROUPS)
3. **Chay gen.py** -> Vault moi se duoc tao
4. **Upload vault** vao GitHub (create repo moi)

## Dependencies

- Python 3.7+
- `google-api-python-client` (cho YouTube Data API)
- `requests` (cho demo data)

## License

MIT License

---

*Tao boi gen.py | Repo: [ketoanhostech-creator/moi-gioi-bds-vault](https://github.com/ketoanhostech-creator/moi-gioi-bds-vault)*
