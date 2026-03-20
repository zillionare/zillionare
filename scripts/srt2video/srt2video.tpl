<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <link id="animatecss" rel="stylesheet" href="{animate_url}">
  <style>
    {font_face_css}
    html, body {{
      margin: 0;
      padding: 0;
      width: 100%;
      height: 100%;
      overflow: hidden;
      {background_css}
      font-family: {font_family_custom} -apple-system, BlinkMacSystemFont, "PingFang SC", "Hiragino Sans GB", "Noto Sans CJK SC", "Microsoft YaHei", Arial, sans-serif;
    }}
    #viewport {{
      position: fixed;
      left: 0;
      top: 0;
      width: 100vw;
      height: 100vh;
      overflow: auto;
      display: flex;
      justify-content: center;
      align-items: center;
      {background_css}
    }}
    #stage {{
      position: relative;
      width: {canvas_w}px;
      height: {canvas_h}px;
      overflow: hidden;
      flex-shrink: 0;
    }}
    @keyframes profileBlink {{
      0%, 100% {{
        opacity: 1;
      }}
      50% {{
        opacity: 0.5;
      }}
    }}
    #profile {{
      position: absolute;
      left: {profile_x}px;
      top: {profile_y}px;
      width: {profile_w}px;
      height: auto;
      z-index: 1;
      border-radius: 18px;
      transform: translateZ(0);
      backface-visibility: hidden;
      image-rendering: -webkit-optimize-contrast;
      {profile_animation_css_applied}
    }}

    /* Instructor Header Styles */
    .instructor-header {{
      position: absolute;
      top: 8%;
      left: 0;
      width: 100%;
      display: flex;
      flex-direction: column;
      align-items: center;
      z-index: 5;
      color: white;
      text-align: center;
      transform: scale(0.8);
      transform-origin: top center;
      {instructor_header_animation_css}
    }}
    .instructor-title {{
      font-size: 8vw;
      font-weight: 900;
      margin-bottom: 5px;
      letter-spacing: 2px;
      text-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }}
    .instructor-subtitle {{
      font-size: 4.2vw;
      color: rgba(255, 255, 255, 0.85);
      margin-bottom: 30px;
      letter-spacing: 1px;
    }}
    .instructor-profiles {{
      display: flex;
      gap: 40px;
      justify-content: center;
    }}
    .instructor-avatar-wrapper {{
      position: relative;
      width: 28vw;
      height: 28vw;
      border-radius: 50%;
      overflow: hidden;
      box-shadow: 0 8px 25px rgba(0,0,0,0.4);
      background: #eee;
    }}
    .instructor-avatar {{
      width: 100%;
      height: 100%;
      object-fit: cover;
      image-rendering: -webkit-optimize-contrast;
    }}

    @keyframes subZoomIn {{
      0% {{ transform: scale(0.6); opacity: 0; }}
      100% {{ transform: scale(1); opacity: 1; }}
    }}
    @keyframes subZoomOutIn {{
      0% {{ transform: scale(1.35); opacity: 0; }}
      100% {{ transform: scale(1); opacity: 1; }}
    }}
    @keyframes subRotateInLeft {{
      0% {{ transform: translateX(-60px) rotate(-12deg); opacity: 0; }}
      100% {{ transform: translateX(0) rotate(0); opacity: 1; }}
    }}
    @keyframes subRotateInRight {{
      0% {{ transform: translateX(60px) rotate(12deg); opacity: 0; }}
      100% {{ transform: translateX(0) rotate(0); opacity: 1; }}
    }}
    @keyframes subFlipIn {{
      0% {{ transform: perspective(800px) rotateY(80deg); opacity: 0; }}
      100% {{ transform: perspective(800px) rotateY(0deg); opacity: 1; }}
    }}
    @keyframes subExit {{
      0% {{ opacity: 1; transform: translateY(0) scale(1); }}
      100% {{ opacity: 0; transform: translateY(10px) scale(0.98); }}
    }}

    .enter-zoom-in {{ animation: subZoomIn var(--dur) ease-out both; }}
    .enter-zoom-out {{ animation: subZoomOutIn var(--dur) ease-out both; }}
    .enter-rotate-left {{ animation: subRotateInLeft var(--dur) ease-out both; }}
    .enter-rotate-right {{ animation: subRotateInRight var(--dur) ease-out both; }}
    .enter-flip {{ animation: subFlipIn var(--dur) ease-out both; }}
    .exit-default {{ animation: subExit 420ms ease-in both; }}

    .subtitle {{
      position: absolute;
      padding: 10px 15px;
      box-sizing: border-box;
      line-height: 1.2;
      color: #ffffff;
      text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8), -1px -1px 0 rgba(0, 0, 0, 0.5);
      white-space: nowrap;
      overflow: visible;
      z-index: 2;
      --dur: {animation_duration_ms}ms;
      transition: top 400ms cubic-bezier(0.215, 0.61, 0.355, 1);
    }}
    #measure {{
      position: absolute;
      left: -99999px;
      top: -99999px;
      visibility: hidden;
      width: {measure_width}px;
    }}

    #closing-screen {{
      position: absolute;
      left: 0;
      top: 0;
      width: 100%;
      height: 100%;
      display: none; /* 初始隐藏 */
      flex-direction: column;
      justify-content: center;
      align-items: center;
      z-index: 1000;
      {background_css}
    }}
    #closing-logo {{
      width: 20%;
      height: auto;
      margin-bottom: 30px;
      border-radius: 50%; /* 圆角处理 */
    }}
    .search-box {{
      display: flex;
      align-items: center;
      background: white;
      border-radius: 50px;
      padding: 10px 35px;
      box-shadow: 0 4px 20px rgba(0,0,0,0.15);
      border: 1px solid #eee;
    }}
    .wechat-icon {{
      width: 6vw;
      height: 6vw;
      margin-right: 15px;
      color: #07c160; /* 微信绿 */
    }}
    .search-text {{
      font-size: 5vw;
      font-weight: bold;
      color: #333;
      margin-right: 20px;
      letter-spacing: 1px;
    }}
    .search-icon {{
      width: 5vw;
      height: 5vw;
      color: #ffcc00;
    }}
    .search-footer {{
      margin-top: 15px;
      font-size: 3.5vw;
      color: #a0a0a0;
      letter-spacing: 1px;
      font-weight: 500;
    }}
  </style>
</head>
<body>
  <div id="viewport">
    <div id="stage">
      {profile_img_tag}
      
      {instructor_header_html}

      <div id="measure"></div>
      <div id="closing-screen">
        <img id="closing-logo" src="{logo_url_safe}" />
        <div class="search-box">
          <div class="search-text">Quantide</div>
          <svg class="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="11" cy="11" r="8"></circle>
            <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
          </svg>
        </div>
        <div class="search-footer">点个关注不迷路</div>
      </div>
    </div>
  </div>
  <script type="application/json" id="payload">{payload_json}</script>
  <script>
    (() => {{
      const pageLoadStartTime = performance.now();
      const payload = JSON.parse(document.getElementById('payload').textContent);
      const viewport = document.getElementById('viewport');
      const stage = document.getElementById('stage');
      const measure = document.getElementById('measure');
      const profileRect = payload.profile.rect;
      const W = payload.canvas.w;
      const H = payload.canvas.h;
      const margin = Math.max(16, Math.floor(Math.min(W, H) * 0.02));
      const maxActive = 5;
      const subtitles = payload.subtitles || [];
      const animationDurationMs = payload.animationDurationMs || 600;
      const randomColorEnabled = !!payload.randomColor;
      const colorPool = Array.isArray(payload.colors) && payload.colors.length ? payload.colors : [];
      const animationTypes = Array.isArray(payload.animationTypes) && payload.animationTypes.length
        ? payload.animationTypes
        : [];
      const yMin = typeof payload.yMin === 'number' ? payload.yMin : 0.0;
      const yMax = typeof payload.yMax === 'number' ? payload.yMax : 1.0;
      const layoutMode = payload.layoutMode || 'random';
      const totalDuration = payload.totalDuration || 0;
      let nextIndex = 0;
      let active = [];
      let running = false;
      let t0 = 0;
      let zCounter = 10;
      
      let animatePool = [];
      let enterPool = [];
      let exitPool = [];

      async function loadAnimateCss() {{
        const link = document.getElementById('animatecss');
        try {{
          // 如果是 data URL，直接处理内容，不再 fetch
          let text;
          if (link.href.startsWith('data:')) {{
            const base64 = link.href.split(',')[1];
            text = atob(base64);
          }} else {{
            // 增加 10 秒超时限制，避免因网络问题无限期等待
            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), 10000);
            
            const resp = await fetch(link.href, {{ signal: controller.signal }});
            clearTimeout(timeoutId);
            text = await resp.text();
          }}
          
          const found = new Set();
          const re = /\.animate__(?:animated|([a-zA-Z0-9]+))/g;
          let m;
          while ((m = re.exec(text)) !== null) {{
            if (m[1]) found.add('animate__' + m[1]);
          }}
          animatePool = Array.from(found);
          exitPool = animatePool.filter(n => (n.toLowerCase().includes('out') || n.toLowerCase().includes('hinge')));
          enterPool = animatePool.filter(n => !(n.toLowerCase().includes('out') || n.toLowerCase().includes('hinge')));
        }} catch (e) {{
          console.error('Failed to load Animate.css:', e);
          // Fallback if fetch fails
          enterPool = ['animate__zoomIn', 'animate__fadeIn', 'animate__backInDown'];
          exitPool = ['animate__zoomOut', 'animate__fadeOut'];
        }}
      }}
      loadAnimateCss();

      window.__animateReady = false;
      window.__animateError = null;
      window.__animateReady = true;

      function mulberry32(seed) {{
        let a = seed >>> 0;
        return function() {{
          a |= 0;
          a = (a + 0x6D2B79F5) | 0;
          let t = Math.imul(a ^ (a >>> 15), 1 | a);
          t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
          return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
        }};
      }}

      const rng = mulberry32(payload.seed || 1);
      const rngColor = mulberry32(((payload.seed || 1) ^ 0x9e3779b9) >>> 0);

      window.__activeSubtitles = () => active;

      function randChoice(arr) {{
        if (!arr || arr.length === 0) return null;
        return arr[Math.floor(rng() * arr.length)];
      }}

      function randomReadableColor() {{
        if (colorPool.length > 0) {{
          const c = randChoice(colorPool);
          return c.startsWith('#') ? c : '#' + c;
        }}
        const h = Math.floor(rngColor() * 360);
        const s = 85;
        const l = 60;
        return 'hsl(' + h + ' ' + s + '% ' + l + '%)';
      }}

      function intersects(a, b) {{
        return !(
          a.x + a.w <= b.x ||
          b.x + b.w <= a.x ||
          a.y + a.h <= b.y ||
          b.y + b.h <= a.y
        );
      }}

      function expandedRect(r, pad) {{
        return {{ x: r.x - pad, y: r.y - pad, w: r.w + pad * 2, h: r.h + pad * 2 }};
      }}

      function measureTextBox(text) {{
        const tmp = document.createElement('div');
        tmp.className = 'subtitle';
        tmp.style.position = 'static';
        tmp.style.left = '';
        tmp.style.top = '';
        tmp.textContent = text;
        measure.appendChild(tmp);
        const rect = {{ width: tmp.offsetWidth, height: tmp.offsetHeight }};
        measure.removeChild(tmp);
        return {{ w: Math.ceil(rect.width), h: Math.ceil(rect.height) }};
      }}

      function pickPosition(boxW, boxH) {{
        const mode = randChoice(['left', 'center', 'right']);
        let x = margin;
        if (mode === 'center') x = (W - boxW) / 2;
        else if (mode === 'right') x = W - boxW - margin;
        
        const yStart = Math.floor(H * yMin);
        const yEnd = Math.floor(H * yMax);
        const safeY0 = Math.max(margin, yStart);
        const safeY1 = Math.max(safeY0, Math.min(H - margin - boxH, yEnd - boxH));
        
        const y = safeY0 + Math.floor(rng() * (safeY1 - safeY0 + 1));
        return {{ x, y, w: boxW, h: boxH, align: mode }};
      }}

      function setAnimation(node, name, onEnd) {{
        if (!name) {{
          if (onEnd) onEnd();
          return;
        }}
        node.style.setProperty('--dur', animationDurationMs + 'ms');
        if (name.startsWith('animate__')) {{
          node.classList.add('animate__animated');
        }}
        node.classList.add(name);
        if (!onEnd) return;
        const handler = (ev) => {{
          if (ev.target !== node) return;
          node.removeEventListener('animationend', handler);
          onEnd();
        }};
        node.addEventListener('animationend', handler);
      }}

      function stripAnimationClasses(node) {{
        // Remove all animate.css classes
        const cls = Array.from(node.classList);
        for (const c of cls) {{
          if (c.startsWith('animate__')) node.classList.remove(c);
        }}
        node.classList.remove('animate__animated');
      }}

      function startExit(item, preferredKind) {{
        if (item.exiting) return;
        item.exiting = true;
        const kind = preferredKind || randChoice(exitPool) || 'animate__fadeOut';
        
        setAnimation(item.node, kind, () => {{
          if (item.node && item.node.parentNode) item.node.parentNode.removeChild(item.node);
          active = active.filter((x) => x !== item);
        }});

        // 安全兜底：如果动画回调没触发，1.5秒后强制清理
        setTimeout(() => {{
          if (item.node && item.node.parentNode) {{
            item.node.parentNode.removeChild(item.node);
            active = active.filter((x) => x !== item);
          }}
        }}, 1500);
      }}

      function clampToViewport(node, item) {{
        const w = node.offsetWidth;
        const h = node.offsetHeight;
        let x = parseFloat(node.style.left || '0');
        let y = parseFloat(node.style.top || '0');
        if (x < margin) x = margin;
        if (x + w > W - margin) x = Math.max(margin, (W - margin) - w);
        if (y < margin) y = margin;
        if (y + h > H - margin) y = Math.max(margin, (H - margin) - h);
        node.style.left = x + 'px';
        node.style.top = y + 'px';
        item.rect = {{ x, y, w, h }};
      }}

      function addSubtitle(s) {{
        const node = document.createElement('div');
        node.className = 'subtitle';
        node.textContent = s.text;
        node.style.zIndex = String(zCounter++);
        if (randomColorEnabled) {{
          node.style.color = randomReadableColor();
        }}
        stage.appendChild(node);

        // 字幕长度处理：20字以内不换行
        const charCount = s.text.length;
        if (charCount <= 20) {{
          node.style.whiteSpace = 'nowrap';
        }} else {{
          node.style.whiteSpace = 'pre-wrap';
          node.style.overflowWrap = 'break-word';
          node.style.width = Math.floor(W * 0.96) + 'px';
        }}

        // 1. 初始字体大小计算：基于屏宽 96% 的保守估算
        // 对于中文，字宽约等于字号，所以 idealFontSize = (W * 0.96) / charCount
        let fs = Math.floor((W * 0.96) / Math.max(1, charCount));
        
        // 限制最大字号为屏宽의 20%，最小为 28px
        fs = Math.max(28, Math.min(fs, Math.floor(W * 0.2)));
        node.style.fontSize = fs + 'px';

        // 2. 动态收缩机制：如果实际宽度溢出，则循环缩小字号
        const maxSafeW = Math.floor(W * 0.98); // 允许的最大安全宽度
        let guard = 0;
        while (node.scrollWidth > maxSafeW && fs > 20 && guard < 20) {{
          fs -= 2;
          node.style.fontSize = fs + 'px';
          guard++;
        }}

        const boxW = node.offsetWidth;
        const boxH = node.offsetHeight;
        
        let rect;
        if (layoutMode === 'scroll_up') {{
          // 向上顶模式：新字幕出现在 yMax 处
          const x = (W - boxW) / 2;
          const y = Math.floor(H * yMax) - boxH - margin;
          rect = {{ x, y, w: boxW, h: boxH, align: 'center' }};
          
          // 将现有的所有 active 字幕向上移动
          const gap = 12; // 字幕间距
          const shift = boxH + gap;
          for (const item of active) {{
            if (!item.exiting) {{
              item.rect.y -= shift;
              item.node.style.top = item.rect.y + 'px';
            }}
          }}
        }} else {{
          rect = pickPosition(boxW, boxH);
        }}
        
        node.style.left = rect.x + 'px';
        node.style.top = rect.y + 'px';
        node.style.textAlign = rect.align;

        const item = {{ node, rect, start: s.start, end: s.end, exiting: false, animating: true }};
        active.push(item);
        
        // 如果是 scroll_up 模式，检查是否达到 5 条，如果是则批量清除前 4 条
        if (layoutMode === 'scroll_up' && active.filter(x => !x.exiting).length >= 5) {{
          const nonExiting = active.filter(x => !x.exiting);
          // 所有的字幕都向同一方向旋转（随机选一个方向，但本批次统一）
          const exitKind = rng() > 0.5 ? 'animate__rotateOutUpLeft' : 'animate__rotateOutUpRight';
          // 倒数第1个是刚加的，所以清除索引 0 到 length-2 的字幕
          for (let i = 0; i < nonExiting.length - 1; i++) {{
            startExit(nonExiting[i], exitKind);
          }}
        }}

        // 初次放置即修正（scroll_up 模式下可能暂时超出 top，但 tick 会持续修正）
        clampToViewport(node, item);

        const finalize = () => {{
          if (!item.animating) return;
          item.animating = false;
          stripAnimationClasses(node);
          node.style.transform = 'none';
          requestAnimationFrame(() => clampToViewport(node, item));
        }};

        const kind = randChoice(animationTypes);
        if (kind === 'typewriter') {{
          node.style.opacity = '1';
          const full = s.text;
          node.textContent = '';
          const duration = Math.max(250, Math.min(animationDurationMs, Math.floor((s.end - s.start) * 1000 * 0.8)));
          const steps = Math.max(2, Math.min(80, full.length));
          const stepMs = Math.max(16, Math.floor(duration / steps));
          let i = 0;
          const timer = setInterval(() => {{
            i += 1;
            const n = Math.floor((i / steps) * full.length);
            node.textContent = full.slice(0, n);
            if (i >= steps) {{
              clearInterval(timer);
              node.textContent = full;
              finalize();
            }} else {{
              clampToViewport(node, item);
            }}
          }}, stepMs);
          return;
        }}

        let cls = '';
        if (!kind) {{
          cls = randChoice(enterPool) || 'enter-zoom-in';
        }} else if (kind.startsWith('animate__')) {{
          cls = kind;
        }} else {{
          cls = {{
            'zoom_in': 'enter-zoom-in',
            'zoom_out': 'enter-zoom-out',
            'rotate_left': 'enter-rotate-left',
            'rotate_right': 'enter-rotate-right',
            'flip': 'enter-flip',
          }}[kind] || 'enter-zoom-in';
        }}

        setAnimation(node, cls, finalize);
        setTimeout(() => {{ if (node.isConnected) finalize(); }}, animationDurationMs + 120);
      }}

      function tick() {{
        if (!running) return;
        const now = performance.now();
        const t = (now - t0) / 1000.0;

        // 检查是否显示结尾联系方式 (最后 1.0 秒)
        if (totalDuration > 0 && t >= totalDuration - 1.0) {{
          const closing = document.getElementById('closing-screen');
          if (closing && closing.style.display !== 'flex') {{
            closing.style.display = 'flex';
            // 隐藏所有正在显示的字幕
            for (const item of active) {{
              if (item.node) item.node.style.display = 'none';
            }}
            // 隐藏 profile
            const profile = document.getElementById('profile');
            if (profile) profile.style.display = 'none';
          }}
        }}

        while (nextIndex < subtitles.length && subtitles[nextIndex].start <= t) {{
          addSubtitle(subtitles[nextIndex]);
          nextIndex += 1;
        }}

        while (active.filter(x => !x.exiting).length > maxActive) {{
          const candidate = active.find((x) => !x.exiting);
          if (!candidate) break;
          startExit(candidate);
        }}

        for (const item of active) {{
          if (!item.exiting && !item.animating) {{
            clampToViewport(item.node, item);
          }}
        }}

        requestAnimationFrame(tick);
      }}

      window.__start = () => {{
        if (running) return performance.now() - pageLoadStartTime;
        
        // 记录启动时刻
        t0 = performance.now();
        running = true;
        
        // 快速验证功能：支持通过 URL 参数 ?skipToEnd=1 或按 'E' 键跳转到结尾前 2 秒
        const urlParams = new URLSearchParams(window.location.search);
        if (urlParams.has('skipToEnd') && totalDuration > 2) {{
          const offsetMs = (totalDuration - 2) * 1000;
          t0 -= offsetMs;
          // 快速定位 nextIndex
          const skipTime = totalDuration - 2;
          while (nextIndex < subtitles.length && subtitles[nextIndex].start < skipTime) {{
            nextIndex++;
          }}
        }}

        requestAnimationFrame(tick);
        // 返回相对于页面加载开始的偏移量，用于 FFmpeg 剪切
        return t0 - pageLoadStartTime;
      }};

      // 监听键盘 'E' 键实现手动跳转
      window.addEventListener('keydown', (e) => {{
        if (e.key.toLowerCase() === 'e' && totalDuration > 2) {{
          const skipTime = totalDuration - 2;
          t0 = performance.now() - (skipTime * 1000);
          // 修正 nextIndex
          nextIndex = 0;
          while (nextIndex < subtitles.length && subtitles[nextIndex].start < skipTime) {{
            nextIndex++;
          }}
          console.log('Skipped to end (2s remaining)');
        }}
      }});

      function autoStart() {{
        if (running) return;
        window.__start();
      }}

      setTimeout(autoStart, 0);
    }})();
  </script>
</body>
</html>
