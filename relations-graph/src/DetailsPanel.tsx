import type { RelationNodeData } from './types';

interface DetailsPanelProps {
  node: RelationNodeData | null;
}

export function DetailsPanel({ node }: DetailsPanelProps) {
  if (!node) {
    return (
      <aside className="graph-details-panel">
        <div className="graph-details-empty">选择一个题目节点查看关系。</div>
      </aside>
    );
  }

  return (
    <aside className="graph-details-panel">
      <div className="graph-details-kicker">{node.oj} {node.problem_id}</div>
      <h2>{node.title || node.label}</h2>
      <div className="graph-details-tags">
        {node.tags?.length ? node.tags.map((tag) => <span key={tag}>{tag}</span>) : <span className="is-muted">无标签</span>}
      </div>
      <dl className="graph-details-stats">
        <div><dt>前置</dt><dd>{node.predecessorCount}</dd></div>
        <div><dt>后置</dt><dd>{node.successorCount}</dd></div>
        <div><dt>相似</dt><dd>{node.commonCount}</dd></div>
      </dl>
      <a href={node.url} className="graph-details-link">打开题解</a>
    </aside>
  );
}
