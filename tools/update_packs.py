"""Lấy dữ liệu tuyến + địa điểm mới nhất (bản phát hành công khai của mittohoa/toidi-data) cho bản web.

Ghi app/packs/<loại>/<mã>.json.gz — bản web đọc ở đây trước bản đóng sẵn, nên web luôn mới như app điện thoại.
Kiểm sha256 từng file; manifest khác schema (định dạng mới mà bản web chưa hiểu) thì không đụng gì.
Bản đồ (.pmtiles, 20–30 MB) KHÔNG cập nhật ở đây để repo website không phình to — chỉ khi dựng lại website.

Dùng:  python tools/update_packs.py     (in "changed" nếu có file đổi)
"""
import hashlib, json, os, sys, urllib.request

MANIFEST = "https://github.com/mittohoa/toidi-data/releases/latest/download/manifest.json"
SCHEMA = 1  # khớp DataUpdater.schema trong app
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
KINDS = ("transit", "places")


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "toidi-site/1.0"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read()


def main():
    m = json.loads(get(MANIFEST))
    if m.get("schema") != SCHEMA:
        print("manifest schema %s khác %s — bỏ qua" % (m.get("schema"), SCHEMA))
        return
    changed = 0
    for city, entry in m["cities"].items():
        for kind in KINDS:
            f = entry.get("files", {}).get(kind)
            if not f:
                continue
            dst = os.path.join(ROOT, "app", "packs", kind, city + ".json.gz")
            if os.path.exists(dst) and hashlib.sha256(open(dst, "rb").read()).hexdigest() == f["sha256"]:
                continue
            data = get(f.get("url") or m["base_url"] + f["path"])
            if hashlib.sha256(data).hexdigest() != f["sha256"]:
                sys.exit("sai sha256: %s/%s" % (city, kind))
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            open(dst, "wb").write(data)
            changed += 1
            print("cập nhật %s/%s (%d KB, dữ liệu ngày %s)" % (city, kind, len(data) // 1024, entry.get("data_date")))
    print("changed" if changed else "không có gì mới", "— bản dữ liệu", m.get("tag"))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
