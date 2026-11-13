# CLAUDE.md

本專案的完整規則寫在 **AGENTS.md**，請先讀它再動手。

@AGENTS.md

## 快速提醒

- 新增文法頁：複製 `templates/grammar-template.html` → 填完所有 `{{佔位符}}` → 登錄 `assets/js/catalog.js` → 跑 `python3 scripts/check.py`
- 只用純 HTML/CSS/JS、相對路徑，不要加框架或 npm
- 樣式只能寫在 `assets/css/style.css`，只能用既有 CSS 變數
