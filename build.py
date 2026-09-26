"""Sinh các trang HTML từ src/layout.html + src/pages/*.html.

Mỗi trang nguồn bắt đầu bằng khối khai báo:
    <!--
    title: ...
    description: ...
    nav: home | how | privacy
    -->
rồi tới nội dung <main>. Có thể thêm <!--head--> ... <!--/head--> để chèn thẻ vào <head>.

Dùng:  python build.py
"""
import glob, hashlib, json, os, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    layout = open(os.path.join(ROOT, "src", "layout.html"), encoding="utf-8").read()
    # phiên bản tài nguyên = băm CSS+JS: đổi nội dung thì trình duyệt tải lại
    h = hashlib.sha1()
    for f in ("assets/site.css", "assets/site.js"):
        h.update(open(os.path.join(ROOT, f), "rb").read())
    version = h.hexdigest()[:8]
    # link tải + SHA-256 của bản phát hành (cập nhật khi đăng bản mới)
    dl_path = os.path.join(ROOT, "downloads.json")
    downloads = json.load(open(dl_path, encoding="utf-8")) if os.path.exists(dl_path) else {}
    for path in sorted(glob.glob(os.path.join(ROOT, "src", "pages", "*.html"))):
        src = open(path, encoding="utf-8").read()
        m = re.match(r"\s*<!--(.*?)-->", src, re.S)
        meta = dict(re.findall(r"^\s*(\w+):\s*(.+?)\s*$", m.group(1), re.M)) if m else {}
        body = src[m.end():] if m else src
        head = ""
        hm = re.search(r"<!--head-->(.*?)<!--/head-->", body, re.S)
        if hm:
            head, body = hm.group(1).strip(), body[:hm.start()] + body[hm.end():]
        out = layout
        nav = meta.get("nav", "")
        for key in ("home", "how", "privacy"):
            out = out.replace("{{nav_%s}}" % key, 'aria-current="page"' if nav == key else "")
        out = (out.replace("{{title}}", meta.get("title", "TÔI ĐI"))
                  .replace("{{description}}", meta.get("description", ""))
                  .replace("{{version}}", version)
                  .replace("{{head}}", head)
                  .replace("{{body}}", body.strip()))
        for k, v in downloads.items():
            out = out.replace("{{%s}}" % k, v)
        name = os.path.basename(path)
        with open(os.path.join(ROOT, name), "w", encoding="utf-8", newline="\n") as f:
            f.write(out)
        print("  ", name)


if __name__ == "__main__":
    main()
