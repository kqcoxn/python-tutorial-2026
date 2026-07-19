<script>
/* === SECTION: 课件专属交互（data-reveal 点击揭示 + data-step 分步揭示 StepManager） ===
   模型：非 data-step 元素翻页到位后按 --d 自动播放入场动画（.slide.visible 驱动）；
   仅带 data-step 的元素保持隐藏，由 StepManager 按 →/Space/点击/滚轮揭示。
   步状态为瞬态：不进历史栈、不进 localStorage、不进导出（运行时 sanitize 已剥离）。
   slide 列表查询一律限定在 .slides-offset 内，防止选中 Pages 侧栏的克隆节点。 */
(function () {
  'use strict';

  function reducedMotion() {
    return window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  }

  /* ---- 1. data-reveal 点击揭示：演示模式专属，编辑模式禁用；与分步互不干扰 ---- */
  document.addEventListener('click', function (e) {
    if (document.body.classList.contains('deck-edit-mode')) return;
    var t = e.target && e.target.closest ? e.target.closest('[data-reveal]') : null;
    if (!t) return;
    t.classList.toggle('revealed');
  });

  /* ---- 2. StepManager（opt-in）：扫描 [data-step]，同属性值为一组，DOM 顺序成步 ---- */
  var StepManager = {
    current: null,   /* 当前页 section.slide */
    steps: [],       /* [[key, [els...]], ...] 按 DOM 顺序 */
    shown: 0,        /* 已揭示步数 */
    intent: 'next',  /* 下一次页面激活的初态：'next' = 0 步；其余 = 全部步 */
    _intentT: null,

    activate: function (slide, showAll) {
      this.current = slide;
      this.steps = this.scan(slide);
      this.shown = showAll ? this.steps.length : 0;
      slide.classList.toggle('steps-instant', !!showAll);
      this.apply();
    },
    scan: function (slide) {
      var map = new Map();
      var seq = 0;
      var els = slide.querySelectorAll('[data-step]');
      for (var i = 0; i < els.length; i++) {
        var k = els[i].getAttribute('data-step');
        if (!k) k = '__bare' + seq++; /* 裸 data-step：每个元素独立成步 */
        if (!map.has(k)) map.set(k, []);
        map.get(k).push(els[i]);
      }
      return Array.from(map.entries());
    },
    apply: function () {
      var shownKeys = {};
      for (var i = 0; i < this.steps.length; i++) {
        var on = i < this.shown;
        shownKeys[this.steps[i][0]] = on;
        for (var j = 0; j < this.steps[i][1].length; j++) {
          this.steps[i][1][j].classList.toggle('step-shown', on);
        }
      }
      /* data-flash-with 元素（代码段高亮）跟随同名步的可见性 */
      if (this.current) {
        var flash = this.current.querySelectorAll('[data-flash-with]');
        for (var f = 0; f < flash.length; f++) {
          flash[f].classList.toggle('seg-now', !!shownKeys[flash[f].getAttribute('data-flash-with')]);
        }
      }
    },
    _expireIntent: function () {
      var self = this;
      clearTimeout(this._intentT);
      this._intentT = setTimeout(function () { self.intent = 'jump'; }, 900);
    },
    next: function () {
      if (!this.current) return false;
      if (this.shown < this.steps.length) {
        this.shown += 1;
        this.apply();
        return true;
      }
      this.intent = 'next'; /* 即将前进翻页：下一页 data-step 从 0 步开始 */
      this._expireIntent();
      return false;
    },
    prev: function () {
      if (!this.current) return false;
      if (this.shown > 0) {
        this.shown -= 1;
        this.apply();
        return true;
      }
      this.intent = 'prev'; /* 即将后退翻页：上一页直接显示全部步 */
      this._expireIntent();
      return false;
    }
  };

  /* 运行时统一 next/prev 入口（键盘 ←/→/Space/PgUp/PgDn 与滚轮）在翻页前先询问这里。
     仅当前页还有未揭示的 data-step 步时才拦截。编辑模式 / 减弱动效下停用。 */
  window.__deckStepNav = function (dir) {
    if (document.body.classList.contains('deck-edit-mode')) return false;
    if (reducedMotion()) return false;
    return dir === 'prev' ? StepManager.prev() : StepManager.next();
  };

  /* ---- 3. 页面激活：非 data-step 动画重播（.visible 驱动）+ data-step 初态 ----
     前进进入 → 0 步；后退 / 圆点 / 缩略图跳转 → 全部步终态。 */
  var activeSlide = null;
  var obs = new IntersectionObserver(function (entries) {
    entries.forEach(function (en) {
      if (!en.isIntersecting || en.intersectionRatio < 0.55) return;
      var slide = en.target;
      if (slide === activeSlide) return;
      activeSlide = slide;
      var root = slide.closest('.slides-offset');
      if (root) {
        root.querySelectorAll(':scope > section.slide').forEach(function (s) {
          if (s !== slide) s.classList.remove('visible');
        });
        slide.classList.remove('visible');
        void slide.offsetWidth; /* 强制回流，重播自动入场动画 */
        slide.classList.add('visible');
      }
      if (reducedMotion()) return;
      if (document.body.classList.contains('deck-edit-mode')) return;
      var showAll = StepManager.intent !== 'next';
      StepManager.intent = 'jump';
      StepManager.activate(slide, showAll);
    });
  }, { threshold: [0.55] });
  document.querySelectorAll('.slides-offset > section.slide').forEach(function (s) { obs.observe(s); });

  /* ---- 4. 演示模式点击页面任意处也尝试前进一步（无步可揭示时不翻页、不动作；
        reveal 卡与运行时 chrome 除外） ---- */
  document.addEventListener('click', function (e) {
    if (document.body.classList.contains('deck-edit-mode')) return;
    if (reducedMotion()) return;
    var t = e.target;
    if (!t || !t.closest) return;
    if (t.closest('[data-reveal]')) return;
    if (t.closest('#deckLeftHover, #navDots, .slide-sidebar, #rteToolbar, #deckAddElementMenu, .progress-bar, .deck-edit-chrome')) return;
    if (!t.closest('.slides-offset > section.slide')) return;
    window.__deckStepNav('next');
  });

  /* ---- 5. 编辑模式进出：退出后当前页按"跳转"语义恢复（全部步终态可见） ---- */
  var wasEditing = false;
  new MutationObserver(function () {
    var editing = document.body.classList.contains('deck-edit-mode');
    if (editing) { wasEditing = true; return; }
    if (!wasEditing) return;
    wasEditing = false;
    if (activeSlide && !reducedMotion()) {
      StepManager.intent = 'jump';
      StepManager.activate(activeSlide, true);
    }
  }).observe(document.body, { attributes: true, attributeFilter: ['class'] });
})();
</script>
