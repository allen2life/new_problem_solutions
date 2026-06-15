import type { TagStat } from './types';

export function TagLegend({ tags }: { tags: TagStat[] }) {
  const visibleTags = tags.slice(0, 16);

  return (
    <div className="graph-tag-legend" aria-label="主要标签">
      <strong>主要标签</strong>
      <div>
        {visibleTags.map((item) => (
          <span key={item.tag} className="graph-tag-pill">
            <i style={{ backgroundColor: item.color }} aria-hidden="true" />
            {item.tag}
            <em>{item.count}</em>
          </span>
        ))}
      </div>
    </div>
  );
}
