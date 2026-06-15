import type { GraphSettings, LayoutMode } from './types';
import { layoutSupports } from './settings';

interface ToolbarProps {
  settings: GraphSettings;
  query: string;
  summaryText: string;
  onSettingsChange: (patch: Partial<GraphSettings>) => void;
  onQueryChange: (query: string) => void;
  onApplyLayout: () => void;
  onFit: () => void;
}

const layoutLabels: Record<LayoutMode, string> = {
  learning: '学习路径',
  explore: '探索',
  circle: '环形',
};

export function Toolbar({
  settings,
  query,
  summaryText,
  onSettingsChange,
  onQueryChange,
  onApplyLayout,
  onFit,
}: ToolbarProps) {
  return (
    <div className="graph-settings">
      <details className="graph-settings-popover">
        <summary className="graph-settings-toggle" title="设置" aria-label="设置">
          <span aria-hidden="true">⚙</span>
        </summary>
        <section className="graph-toolbar" aria-label="关系图设置">
          <header className="graph-toolbar-header">
            <div>
              <strong>题目关系图</strong>
              <p>{summaryText}</p>
            </div>
            <a href="/" className="graph-toolbar-home">首页</a>
          </header>

          <div className="graph-toolbar-row">
            <label className="graph-search">
              <span className="visually-hidden">搜索题目</span>
              <input
                type="search"
                value={query}
                placeholder="搜索 OJ / 题号 / 标题 / tag"
                onChange={(event) => onQueryChange(event.target.value)}
              />
            </label>
            <label className="graph-select">
              <span className="visually-hidden">布局</span>
              <select
                value={settings.layout}
                onChange={(event) => onSettingsChange({ layout: event.target.value as LayoutMode })}
              >
                {Object.entries(layoutLabels).map(([value, label]) => (
                  <option key={value} value={value}>{label}</option>
                ))}
              </select>
            </label>
          </div>

          <div className="graph-toggle-row">
            <Toggle checked={settings.showPre} label="pre 边" onChange={(showPre) => onSettingsChange({ showPre })} />
            <Toggle checked={settings.showCommon} label="common 边" onChange={(showCommon) => onSettingsChange({ showCommon })} />
            <Toggle checked={settings.showIsolated} label="孤立题目" onChange={(showIsolated) => onSettingsChange({ showIsolated })} />
            <Toggle checked={settings.showLegend} label="主要标签" onChange={(showLegend) => onSettingsChange({ showLegend })} />
          </div>

          <div className="graph-slider-grid">
            <Slider
              label="滚轮缩放速度"
              value={settings.wheelSensitivity}
              min={0.1}
              max={1.5}
              step={0.1}
              enabled={layoutSupports(settings.layout, 'wheelSensitivity')}
              onChange={(wheelSensitivity) => onSettingsChange({ wheelSensitivity })}
            />
            <Slider
              label="关系边长"
              value={settings.edgeLength}
              min={80}
              max={320}
              step={10}
              enabled={layoutSupports(settings.layout, 'edgeLength')}
              onChange={(edgeLength) => onSettingsChange({ edgeLength })}
            />
            <Slider
              label="节点间距"
              value={settings.nodeSpacing}
              min={48}
              max={180}
              step={4}
              enabled={layoutSupports(settings.layout, 'nodeSpacing')}
              onChange={(nodeSpacing) => onSettingsChange({ nodeSpacing })}
            />
            <Slider
              label="层级间距"
              value={settings.layerSpacingRatio}
              min={0.5}
              max={1.5}
              step={0.05}
              enabled={layoutSupports(settings.layout, 'layerSpacingRatio')}
              onChange={(layerSpacingRatio) => onSettingsChange({ layerSpacingRatio })}
            />
            <Slider
              label="探索斥力"
              value={settings.forceStrength}
              min={200}
              max={1800}
              step={50}
              enabled={layoutSupports(settings.layout, 'forceStrength')}
              onChange={(forceStrength) => onSettingsChange({ forceStrength })}
            />
          </div>

          <div className="graph-toolbar-actions">
            <button type="button" onClick={onApplyLayout}>应用布局</button>
            <button type="button" onClick={onFit}>适应视图</button>
          </div>
        </section>
      </details>
    </div>
  );
}

function Toggle({ checked, label, onChange }: { checked: boolean; label: string; onChange: (value: boolean) => void }) {
  return (
    <label className="graph-toggle">
      <input type="checkbox" checked={checked} onChange={(event) => onChange(event.target.checked)} />
      <span>{label}</span>
    </label>
  );
}

function Slider({
  label,
  value,
  min,
  max,
  step,
  enabled,
  onChange,
}: {
  label: string;
  value: number;
  min: number;
  max: number;
  step: number;
  enabled: boolean;
  onChange: (value: number) => void;
}) {
  return (
    <label className={`graph-slider ${enabled ? '' : 'is-disabled'}`}>
      <span>{label}</span>
      <output>{Number.isInteger(value) ? value : value.toFixed(2)}</output>
      <input
        type="range"
        value={value}
        min={min}
        max={max}
        step={step}
        disabled={!enabled}
        onChange={(event) => onChange(Number(event.target.value))}
      />
    </label>
  );
}
