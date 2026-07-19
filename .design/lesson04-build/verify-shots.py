# -*- coding: utf-8 -*-
"""第 4 章 slides.html 交付前冒烟：1280×720 逐页走查。
   1) 每页 overflow 检查（页内禁止滚动）  2) 关键页截图  3) 分步揭示 / 点击揭示 / 编辑模式冒烟  4) 控制台错误。"""
import pathlib, sys
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parents[2]
URL = (ROOT / 'lessons' / '04-strings-formatting' / 'slides.html').as_uri()
OUT = pathlib.Path(__file__).resolve().parent / 'shots'
OUT.mkdir(exist_ok=True)

errors = []

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={'width': 1280, 'height': 720})
    pg.on('console', lambda m: errors.append('console: ' + m.text) if m.type == 'error' else None)
    pg.on('pageerror', lambda e: errors.append('pageerror: ' + str(e)))
    pg.goto(URL)
    pg.wait_for_timeout(1500)

    def shot(name):
        pg.screenshot(path=str(OUT / f'{name}.png'))

    def right(n=1, wait=260):
        for _ in range(n):
            pg.keyboard.press('ArrowRight')
            pg.wait_for_timeout(wait)

    def cur_slide():
        return pg.evaluate("document.querySelector('.slides-offset > section.slide.visible')?.id")

    # ---- 1. 全页 overflow 检查 ----
    overs = pg.eval_on_selector_all(
        '.slides-offset > section.slide',
        "els => els.map(e => ({ id: e.id, over: e.scrollHeight - e.clientHeight }))")
    bad = [o for o in overs if o['over'] > 1]
    print('slides:', len(overs), '| overflow pages:', bad if bad else 'NONE')

    # ---- 2. 逐页走查 + 关键页截图 ----
    shot('p01-cover')                                    # slide-0 封面
    right(); pg.wait_for_timeout(700); shot('p02-goals')          # slide-1 三个问题
    right(); pg.wait_for_timeout(700); shot('p03-quotes')         # slide-2 两种引号
    right(); pg.wait_for_timeout(700); shot('p04-boundary')       # slide-3 引号边界
    right(); pg.wait_for_timeout(700); shot('p05-concat')         # slide-4 拼接
    right(); pg.wait_for_timeout(700); shot('p06-predict-hidden') # slide-5 拼接预测
    pg.click('.slide.visible .b-revealbar'); pg.wait_for_timeout(500); shot('p06-predict-revealed')
    right(); pg.wait_for_timeout(700); shot('p07-typeerr-hidden') # slide-6 类型拼接报错
    pg.click('.slide.visible .b-revealbar'); pg.wait_for_timeout(500); shot('p07-typeerr-revealed')
    right(); pg.wait_for_timeout(700); shot('p08-first-fstring')  # slide-7
    right(); pg.wait_for_timeout(700); shot('p09-anatomy-a')      # slide-8 仅代码
    right(); pg.wait_for_timeout(600); shot('p09-anatomy-b1')     # ① 前缀 f 高亮
    right(); pg.wait_for_timeout(600); shot('p09-anatomy-b2')     # ② 引号高亮
    right(); pg.wait_for_timeout(600); shot('p09-anatomy-b3')     # ③ 占位表达式高亮
    right(); pg.wait_for_timeout(700); shot('p10-nof-hidden')     # slide-9 少了 f
    pg.click('.slide.visible .b-revealbar'); pg.wait_for_timeout(500); shot('p10-nof-revealed')
    right(); pg.wait_for_timeout(700); shot('p11-multi-vars')     # slide-10
    right(); pg.wait_for_timeout(700); shot('p12-escape')         # slide-11 S 转义
    right(); pg.wait_for_timeout(1500); shot('p13-newline')       # slide-12 \n 输出三行
    right(); pg.wait_for_timeout(700); shot('p14-tab-backslash')  # slide-13
    right(); pg.wait_for_timeout(700); shot('p15-quote-escape')   # slide-14
    right(); pg.wait_for_timeout(700); shot('p16-combo')          # slide-15
    right(); pg.wait_for_timeout(700); shot('p17-checklist')      # slide-16 快速排错
    right(); pg.wait_for_timeout(1000); shot('p18-declaration')   # slide-17 C 宣言
    right(); pg.wait_for_timeout(1000); shot('p19-v3')            # slide-18 V3 面板
    right(); pg.wait_for_timeout(900); shot('p20-menu-hidden')    # slide-19
    pg.click('.slide.visible .c-revealbar'); pg.wait_for_timeout(500); shot('p20-menu-revealed')
    right(); pg.wait_for_timeout(900); shot('p21-your-turn')      # slide-20
    right(); pg.wait_for_timeout(900); shot('p22-summary')        # slide-21
    print('final slide:', cur_slide())

    # ---- 3. 编辑模式冒烟：E 进入 → 全部内容可见；Esc 退出 ----
    pg.keyboard.press('e'); pg.wait_for_timeout(600)
    editing = pg.evaluate("document.body.classList.contains('deck-edit-mode')")
    hidden = pg.evaluate(
        "[...document.querySelectorAll('.slide.visible .rvi, .slide.visible .rvi-pop, .slide.visible .b-pop')]"
        ".filter(e => getComputedStyle(e).opacity !== '1').length")
    pg.keyboard.press('Escape'); pg.wait_for_timeout(400)
    exited = pg.evaluate("!document.body.classList.contains('deck-edit-mode')")
    print(f'edit mode: entered={editing} hidden_while_editing={hidden} exited={exited}')

    b.close()

print('console errors:', errors if errors else 'NONE')
sys.exit(1 if (errors or bad) else 0)
