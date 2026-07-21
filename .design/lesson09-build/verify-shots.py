# -*- coding: utf-8 -*-
"""第 9 章 slides.html 交付前冒烟：1280×720 逐页走查。
   1) 每页 overflow 检查（页内禁止滚动）  2) 关键页截图  3) 分步揭示 / 点击揭示 / 编辑模式冒烟  4) 控制台错误。"""
import pathlib, sys
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parents[2]
URL = (ROOT / 'lessons' / '09-for-break-continue' / 'slides.html').as_uri()
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
    shot('p01-cover')                                   # slide-0 S 封面
    right(); pg.wait_for_timeout(700); shot('p02-two-kinds')        # slide-1 S 两类重复问题
    right(); pg.wait_for_timeout(700); shot('p03-first-for-code')   # slide-2 B 第一个 for（输出未揭示）
    right(); pg.wait_for_timeout(700); shot('p03-first-for-out')    # step: 输出 0..4
    right(); pg.wait_for_timeout(700); shot('p04-range-stop')       # slide-3（序列未揭示）
    right(); pg.wait_for_timeout(700)                               # step: 实际序列
    right(); pg.wait_for_timeout(700); shot('p05-range-start-stop') # slide-4
    right(); pg.wait_for_timeout(700)                               # step: 实际序列
    right(); pg.wait_for_timeout(700); shot('p06-half-open')        # slide-5 B 左闭右开
    right(); pg.wait_for_timeout(700); shot('p07-step-code')        # slide-6 B 步长
    right(); pg.wait_for_timeout(700); shot('p07-step-seq')         # step: 10、8、6、4
    right(); pg.wait_for_timeout(1300); shot('p08-predict-hidden')  # slide-7 B 范围预测
    assert cur_slide() == 'slide-7', cur_slide()
    pg.click('section.slide.visible .b-revealbar'); pg.wait_for_timeout(500)
    assert cur_slide() == 'slide-7', 'reveal 点击后不应翻页: ' + str(cur_slide())
    shot('p08-predict-revealed')
    right(); pg.wait_for_timeout(700); shot('p09-for-or-while')     # slide-8
    right(); pg.wait_for_timeout(700); shot('p10-break')            # slide-9
    right(); pg.wait_for_timeout(700); shot('p11-break-where')      # slide-10
    right(); pg.wait_for_timeout(700); shot('p12-continue-code')    # slide-11
    right(); pg.wait_for_timeout(700); shot('p12-continue-out')     # step: 1、3、5、7
    right(); pg.wait_for_timeout(700); shot('p13-one-line')         # slide-12 S 一句话区分
    right(); pg.wait_for_timeout(1300); shot('p14-while-continue-hidden') # slide-13
    assert cur_slide() == 'slide-13', cur_slide()
    pg.click('section.slide.visible .b-revealbar'); pg.wait_for_timeout(500)
    assert cur_slide() == 'slide-13', 'reveal 点击后不应翻页: ' + str(cur_slide())
    shot('p14-while-continue-revealed')
    right(); pg.wait_for_timeout(700); shot('p15-nested-break')     # slide-14（结论未揭示）
    right(); pg.wait_for_timeout(700); shot('p15-nested-break-out') # step: 只输出 1、2 列
    right(); pg.wait_for_timeout(700); shot('p16-three-questions')  # slide-15
    right(); pg.wait_for_timeout(900); shot('p17-declaration')      # slide-16 C 宣言
    right(); pg.wait_for_timeout(900); shot('p18-v8-check')         # slide-17 V8 自检
    right(); pg.wait_for_timeout(900); shot('p19-replace-input')    # slide-18
    right(); pg.wait_for_timeout(900); shot('p20-task12')           # slide-19
    right(); pg.wait_for_timeout(900); shot('p21-research-continue')# slide-20
    right(); pg.wait_for_timeout(900); shot('p22-research-ok')      # slide-21
    right(); pg.wait_for_timeout(900); shot('p23-invalid-continue') # slide-22
    right(); pg.wait_for_timeout(900); shot('p24-break-evac')       # slide-23
    right(); pg.wait_for_timeout(900); shot('p25-paths')            # slide-24
    right(); pg.wait_for_timeout(900); shot('p26-task-continue')    # slide-25
    right(); pg.wait_for_timeout(900); shot('p27-task-break')       # slide-26
    right(); pg.wait_for_timeout(900); shot('p28-summary')          # slide-27 S 总结
    print('final slide:', cur_slide())

    # ---- 3. 编辑模式冒烟：E 进入 → 全部内容可见；Esc 退出 ----
    pg.keyboard.press('e'); pg.wait_for_timeout(600)
    editing = pg.evaluate("document.body.classList.contains('deck-edit-mode')")
    hidden = pg.evaluate(
        "[...document.querySelectorAll('.slide.visible .rvi, .slide.visible .rvi-pop')]"
        ".filter(e => getComputedStyle(e).opacity !== '1').length")
    pg.keyboard.press('Escape'); pg.wait_for_timeout(400)
    exited = pg.evaluate("!document.body.classList.contains('deck-edit-mode')")
    print(f'edit mode: entered={editing} hidden_while_editing={hidden} exited={exited}')

    b.close()

print('console errors:', errors if errors else 'NONE')
sys.exit(1 if (errors or bad) else 0)
