# -*- coding: utf-8 -*-
"""Assemble slides.html: viewport-base + inline fonts + custom CSS (+ lesson02 CSS)
   + chrome CSS/DOM + 22 slides + full editable runtime (patched) + deck-specific interactions.
   Lesson 02 · 输出、注释与基础 Debug。共享片段（fonts-inline.css / frag-style.css）仍从 .design/fonts-tmp 读取。"""
import io, os, re, sys

BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(BASE, '..', '..'))
REF = os.path.join(ROOT, '.agents', 'skills', 'frontend-slides-editable', 'examples', 'editable-deck-reference.html')
OUT = os.path.join(ROOT, 'lessons', '02-output-comments-debug', 'slides.html')

def read(p):
    with io.open(p, encoding='utf-8') as f:
        return f.read()

ref = read(REF)

# --- 1. chrome CSS slice (edit shell: progress bar, toggles, sidebar, objects, RTE, laser) ---
css_start = ref.index('/* === deck chrome (fixed UI) === */')
css_end_marker = 'body.deck-edit-mode.slide-anim-paused .reveal { transition: none !important; }'
css_end = ref.index(css_end_marker) + len(css_end_marker)
chrome_css = ref[css_start:css_end]

# --- 2. chrome DOM slice (left hover cluster .. rte toolbar) ---
dom_start = ref.index('<div class="deck-left-hover-anchor"')
dom_end = ref.index('<div class="slides-offset">')
chrome_dom = ref[dom_start:dom_end].rstrip()

# --- 3. runtime JS slice ---
js_start = ref.index('(function () {')
js_end = ref.index('})();') + len('})();')
runtime_js = ref[js_start:js_end]

# --- 4a. patch: strip transient states (reveal / stepped) from saved & exported decks ---
patch_anchor = "root.querySelectorAll('.snap-line-v, .snap-line-h').forEach((el) => el.remove());"
assert runtime_js.count(patch_anchor) == 1, 'patch anchor not unique'
runtime_js = runtime_js.replace(
    patch_anchor,
    patch_anchor + "\n"
    "    root.querySelectorAll('[data-reveal].revealed').forEach((el) => el.classList.remove('revealed')); /* 课件：Reveal 状态不持久化 */\n"
    "    root.querySelectorAll('.step-shown').forEach((el) => el.classList.remove('step-shown')); /* 课件：分步揭示状态不持久化 */\n"
    "    root.querySelectorAll('.seg-now').forEach((el) => el.classList.remove('seg-now')); /* 课件：代码段高亮状态不持久化 */\n"
    "    root.querySelectorAll('.steps-instant').forEach((el) => el.classList.remove('steps-instant')); /* 课件：直达终态标记不持久化 */"
)

# --- 4b. patch: stepped reveal —— 键盘统一 next/prev 入口先询问 StepManager；补 ←/→ ---
keys_old = """    _keys(e) {
      if (document.body.classList.contains('deck-edit-mode')) {
        if (e.target.closest('.slide-object-text[contenteditable="true"]')) return;
        if (e.key === 'ArrowDown' || e.key === 'PageDown' || e.key === ' ') {
          e.preventDefault(); this.goTo(this.current + 1);
        } else if (e.key === 'ArrowUp' || e.key === 'PageUp') {
          e.preventDefault(); this.goTo(this.current - 1);
        }
      } else {
        if (e.key === 'ArrowDown' || e.key === 'PageDown' || e.key === ' ') {
          e.preventDefault(); this.goTo(this.current + 1);
        } else if (e.key === 'ArrowUp' || e.key === 'PageUp') {
          e.preventDefault(); this.goTo(this.current - 1);
        }
      }
    }"""
keys_new = """    _keys(e) {
      if (document.body.classList.contains('deck-edit-mode')) {
        if (e.target.closest('.slide-object-text[contenteditable="true"]')) return;
        if (e.key === 'ArrowDown' || e.key === 'PageDown' || e.key === ' ') {
          e.preventDefault(); this.goTo(this.current + 1);
        } else if (e.key === 'ArrowUp' || e.key === 'PageUp') {
          e.preventDefault(); this.goTo(this.current - 1);
        }
      } else {
        if (e.key === 'ArrowDown' || e.key === 'PageDown' || e.key === ' ' || e.key === 'ArrowRight') {
          e.preventDefault();
          if (window.__deckStepNav && window.__deckStepNav('next')) return;
          this.goTo(this.current + 1);
        } else if (e.key === 'ArrowUp' || e.key === 'PageUp' || e.key === 'ArrowLeft') {
          e.preventDefault();
          if (window.__deckStepNav && window.__deckStepNav('prev')) return;
          this.goTo(this.current - 1);
        }
      }
    }"""
assert runtime_js.count(keys_old) == 1, 'keys patch anchor not unique'
runtime_js = runtime_js.replace(keys_old, keys_new)

# --- 4c. patch: stepped reveal —— 滚轮统一 next/prev 入口同样先询问 StepManager ---
wheel_old = """    _wheel(e) {
      if (document.body.classList.contains('deck-edit-mode')) return;
      if (Math.abs(e.deltaY) < 8) return;
      e.preventDefault();
      if (e.deltaY > 0) this.goTo(this.current + 1);
      else this.goTo(this.current - 1);
    }"""
wheel_new = """    _wheel(e) {
      if (document.body.classList.contains('deck-edit-mode')) return;
      if (Math.abs(e.deltaY) < 8) return;
      e.preventDefault();
      if (e.deltaY > 0) {
        if (window.__deckStepNav && window.__deckStepNav('next')) return;
        this.goTo(this.current + 1);
      } else {
        if (window.__deckStepNav && window.__deckStepNav('prev')) return;
        this.goTo(this.current - 1);
      }
    }"""
assert runtime_js.count(wheel_old) == 1, 'wheel patch anchor not unique'
runtime_js = runtime_js.replace(wheel_old, wheel_new)

# --- 5. fragments ---
viewport_css = read(os.path.join(ROOT, '.agents', 'skills', 'frontend-slides-editable', 'viewport-base.css'))
fonts_css = read(os.path.join(ROOT, '.design', 'fonts-tmp', 'fonts-inline.css'))
custom_css = read(os.path.join(ROOT, '.design', 'fonts-tmp', 'frag-style.css'))
lesson_css = read(os.path.join(BASE, 'frag-style-02.css'))
slides_html = read(os.path.join(BASE, 'frag-slides.html')).strip()
extra_js = read(os.path.join(BASE, 'frag-extra.js')).strip()

html = f"""<!DOCTYPE html>
<html lang="zh-CN" data-deck-id="py02-output-comments-debug-v1" data-template-edit-mode="components" data-mobile-adaptation="desktop-default">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>第 2 章 · 输出、注释与基础 Debug — 课件</title>
<style>
/* === SECTION: viewport-base.css（完整内联，禁止删改） === */
{viewport_css}
/* === SECTION: 拉丁字体 @font-face（Google Fonts latin 子集，base64 内联，无外链） === */
{fonts_css}
/* === SECTION: 三风格设计系统 + 课件元件 === */
{custom_css}
/* === SECTION: 第 2 章专属补充样式 === */
{lesson_css}
/* === SECTION: 可编辑运行时 chrome（取自 editable-deck-reference，仅使用 --deck-chrome-* 变量） === */
{chrome_css}
</style>
</head>
<body>

{chrome_dom}

<div class="slides-offset">
{slides_html}
</div>

<script>
/* === SECTION: 可编辑运行时（SlideDeck / 对象编辑器 / Pages 侧栏 / HistoryStack / Ctrl+S / 导出 / 激光笔 / 全屏） === */
{runtime_js}
</script>

{extra_js}

</body>
</html>
"""

with io.open(OUT, 'w', encoding='utf-8', newline='\n') as f:
    f.write(html)
print('written:', OUT)
print('bytes:', os.path.getsize(OUT))
