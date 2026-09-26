# TÔI ĐI — website

Trang giới thiệu, chính sách và tải về của ứng dụng **TÔI ĐI** (xe buýt & metro TP.HCM · Hà Nội):
https://mittohoa.github.io/toidi/

- `src/pages/*.html` + `src/layout.html` → `python build.py` sinh các trang ở thư mục gốc (GitHub Pages phục vụ nhánh `main`).
- `how-it-works` sinh từ nội dung trong app: `python tools/site_method.py` (repo mã nguồn).
- `assets/config.js`: khoá Supabase **công khai** (giống trong app), sinh bởi `tools/site_config.py`.
- `downloads.json`: link tải + SHA-256 của bản APK mới nhất (Releases của repo này).

TÔI ĐI là ứng dụng độc lập, không liên kết với cơ quan nhà nước. Bản đồ © OpenStreetMap contributors.
