import type { GraphSettings, LayoutMode } from './types';

const STORAGE_KEY = 'rbook.relations.xyflow.settings';

export const defaultSettings: GraphSettings = {
  showPre: true,
  showCommon: true,
  showIsolated: false,
  showLegend: true,
  layout: 'learning',
  wheelSensitivity: 0.8,
  edgeLength: 190,
  nodeSpacing: 90,
  layerSpacingRatio: 1,
  forceStrength: 760,
};

export function readSettings(): GraphSettings {
  try {
    const raw = window.localStorage.getItem(STORAGE_KEY);
    if (!raw) return { ...defaultSettings };
    return normalizeSettings(JSON.parse(raw));
  } catch {
    return { ...defaultSettings };
  }
}

export function saveSettings(settings: GraphSettings): void {
  try {
    window.localStorage.setItem(STORAGE_KEY, JSON.stringify(settings));
  } catch {
    // Local storage is optional. The graph still works during this session.
  }
}

export function readInitialUrlState(): { activeId: string; settingsPatch: Partial<GraphSettings> } {
  const url = new URL(window.location.href);
  const oj = url.searchParams.get('oj');
  const pid = url.searchParams.get('pid');
  const edges = parseEdges(url.searchParams.get('edges'));
  const layout = normalizeLayout(url.searchParams.get('layout'));

  return {
    activeId: oj && pid ? `${oj}/${pid}` : '',
    settingsPatch: {
      showPre: edges.has('pre'),
      showCommon: edges.has('common'),
      showIsolated: url.searchParams.get('isolated') === '1',
      ...(layout ? { layout } : {}),
    },
  };
}

export function updateUrlState(activeId: string, settings: GraphSettings): void {
  const next = new URL(window.location.href);
  const edges = [];
  if (settings.showPre) edges.push('pre');
  if (settings.showCommon) edges.push('common');
  next.searchParams.set('edges', edges.length ? edges.join(',') : 'none');
  next.searchParams.set('layout', settings.layout);

  if (settings.showIsolated) {
    next.searchParams.set('isolated', '1');
  } else {
    next.searchParams.delete('isolated');
  }

  if (activeId.includes('/')) {
    const [oj, pid] = activeId.split('/');
    next.searchParams.set('oj', oj);
    next.searchParams.set('pid', pid);
  } else {
    next.searchParams.delete('oj');
    next.searchParams.delete('pid');
  }

  window.history.replaceState({}, '', next);
}

export function layoutSupports(mode: LayoutMode, key: keyof GraphSettings): boolean {
  if (key === 'wheelSensitivity') return true;
  if (mode === 'learning') return ['edgeLength', 'nodeSpacing', 'layerSpacingRatio'].includes(key);
  if (mode === 'explore') return ['edgeLength', 'forceStrength'].includes(key);
  if (mode === 'circle') return ['nodeSpacing'].includes(key);
  return false;
}

function normalizeSettings(value: Partial<GraphSettings>): GraphSettings {
  return {
    showPre: typeof value.showPre === 'boolean' ? value.showPre : defaultSettings.showPre,
    showCommon: typeof value.showCommon === 'boolean' ? value.showCommon : defaultSettings.showCommon,
    showIsolated: typeof value.showIsolated === 'boolean' ? value.showIsolated : defaultSettings.showIsolated,
    showLegend: typeof value.showLegend === 'boolean' ? value.showLegend : defaultSettings.showLegend,
    layout: normalizeLayout(value.layout) || defaultSettings.layout,
    wheelSensitivity: clampNumber(value.wheelSensitivity, 0.1, 1.5, defaultSettings.wheelSensitivity),
    edgeLength: clampNumber(value.edgeLength, 80, 320, defaultSettings.edgeLength),
    nodeSpacing: clampNumber(value.nodeSpacing, 48, 180, defaultSettings.nodeSpacing),
    layerSpacingRatio: clampNumber(value.layerSpacingRatio, 0.5, 1.5, defaultSettings.layerSpacingRatio),
    forceStrength: clampNumber(value.forceStrength, 200, 1800, defaultSettings.forceStrength),
  };
}

function clampNumber(value: unknown, min: number, max: number, fallback: number): number {
  const numeric = Number(value);
  if (!Number.isFinite(numeric)) return fallback;
  return Math.min(max, Math.max(min, numeric));
}

function parseEdges(raw: string | null): Set<'pre' | 'common'> {
  if (!raw) return new Set(['pre', 'common']);
  if (raw === 'none') return new Set();
  return new Set(raw.split(',').filter((item): item is 'pre' | 'common' => item === 'pre' || item === 'common'));
}

function normalizeLayout(value: unknown): LayoutMode | null {
  if (value === 'learning' || value === 'breadthfirst') return 'learning';
  if (value === 'explore' || value === 'cose') return 'explore';
  if (value === 'circle') return 'circle';
  return null;
}
