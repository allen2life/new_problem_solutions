import type { Edge, Node } from '@xyflow/react';

export type RelationType = 'pre' | 'common';
export type LayoutMode = 'learning' | 'explore' | 'circle';

export interface RelationNodeData extends Record<string, unknown> {
  id: string;
  oj: string;
  problem_id: string;
  label: string;
  title: string;
  tags: string[];
  primaryTag: string;
  color: string;
  url: string;
  isolated: boolean;
  difficulty?: string;
  predecessorCount: number;
  successorCount: number;
  commonCount: number;
  isActive: boolean;
  isDimmed: boolean;
  isMatched: boolean;
}

export interface RelationEdgeData extends Record<string, unknown> {
  id: string;
  source: string;
  target: string;
  type: RelationType;
  directed: boolean;
  reason: string;
}

export interface TagStat {
  tag: string;
  count: number;
  color: string;
}

export interface RelationSummary {
  nodes: number;
  edges: number;
  relationNodes: number;
  isolatedNodes: number;
  preEdges: number;
  commonEdges: number;
}

export interface RelationGraphResponse {
  nodes: RelationNodeData[];
  edges: RelationEdgeData[];
  tagStats: TagStat[];
  summary: RelationSummary;
}

export type RelationFlowNode = Node<RelationNodeData, 'problem'>;
export type RelationFlowEdge = Edge<RelationEdgeData>;

export interface LayoutSettings {
  wheelSensitivity: number;
  edgeLength: number;
  nodeSpacing: number;
  layerSpacingRatio: number;
  forceStrength: number;
}

export interface GraphSettings extends LayoutSettings {
  showPre: boolean;
  showCommon: boolean;
  showIsolated: boolean;
  showLegend: boolean;
  layout: LayoutMode;
}
