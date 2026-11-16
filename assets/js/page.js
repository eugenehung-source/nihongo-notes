/* 文法頁共用功能：假名開關、上一篇 / 下一篇（依 catalog.js 自動產生） */
(function () {
  "use strict";

  var LEVELS = ["N5", "N4", "N3", "N2", "N1"];
  var KEY = "nihongo-notes:hide-furigana";
  var body = document.body;

  // ---- 假名開關（記住使用者偏好；storage 不可用時就只在本頁生效）----
  var btn = document.getElementById("toggle-furigana");
  function apply(hide) {
    body.classList.toggle("hide-furigana", hide);
    if (btn) btn.textContent = hide ? "顯示假名" : "隱藏假名";
  }
  var saved = false;
  try { saved = localStorage.getItem(KEY) === "1"; } catch (e) {}
  apply(saved);
  if (btn) {
    btn.addEventListener("click", function () {
      var hide = !body.classList.contains("hide-furigana");
      apply(hide);
      try { localStorage.setItem(KEY, hide ? "1" : "0"); } catch (e) {}
    });
  }

  // ---- 上一篇 / 下一篇 ----
  var pager = document.getElementById("pager");
  var id = body.dataset.id;
  var list = (window.CATALOG || []).slice().sort(function (a, b) {
    var d = LEVELS.indexOf(a.level) - LEVELS.indexOf(b.level);
    return d !== 0 ? d : a.reading.localeCompare(b.reading, "ja");
  });
  var i = list.findIndex(function (x) { return x.id === id; });
  if (!pager || i === -1) return;

  function link(item, cls, label) {
    return '<a class="' + cls + '" href="./' + item.id + '.html"><small>' + label + "・" + item.level +
      "</small><span>" + item.pattern + "</span></a>";
  }
  var html = "";
  if (i > 0) html += link(list[i - 1], "prev", "← 上一篇");
  if (i < list.length - 1) html += link(list[i + 1], "next", "下一篇 →");
  pager.innerHTML = html;
})();
