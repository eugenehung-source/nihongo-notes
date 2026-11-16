#!/usr/bin/env python3
"""
日文文法筆記站 — 自動檢查腳本
用法：python3 scripts/check.py
檢查項目對應 AGENTS.md 的規則；任何 AI 或協作者在提交前都必須跑過並顯示「全部通過」。
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GRAMMAR = ROOT / "grammar"
CATALOG = ROOT / "assets" / "js" / "catalog.js"

LEVELS = {"N5", "N4", "N3", "N2", "N1"}
CATEGORIES = {"時態・狀態", "變化", "推測・判斷", "同時・順序", "原因・理由", "條件・假定", "敬語・授受", "其他"}
SECTIONS = ["meaning", "connection", "examples", "notes", "compare", "quiz", "related"]
FILENAME = re.compile(r"^n[1-5]-[a-z0-9]+(?:-[a-z0-9]+)*\.html$")
REQUIRED_KEYS = ["id", "pattern", "reading", "level", "category", "meaning", "tags", "updated"]

errors = []


def err(where, msg):
    errors.append(f"  ✗ {where}: {msg}")


def load_catalog():
    src = CATALOG.read_text(encoding="utf-8")
    body = src[src.index("[") : src.rindex("]") + 1]
    body = re.sub(r"//.*", "", body)                       # 去除註解
    body = re.sub(r"(\w+)\s*:", r'"\1":', body)            # key 加引號
    body = re.sub(r",\s*([}\]])", r"\1", body)             # 去除尾逗號
    return json.loads(body)


def main():
    try:
        catalog = load_catalog()
    except Exception as e:  # noqa: BLE001
        print(f"✗ catalog.js 無法解析：{e}")
        return 1

    # --- catalog 本身 ---
    ids = [c.get("id") for c in catalog]
    if ids != sorted(ids):
        err("catalog.js", "陣列沒有依 id 字母順序排列（§7）")
    seen = set()
    for c in catalog:
        cid = c.get("id", "?")
        for k in REQUIRED_KEYS:
            if k not in c:
                err(f"catalog:{cid}", f"缺少欄位 {k}")
        if cid in seen:
            err(f"catalog:{cid}", "id 重複")
        seen.add(cid)
        if c.get("level") not in LEVELS:
            err(f"catalog:{cid}", f"level 必須是 N5–N1，目前是 {c.get('level')}")
        elif not cid.startswith(c["level"].lower() + "-"):
            err(f"catalog:{cid}", "id 開頭等級與 level 欄位不一致")
        if c.get("category") not in CATEGORIES:
            err(f"catalog:{cid}", f"category 不在允許清單（§7.1）：{c.get('category')}")
        if len(c.get("meaning", "")) > 20:
            err(f"catalog:{cid}", "meaning 超過 20 字")
        if len(c.get("tags", [])) > 3:
            err(f"catalog:{cid}", "tags 超過 3 個")
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", c.get("updated", "")):
            err(f"catalog:{cid}", "updated 格式須為 YYYY-MM-DD")
        if not (GRAMMAR / f"{cid}.html").exists():
            err(f"catalog:{cid}", f"找不到對應檔案 grammar/{cid}.html")

    # --- 每個文法頁 ---
    pages = sorted(GRAMMAR.glob("*.html"))
    for p in pages:
        name = p.name
        html = p.read_text(encoding="utf-8")
        pid = name[:-5]
        if not FILENAME.match(name):
            err(name, "檔名不符合 {等級}-{slug}.html 規則（§4.1）")
        if pid not in seen:
            err(name, "沒有登錄在 catalog.js（首頁會看不到）")
        m = re.search(r'<body data-id="([^"]+)"', html)
        if not m or m.group(1) != pid:
            err(name, "<body data-id> 必須等於檔名")
        if re.search(r"\[[^\]<>]*\|[^\]<>]*\]", html):
            err(name, "有未轉換的 [漢字|かな] 寫法，請改用 <ruby>")
        if "{{" in html:
            err(name, "仍有未替換的 {{佔位符}}")
        found = re.findall(r'<section id="([^"]+)"', html)
        if found != SECTIONS:
            err(name, f"section 順序/名稱錯誤，應為 {SECTIONS}，目前 {found}")
        n_ex = html.count('class="example"')
        if not 3 <= n_ex <= 5:
            err(name, f"例句需 3–5 句，目前 {n_ex} 句")
        if html.count("<ruby>") != html.count("<rt>"):
            err(name, "<ruby> 與 <rt> 數量不一致")
        for jp in re.findall(r'<p class="jp">(.*?)</p>', html, flags=re.S):
            bare = re.sub(r"<ruby>.*?</ruby>", "", jp)
            bare = re.sub(r"<[^>]+>", "", bare)
            if re.search(r"[一-鿿]", bare):
                err(name, f"例句有漢字沒有加假名：{bare.strip()[:30]}")
            if "<mark>" not in jp:
                err(name, "例句缺少 <mark> 標出目標文法")
        if 'style="' in html or "<style" in html:
            err(name, "禁止 inline style 或頁內 <style>（§8.4）")
        for href in re.findall(r'(?:href|src)="([^"]+)"', html):
            if href.startswith("/"):
                err(name, f"禁止絕對路徑：{href}")
            if href.startswith("./") and href.endswith(".html") and not (GRAMMAR / href[2:]).exists():
                err(name, f"相關文法連結失效：{href}")

    print(f"檢查 {len(catalog)} 筆目錄、{len(pages)} 個文法頁")
    if errors:
        print("\n".join(errors))
        print(f"\n共 {len(errors)} 個問題，請修正後再提交。")
        return 1
    print("✓ 全部通過")
    return 0


if __name__ == "__main__":
    sys.exit(main())
