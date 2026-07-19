<script>
/* === SECTION: 课件专属交互（点击揭示 + 入场动画重播） ===
   独立于可编辑运行时；Reveal 状态不进历史栈、不进导出（导出前由运行时统一剥离 .revealed）。 */
(function () {
  'use strict';

  /* 1. 点击揭示：仅演示模式生效，编辑模式禁用 */
  document.addEventListener('click', function (e) {
    if (document.body.classList.contains('deck-edit-mode')) return;
    var t = e.target && e.target.closest ? e.target.closest('[data-reveal]') : null;
    if (!t) return;
    t.classList.toggle('revealed');
  });

  /* 2. 每次进入页面重播入场动画（翻页即时，不强制看完；再进入时重新播一遍）。
        注意：slide 列表查询必须限定在 .slides-offset 内，防止选中 Pages 侧栏里的克隆节点。 */
  var current = null;
  var obs = new IntersectionObserver(function (entries) {
    entries.forEach(function (en) {
      if (!en.isIntersecting || en.intersectionRatio < 0.55) return;
      var slide = en.target;
      if (slide === current) return;
      current = slide;
      var root = slide.closest('.slides-offset');
      if (!root) return;
      root.querySelectorAll(':scope > section.slide').forEach(function (s) {
        if (s !== slide) s.classList.remove('visible');
      });
      slide.classList.remove('visible');
      void slide.offsetWidth; /* 强制回流，重启 CSS 动画 */
      slide.classList.add('visible');
    });
  }, { threshold: [0.55] });
  document.querySelectorAll('.slides-offset > section.slide').forEach(function (s) {
    obs.observe(s);
  });
})();
</script>
