# 日文文法筆記站 Nihongo Notes

一個文法一頁的 JLPT 日文文法筆記網站。每一頁都用同一套結構呈現：**意思 → 接續 → 例句 → 使用重點 → 易混淆比較 → 小測驗 → 相關文法**，首頁可依等級、分類、關鍵字篩選。

本專案的重點不只是網頁本身，而是 [`AGENTS.md`](./AGENTS.md)：一份讓 AI 讀完就知道「這個專案該怎麼繼續做下去」的規則書。

- 網站：`https://<你的帳號>.github.io/nihongo-notes/`
- 技術：純 HTML / CSS / JavaScript，無框架、無 build，可直接部署到 GitHub Pages

## 專案結構

| 路徑 | 說明 |
|---|---|
| `AGENTS.md` | AI 規則書：目的、風格、結構、命名、新增頁面 SOP、禁止事項 |
| `CLAUDE.md` | 給 Claude Code 的入口，指向 AGENTS.md |
| `index.html` | 首頁（文法目錄＋篩選） |
| `grammar/` | 文法頁，每個文法一個 HTML |
| `templates/grammar-template.html` | 新文法頁的唯一模板 |
| `assets/js/catalog.js` | 文法目錄資料 |
| `scripts/check.py` | 自動檢查是否符合 AGENTS.md 規則 |

## 新增一個文法

對 AI 說：

> 依照 AGENTS.md，新增 N4 文法 〜てしまう

AI 會：複製模板 → 填內容 → 登錄 `catalog.js` → 執行 `python3 scripts/check.py`。

## 本機預覽

直接用瀏覽器打開 `index.html` 即可。

## 部署到 GitHub Pages

1. 在 GitHub 建立公開 repository `nihongo-notes`
2. 上傳本資料夾所有檔案（含 `.nojekyll`）
3. Settings → Pages → Source 選 **Deploy from a branch**，Branch 選 `main` / `(root)` → Save
4. 約 1 分鐘後即可在 `https://<你的帳號>.github.io/nihongo-notes/` 瀏覽
