/* 首頁：渲染文法卡片、等級 / 分類 / 關鍵字篩選 */
(function () {
  "use strict";

  var LEVELS = ["N5", "N4", "N3", "N2", "N1"];
  // 新增分類時，同步更新 AGENTS.md §7.1
  var CATEGORIES = ["時態・狀態", "變化", "推測・判斷", "同時・順序", "原因・理由", "條件・假定", "敬語・授受", "其他"];

  var data = (window.CATALOG || []).slice().sort(function (a, b) {
    var d = LEVELS.indexOf(a.level) - LEVELS.indexOf(b.level);
    return d !== 0 ? d : a.reading.localeCompare(b.reading, "ja");
  });

  var state = { level: "ALL", category: "ALL", q: "" };

  var $grid = document.getElementById("grid");
  var $count = document.getElementById("count");
  var $levels = document.getElementById("levels");
  var $cat = document.getElementById("category");
  var $q = document.getElementById("q");

  function esc(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }

  // 等級按鈕
  ["ALL"].concat(LEVELS).forEach(function (lv) {
    var b = document.createElement("button");
    b.type = "button";
    b.className = "chip";
    b.textContent = lv === "ALL" ? "全部" : lv;
    b.dataset.level = lv;
    b.setAttribute("aria-pressed", lv === "ALL" ? "true" : "false");
    b.addEventListener("click", function () {
      state.level = lv;
      Array.prototype.forEach.call($levels.children, function (c) {
        c.setAttribute("aria-pressed", c.dataset.level === lv ? "true" : "false");
      });
      render();
    });
    $levels.appendChild(b);
  });

  // 分類選單
  CATEGORIES.forEach(function (c) {
    var o = document.createElement("option");
    o.value = c;
    o.textContent = c;
    $cat.appendChild(o);
  });
  $cat.addEventListener("change", function () { state.category = $cat.value; render(); });
  $q.addEventListener("input", function () { state.q = $q.value.trim().toLowerCase(); render(); });

  function match(item) {
    if (state.level !== "ALL" && item.level !== state.level) return false;
    if (state.category !== "ALL" && item.category !== state.category) return false;
    if (!state.q) return true;
    var hay = [item.pattern, item.reading, item.meaning, item.category].concat(item.tags || []).join(" ").toLowerCase();
    return hay.indexOf(state.q) !== -1;
  }

  function render() {
    var list = data.filter(match);
    $count.textContent = "共 " + list.length + " 個文法（全站 " + data.length + " 個）";
    if (!list.length) {
      $grid.innerHTML = '<div class="empty">這個條件下還沒有文法，換個篩選試試，或請 AI 依 AGENTS.md 新增一頁。</div>';
      return;
    }
    $grid.innerHTML = list.map(function (it) {
      var tags = (it.tags || []).map(function (t) { return '<span class="tag">' + esc(t) + "</span>"; }).join("");
      return (
        '<a class="card" href="grammar/' + esc(it.id) + '.html">' +
          '<div class="meta"><span class="badge badge-' + it.level.toLowerCase() + '">' + esc(it.level) + "</span>" +
          '<span class="tag">' + esc(it.category) + "</span>" + tags + "</div>" +
          '<p class="pattern-sm">' + esc(it.pattern) + "</p>" +
          '<p class="meaning-sm">' + esc(it.meaning) + "</p>" +
        "</a>"
      );
    }).join("");
  }

  render();
})();
