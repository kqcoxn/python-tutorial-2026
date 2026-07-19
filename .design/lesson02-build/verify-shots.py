# -*- coding: utf-8 -*-
"""第 2 章 slides.html 交付前冒烟：1280×720 逐页走查。
   1) 每页 overflow 检查（页内禁止滚动）  2) 关键页截图  3) 分步揭示 / 点击揭示 / 编辑模式冒烟  4) 控制台错误。"""
import pathlib, sys
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parents[2]
URL = (ROOT / 'lessons' / '02-output-comments-debug' / 'slides.html').as_uri()
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
    shot('p01-cover')                                   # slide-0 封面
    right(); pg.wait_for_timeout(700); shot('p02-recap')          # slide-1
    right(); pg.wait_for_timeout(2200); shot('p03-multi-print')   # slide-2 级联点亮
    right(2); pg.wait_for_timeout(800)                            # slide-4 预测页
    shot('p05-predict-hidden')
    pg.click('.b-revealbar'); pg.wait_for_timeout(500); shot('p05-predict-revealed')
    right(3); pg.wait_for_timeout(800); shot('p08-new-words')     # slide-7
    right(); pg.wait_for_timeout(1100); shot('p09-syntax-a')      # slide-8 仅代码+运行行
    right(); pg.wait_for_timeout(700); shot('p09-syntax-b-error') # step1 报错震动
    right(); pg.wait_for_timeout(900); shot('p09-syntax-c-hint')  # step2 提示+缺口高亮
    right(); pg.wait_for_timeout(900)                             # slide-9 NameError
    right(); pg.wait_for_timeout(600)
    right(); pg.wait_for_timeout(800); shot('p10-nameerror')      # 报错+pritn 高亮
    right(); pg.wait_for_timeout(800)
    right(); pg.wait_for_timeout(700); shot('p11-indentation')    # slide-10 报错+缩进高亮
    right(); pg.wait_for_timeout(800)
    right(); pg.wait_for_timeout(700); shot('p12-zerodiv')        # slide-11
    right(); pg.wait_for_timeout(1000); shot('p13-traceback-a')   # slide-12 仅卡片+规则
    right(); pg.wait_for_timeout(700); shot('p13-traceback-b1')   # ①最后一行
    right(); pg.wait_for_timeout(600)
    right(); pg.wait_for_timeout(800); shot('p13-traceback-c3')   # ③回到代码
    right(); pg.wait_for_timeout(800); shot('p14-debug-flow')     # slide-13
    right(); pg.wait_for_timeout(700); shot('p15-error-queue')    # slide-14
    right(); pg.wait_for_timeout(700); shot('p16-breakpoint')     # slide-15
    right(); pg.wait_for_timeout(700); shot('p17-step-over')      # slide-16
    right(); pg.wait_for_timeout(1000); shot('p18-declaration')   # slide-17 C 宣言
    right(); pg.wait_for_timeout(1000); shot('p19-v1')            # slide-18 V1
    right(); pg.wait_for_timeout(900); shot('p20-chain-hidden')   # slide-19
    pg.locator('.c-revealbar').nth(0).click(); pg.wait_for_timeout(400)
    pg.locator('.c-revealbar').nth(1).click(); pg.wait_for_timeout(500)
    shot('p20-chain-revealed')
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
