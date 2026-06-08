(function () {
  const graphEl = document.getElementById('relations-graph');
  const panelEl = document.querySelector('[data-relation-panel]');
  const summaryEl = document.querySelector('[data-relations-summary]');
  const legendEl = document.querySelector('[data-relations-legend]');
  const searchInput = document.querySelector('[data-relation-search]');
  const layoutSelect = document.querySelector('[data-relation-layout]');
  const fitButton = document.querySelector('[data-relation-fit]');
  const applyLayoutButton = document.querySelector('[data-layout-apply]');
  const isolatedToggle = document.querySelector('[data-isolated-toggle]');
  const legendToggle = document.querySelector('[data-legend-toggle]');
  const settingsWrap = document.querySelector('.relations-settings');
  const settingsToggle = document.querySelector('[data-relation-settings-toggle]');
  const layoutParamInputs = Array.from(document.querySelectorAll('[data-layout-param]'));
  const edgeToggles = Array.from(document.querySelectorAll('[data-edge-toggle]'));

  if (!graphEl) return;

  graphEl.addEventListener('wheel', (event) => {
    event.preventDefault();
  }, { passive: false });

  const url = new URL(window.location.href);
  const focusId = url.searchParams.get('oj') && url.searchParams.get('pid')
    ? `${url.searchParams.get('oj')}/${url.searchParams.get('pid')}`
    : '';
  const initialEdges = parseEdges(url.searchParams.get('edges'));
  const settingsStorageKey = 'rbook.relations.settings';
  const layoutDefaults = {
    wheelSensitivity: 0.8,
    idealEdgeLength: 155,
    nodeRepulsion: 12000,
    componentSpacing: 120,
    gravity: 0.12,
    spacingFactor: 1.85,
    showLegend: true,
  };
  const layoutSettings = readLayoutSettings();
  const state = {
    activeId: '',
    hoverId: '',
    searchText: '',
    showPre: initialEdges.has('pre'),
    showCommon: initialEdges.has('common'),
    showIsolated: url.searchParams.get('isolated') === '1',
    showLegend: layoutSettings.showLegend,
    layout: url.searchParams.get('layout') || 'cose',
  };
  let graphData = null;
  let cy = null;
  let lastLayoutSignature = '';

  function parseEdges(raw) {
    if (!raw) return new Set(['pre', 'common']);
    if (raw === 'none') return new Set();
    return new Set(raw.split(',').filter(Boolean));
  }

  function readLayoutSettings() {
    try {
      const raw = window.localStorage.getItem(settingsStorageKey);
      if (!raw) return { ...layoutDefaults };
      return normalizeLayoutSettings(JSON.parse(raw));
    } catch (error) {
      return { ...layoutDefaults };
    }
  }

  function normalizeLayoutSettings(settings) {
    const next = { ...layoutDefaults };
    for (const key of Object.keys(layoutDefaults)) {
      if (key === 'showLegend') {
        next[key] = typeof settings?.[key] === 'boolean' ? settings[key] : layoutDefaults[key];
        continue;
      }

      const value = Number(settings?.[key]);
      next[key] = Number.isFinite(value) ? value : layoutDefaults[key];
    }
    return next;
  }

  function saveLayoutSettings() {
    try {
      window.localStorage.setItem(settingsStorageKey, JSON.stringify(layoutSettings));
    } catch (error) {
      // Ignore storage failures; controls should still work for this session.
    }
  }

  function formatLayoutValue(key, value) {
    if (key === 'gravity' || key === 'spacingFactor') return Number(value).toFixed(2);
    if (key === 'wheelSensitivity') return Number(value).toFixed(1);
    return String(Math.round(Number(value)));
  }

  function escapeHtml(value) {
    return String(value || '')
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
  }

  function updateUrl() {
    const next = new URL(window.location.href);
    const edges = [];
    if (state.showPre) edges.push('pre');
    if (state.showCommon) edges.push('common');
    next.searchParams.set('edges', edges.length ? edges.join(',') : 'none');
    next.searchParams.set('layout', state.layout);

    if (state.showIsolated) {
      next.searchParams.set('isolated', '1');
    } else {
      next.searchParams.delete('isolated');
    }

    if (state.activeId) {
      const node = graphData.nodesById.get(state.activeId);
      next.searchParams.set('oj', node.oj);
      next.searchParams.set('pid', node.problem_id);
    } else {
      next.searchParams.delete('oj');
      next.searchParams.delete('pid');
    }

    window.history.replaceState({}, '', next);
  }

  function buildElements(data) {
    return [
      ...data.nodes.map((node) => ({
        group: 'nodes',
        data: node,
        classes: node.isolated ? 'is-isolated' : '',
      })),
      ...data.edges.map((edge) => ({
        group: 'edges',
        data: edge,
        classes: edge.type,
      })),
    ];
  }

  function getLayoutParamKeys(name) {
    if (name === 'breadthfirst') return ['spacingFactor'];
    if (name === 'circle') return [];
    return ['idealEdgeLength', 'nodeRepulsion', 'componentSpacing', 'gravity'];
  }

  function getLayoutSignature() {
    if (!cy) return '';
    const visibleNodes = cy.nodes(':visible').map((node) => node.id()).sort();
    const visibleEdges = cy.edges(':visible').map((edge) => edge.id()).sort();
    const params = getLayoutParamKeys(state.layout)
      .map((key) => `${key}:${layoutSettings[key]}`)
      .join('|');

    return [
      state.layout,
      graphEl.clientWidth,
      graphEl.clientHeight,
      params,
      visibleNodes.join(','),
      visibleEdges.join(','),
    ].join('#');
  }

  function getLayoutOptions(name) {
    const boundingBox = {
      x1: 80,
      y1: 80,
      w: Math.max(320, graphEl.clientWidth - 160),
      h: Math.max(320, graphEl.clientHeight - 160),
    };

    if (name === 'breadthfirst') {
      return {
        name,
        directed: true,
        circle: false,
        grid: false,
        avoidOverlap: true,
        spacingFactor: layoutSettings.spacingFactor,
        animate: true,
        animationDuration: 350,
        fit: false,
        padding: 48,
        boundingBox,
      };
    }

    if (name === 'circle') {
      return {
        name,
        animate: true,
        animationDuration: 350,
        fit: false,
        padding: 48,
        boundingBox,
      };
    }

    return {
      name: 'cose',
      animate: true,
      animationDuration: 450,
      fit: false,
      padding: 48,
      boundingBox,
      idealEdgeLength: layoutSettings.idealEdgeLength,
      nodeRepulsion: layoutSettings.nodeRepulsion,
      nodeOverlap: 24,
      componentSpacing: layoutSettings.componentSpacing,
      gravity: layoutSettings.gravity,
      numIter: 1200,
    };
  }

  function fitVisibleElements() {
    if (!cy) return;
    cy.fit(cy.elements(':visible'), 48);
  }

  function runLayout(fit, force) {
    if (!cy) return;
    const signature = getLayoutSignature();
    if (!force && signature === lastLayoutSignature) {
      if (fit) fitVisibleElements();
      return;
    }

    lastLayoutSignature = signature;
    const layout = cy.elements(':visible').layout(getLayoutOptions(state.layout));
    if (fit) {
      if (typeof layout.one === 'function') {
        layout.one('layoutstop', fitVisibleElements);
      } else if (typeof layout.on === 'function') {
        const onStop = () => {
          if (typeof layout.off === 'function') {
            layout.off('layoutstop', onStop);
          }
          fitVisibleElements();
        };
        layout.on('layoutstop', onStop);
      } else if (typeof cy.one === 'function') {
        cy.one('layoutstop', fitVisibleElements);
      } else {
        window.requestAnimationFrame(fitVisibleElements);
      }
    }
    layout.run();
  }

  function applyFilters() {
    if (!cy) return;

    cy.elements().removeClass('is-hidden');
    if (!state.showPre) {
      cy.edges('[type = "pre"]').addClass('is-hidden');
    }
    if (!state.showCommon) {
      cy.edges('[type = "common"]').addClass('is-hidden');
    }
    if (!state.showIsolated) {
      cy.nodes('.is-isolated').addClass('is-hidden');
    }

    applySearch();
    applyLegendVisibility();
    updateUrl();
  }

  function applyLegendVisibility() {
    if (!legendEl) return;
    legendEl.classList.toggle('is-hidden', !state.showLegend);
  }

  function clearClasses() {
    cy.elements().removeClass('is-faded is-highlighted is-search-match is-search-faded');
  }

  function highlightNeighborhood(id) {
    if (!id || !cy) return;
    clearClasses();

    const node = cy.getElementById(id);
    if (!node || node.empty()) return;

    const neighborhood = node.closedNeighborhood(':visible');
    cy.elements(':visible').difference(neighborhood).addClass('is-faded');
    neighborhood.addClass('is-highlighted');
  }

  function applySearch() {
    if (!cy) return [];

    cy.elements().removeClass('is-search-match is-search-faded');
    const query = state.searchText.trim().toLowerCase();
    if (!query) {
      if (state.activeId) highlightNeighborhood(state.activeId);
      return [];
    }

    const matches = cy.nodes(':visible').filter((node) => {
      const data = node.data();
      return [
        data.oj,
        data.problem_id,
        data.title,
        data.label,
        ...(data.tags || []),
      ].join(' ').toLowerCase().includes(query);
    });

    cy.elements(':visible').addClass('is-search-faded');
    matches.removeClass('is-search-faded').addClass('is-search-match');
    return matches;
  }

  function focusNode(id, showPanel) {
    const node = cy.getElementById(id);
    if (!node || node.empty() || node.hasClass('is-hidden')) return;

    state.activeId = id;
    highlightNeighborhood(id);
    cy.animate({
      center: { eles: node },
      zoom: Math.max(cy.zoom(), 1.25),
      duration: 300,
    });

    if (showPanel) {
      renderPanel(node.data());
    }

    updateUrl();
  }

  function edgeCountsFor(id) {
    const counts = { predecessors: 0, successors: 0, common: 0 };
    for (const edge of graphData.edges) {
      if (edge.type === 'pre' && edge.target === id) counts.predecessors += 1;
      if (edge.type === 'pre' && edge.source === id) counts.successors += 1;
      if (edge.type === 'common' && (edge.source === id || edge.target === id)) counts.common += 1;
    }
    return counts;
  }

  function renderPanel(node) {
    const counts = edgeCountsFor(node.id);
    const tagHtml = node.tags && node.tags.length
      ? node.tags.map((tag) => `<span class="relations-panel-tag">${escapeHtml(tag)}</span>`).join('')
      : '<span class="text-muted">无标签</span>';

    panelEl.innerHTML = `
      <div class="relations-panel-card">
        <div class="relations-panel-kicker">${escapeHtml(node.oj)} ${escapeHtml(node.problem_id)}</div>
        <h2>${escapeHtml(node.title || node.label)}</h2>
        <div class="relations-panel-tags">${tagHtml}</div>
        <dl class="relations-panel-stats">
          <div><dt>前置</dt><dd>${counts.predecessors}</dd></div>
          <div><dt>后置</dt><dd>${counts.successors}</dd></div>
          <div><dt>相似</dt><dd>${counts.common}</dd></div>
        </dl>
        <a class="btn btn-primary btn-sm" href="${escapeHtml(node.url)}">打开题解</a>
      </div>
    `;
  }

  function clearSelection() {
    state.activeId = '';
    clearClasses();
    panelEl.innerHTML = '<div class="relations-panel-empty">选择一个题目节点查看关系。</div>';
    updateUrl();
  }

  function renderSummary(data) {
    summaryEl.textContent = [
      `${data.summary.relationNodes} 个关系节点`,
      `${data.summary.isolatedNodes} 个孤立题目`,
      `${data.summary.preEdges} 条 pre`,
      `${data.summary.commonEdges} 条 common`,
    ].join(' / ');
  }

  function renderLegend(data) {
    const topTags = data.tagStats.slice(0, 12);
    legendEl.innerHTML = [
      '<div class="relations-legend-header">',
      '<div class="relations-legend-title">主要标签</div>',
      '<button class="relations-legend-hide" type="button" data-legend-hide title="隐藏主要标签" aria-label="隐藏主要标签">隐藏</button>',
      '</div>',
      '<div class="relations-legend-list">',
      ...topTags.map((item) => `
        <span class="relations-legend-item">
          <span class="relations-legend-swatch" style="background:${escapeHtml(item.color)}"></span>
          ${escapeHtml(item.tag)} <span class="relations-legend-count">${item.count}</span>
        </span>
      `),
      '</div>',
    ].join('');
  }

  function bindControls() {
    settingsToggle?.addEventListener('click', () => {
      const isOpen = settingsWrap.classList.toggle('is-open');
      settingsToggle.setAttribute('aria-expanded', String(isOpen));
    });

    for (const toggle of edgeToggles) {
      const type = toggle.dataset.edgeToggle;
      toggle.checked = type === 'pre' ? state.showPre : state.showCommon;
      toggle.addEventListener('change', () => {
        if (type === 'pre') state.showPre = toggle.checked;
        if (type === 'common') state.showCommon = toggle.checked;
        applyFilters();
      });
    }

    isolatedToggle.checked = state.showIsolated;
    isolatedToggle.addEventListener('change', () => {
      state.showIsolated = isolatedToggle.checked;
      applyFilters();
      runLayout(true);
    });

    layoutSelect.value = state.layout;
    layoutSelect.addEventListener('change', () => {
      state.layout = layoutSelect.value;
      updateLayoutControlAvailability();
      updateUrl();
      runLayout(true);
    });

    fitButton.addEventListener('click', () => {
      fitVisibleElements();
    });

    applyLayoutButton.addEventListener('click', () => {
      runLayout(true);
    });

    legendToggle.checked = state.showLegend;
    legendToggle.addEventListener('change', () => {
      state.showLegend = legendToggle.checked;
      layoutSettings.showLegend = state.showLegend;
      saveLayoutSettings();
      applyLegendVisibility();
    });

    legendEl?.addEventListener('click', (event) => {
      if (!event.target.closest('[data-legend-hide]')) return;
      state.showLegend = false;
      layoutSettings.showLegend = false;
      if (legendToggle) legendToggle.checked = false;
      saveLayoutSettings();
      applyLegendVisibility();
    });

    for (const input of layoutParamInputs) {
      const key = input.dataset.layoutParam;
      const output = document.querySelector(`[data-layout-output="${key}"]`);
      input.value = layoutSettings[key];
      if (output) output.textContent = formatLayoutValue(key, layoutSettings[key]);

      input.addEventListener('input', () => {
        layoutSettings[key] = Number(input.value);
        if (key === 'wheelSensitivity' && cy?._private?.options) {
          cy._private.options.wheelSensitivity = layoutSettings.wheelSensitivity;
        }
        if (output) output.textContent = formatLayoutValue(key, layoutSettings[key]);
        saveLayoutSettings();
      });
    }
    updateLayoutControlAvailability();

    searchInput.addEventListener('input', () => {
      state.searchText = searchInput.value;
      applySearch();
    });

    searchInput.addEventListener('keydown', (event) => {
      if (event.key !== 'Enter') return;
      const matches = applySearch();
      if (matches.length > 0) {
        focusNode(matches[0].id(), true);
      }
    });
  }

  function updateLayoutControlAvailability() {
    for (const input of layoutParamInputs) {
      const key = input.dataset.layoutParam;
      const isAlwaysUseful = key === 'wheelSensitivity';
      const disabled = !isAlwaysUseful && !getLayoutParamKeys(state.layout).includes(key);
      const slider = input.closest('.relations-slider');

      input.disabled = disabled;
      input.setAttribute('aria-disabled', String(disabled));
      slider?.classList.toggle('is-disabled', disabled);
      if (slider) {
        slider.title = disabled ? '当前布局不使用这个参数' : '';
      }
    }
  }

  function initGraph(data) {
    graphData = {
      ...data,
      nodesById: new Map(data.nodes.map((node) => [node.id, node])),
    };

    const focusedNode = focusId ? graphData.nodesById.get(focusId) : null;
    if (focusedNode?.isolated) {
      state.showIsolated = true;
    }

    cy = cytoscape({
      container: graphEl,
      elements: buildElements(data),
      minZoom: 0.15,
      maxZoom: 3,
      wheelSensitivity: layoutSettings.wheelSensitivity,
      style: [
        {
          selector: 'node',
          style: {
            label: 'data(label)',
            'background-color': 'data(color)',
            color: '#1f2937',
            'font-size': 10,
            'text-valign': 'bottom',
            'text-halign': 'center',
            'text-margin-y': 5,
            width: 24,
            height: 24,
            'border-width': 2,
            'border-color': '#ffffff',
            'overlay-opacity': 0,
          },
        },
        {
          selector: 'edge',
          style: {
            width: 1.5,
            'curve-style': 'bezier',
            'line-color': '#94a3b8',
            'target-arrow-color': '#94a3b8',
            'target-arrow-shape': 'none',
            opacity: 0.78,
          },
        },
        {
          selector: 'edge.pre',
          style: {
            'line-color': '#2563eb',
            'target-arrow-color': '#2563eb',
            'target-arrow-shape': 'triangle',
          },
        },
        {
          selector: 'edge.common',
          style: {
            'line-color': '#16a34a',
            'line-style': 'dashed',
          },
        },
        {
          selector: '.is-highlighted',
          style: {
            opacity: 1,
            'z-index': 20,
            'border-color': '#111827',
            width: 34,
            height: 34,
          },
        },
        {
          selector: 'edge.is-highlighted',
          style: {
            width: 3,
          },
        },
        {
          selector: '.is-faded',
          style: {
            opacity: 0.12,
          },
        },
        {
          selector: '.is-search-match',
          style: {
            'border-color': '#f59e0b',
            'border-width': 4,
            width: 36,
            height: 36,
            opacity: 1,
            'z-index': 30,
          },
        },
        {
          selector: '.is-search-faded',
          style: {
            opacity: 0.1,
          },
        },
        {
          selector: '.is-hidden',
          style: {
            display: 'none',
          },
        },
      ],
    });

    cy.on('mouseover', 'node', (event) => {
      state.hoverId = event.target.id();
      highlightNeighborhood(state.hoverId);
    });

    cy.on('mouseout', 'node', () => {
      state.hoverId = '';
      if (state.activeId) {
        highlightNeighborhood(state.activeId);
      } else if (state.searchText.trim()) {
        applySearch();
      } else {
        clearClasses();
      }
    });

    cy.on('tap', 'node', (event) => {
      focusNode(event.target.id(), true);
    });

    cy.on('dbltap', 'node', (event) => {
      window.location.href = event.target.data('url');
    });

    cy.on('tap', (event) => {
      if (event.target === cy) {
        clearSelection();
      }
    });

    bindControls();
    applyFilters();
    renderSummary(data);
    renderLegend(data);
    runLayout(true, true);

    if (focusId && graphData.nodesById.has(focusId)) {
      window.setTimeout(() => focusNode(focusId, true), 500);
    }
  }

  if (typeof cytoscape === 'undefined') {
    graphEl.textContent = 'Cytoscape.js 加载失败。';
    return;
  }

  fetch('/api/relations')
    .then((response) => {
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      return response.json();
    })
    .then(initGraph)
    .catch((error) => {
      graphEl.textContent = `关系图加载失败：${error.message}`;
      if (summaryEl) summaryEl.textContent = '加载失败';
    });
}());
