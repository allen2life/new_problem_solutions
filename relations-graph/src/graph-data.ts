import type {
  RelationEdgeData,
  RelationFlowEdge,
  RelationFlowNode,
  RelationGraphResponse,
  RelationNodeData,
  RelationType,
} from './types';
import { MarkerType } from '@xyflow/react';

export interface GraphFilterState {
  query: string;
  activeId: string;
  hoverId: string;
  showPre: boolean;
  showCommon: boolean;
  showIsolated: boolean;
}

const CARD_WIDTH = 210;
const CARD_HEIGHT = 112;

export function addRelationCounts(data: RelationGraphResponse): RelationGraphResponse {
  const counts = new Map<string, Pick<RelationNodeData, 'predecessorCount' | 'successorCount' | 'commonCount'>>();

  for (const node of data.nodes) {
    counts.set(node.id, {
      predecessorCount: 0,
      successorCount: 0,
      commonCount: 0,
    });
  }

  for (const edge of data.edges) {
    const source = counts.get(edge.source);
    const target = counts.get(edge.target);

    if (edge.type === 'pre') {
      if (source) source.successorCount += 1;
      if (target) target.predecessorCount += 1;
    }

    if (edge.type === 'common') {
      if (source) source.commonCount += 1;
      if (target) target.commonCount += 1;
    }
  }

  return {
    ...data,
    nodes: data.nodes.map((node) => ({
      ...node,
      difficulty: node.difficulty || '未知',
      predecessorCount: counts.get(node.id)?.predecessorCount || 0,
      successorCount: counts.get(node.id)?.successorCount || 0,
      commonCount: counts.get(node.id)?.commonCount || 0,
      isActive: false,
      isDimmed: false,
      isMatched: false,
    })),
  };
}

export function getVisibleTypeSet(showPre: boolean, showCommon: boolean): Set<RelationType> {
  const types = new Set<RelationType>();
  if (showPre) types.add('pre');
  if (showCommon) types.add('common');
  return types;
}

export function createFlowGraph(
  data: RelationGraphResponse,
  filter: GraphFilterState,
): { nodes: RelationFlowNode[]; edges: RelationFlowEdge[] } {
  const visibleTypes = getVisibleTypeSet(filter.showPre, filter.showCommon);
  const visibleEdges = data.edges.filter((edge) => visibleTypes.has(edge.type));
  const incidentIds = new Set<string>();
  const neighborhoodIds = new Set<string>();
  const focusId = filter.hoverId || filter.activeId;

  for (const edge of visibleEdges) {
    incidentIds.add(edge.source);
    incidentIds.add(edge.target);
    if (focusId && (edge.source === focusId || edge.target === focusId)) {
      neighborhoodIds.add(edge.source);
      neighborhoodIds.add(edge.target);
    }
  }

  if (focusId) {
    neighborhoodIds.add(focusId);
  }

  const query = normalizeSearch(filter.query);
  const matchedIds = new Set<string>();

  if (query) {
    for (const node of data.nodes) {
      if (matchesQuery(node, query)) {
        matchedIds.add(node.id);
      }
    }
  }

  const nodes = data.nodes
    .filter((node) => filter.showIsolated || !node.isolated || incidentIds.has(node.id))
    .filter((node) => !query || matchedIds.has(node.id))
    .map((node) => {
      const isDimmed = Boolean(focusId && !neighborhoodIds.has(node.id));

      return {
        id: node.id,
        type: 'problem' as const,
        width: CARD_WIDTH,
        height: CARD_HEIGHT,
        position: { x: 0, y: 0 },
        data: {
          ...node,
          isActive: node.id === filter.activeId,
          isDimmed,
          isMatched: matchedIds.has(node.id),
        },
      };
    });

  const visibleNodeIds = new Set(nodes.map((node) => node.id));
  const edges = visibleEdges
    .filter((edge) => visibleNodeIds.has(edge.source) && visibleNodeIds.has(edge.target))
    .map((edge) => {
      const focused = focusId && (edge.source === focusId || edge.target === focusId);

      return {
        id: edge.id,
        source: edge.source,
        target: edge.target,
        type: edge.type === 'pre' ? 'smoothstep' : 'default',
        animated: edge.type === 'pre' && Boolean(focused),
        data: edge,
        className: [
          'relation-edge',
          `relation-edge-${edge.type}`,
          focusId && !focused ? 'relation-edge-dimmed' : '',
        ].filter(Boolean).join(' '),
        markerEnd: edge.type === 'pre'
          ? { type: MarkerType.ArrowClosed, color: '#2563eb', width: 18, height: 18 }
          : undefined,
      };
    });

  return { nodes, edges };
}

export function findNode(data: RelationGraphResponse | null, id: string): RelationNodeData | null {
  if (!data || !id) return null;
  return data.nodes.find((node) => node.id === id) || null;
}

function normalizeSearch(value: string): string {
  return value.trim().toLowerCase();
}

function matchesQuery(node: RelationNodeData, query: string): boolean {
  return [
    node.oj,
    node.problem_id,
    node.label,
    node.title,
    node.difficulty,
    node.primaryTag,
    ...(node.tags || []),
  ].join(' ').toLowerCase().includes(query);
}
