import { memo } from 'react';
import { Handle, Position, type NodeProps } from '@xyflow/react';
import type { RelationFlowNode } from './types';

const difficultyClassMap: Record<string, string> = {
  '入门': 'difficulty-entry',
  '普及-': 'difficulty-basic',
  '普及/提高-': 'difficulty-intermediate-minus',
  '普及+/提高': 'difficulty-intermediate',
  '提高+/省选-': 'difficulty-advanced-minus',
  '省选/NOI-': 'difficulty-advanced',
  'NOI/NOI+/CTSC': 'difficulty-elite',
  '未知': 'difficulty-unknown',
};

function ProblemNode({ data }: NodeProps<RelationFlowNode>) {
  const tags = data.tags?.slice(0, 3) || [];
  const className = [
    'problem-card-node',
    data.isActive ? 'is-active' : '',
    data.isDimmed ? 'is-dimmed' : '',
    data.isMatched ? 'is-matched' : '',
  ].filter(Boolean).join(' ');

  return (
    <article className={className} style={{ '--node-color': data.color } as React.CSSProperties}>
      <Handle className="problem-node-handle" type="target" position={Position.Left} />
      <Handle className="problem-node-handle" type="source" position={Position.Right} />
      <div className="problem-card-node-top">
        <span className="problem-card-node-id">{data.oj} {data.problem_id}</span>
        <span className={`graph-difficulty-badge ${difficultyClassMap[data.difficulty || '未知'] || 'difficulty-unknown'}`}>
          {data.difficulty || '未知'}
        </span>
      </div>
      <h2 title={data.title || data.label}>{data.title || data.label}</h2>
      <div className="problem-card-node-tags">
        {tags.length > 0 ? tags.map((tag) => <span key={tag}>{tag}</span>) : <span className="is-muted">无标签</span>}
      </div>
      <div className="problem-card-node-stats" aria-label="关系数量">
        <span title="前置题目">前 {data.predecessorCount}</span>
        <span title="后置题目">后 {data.successorCount}</span>
        <span title="相似题目">似 {data.commonCount}</span>
      </div>
    </article>
  );
}

export default memo(ProblemNode);
