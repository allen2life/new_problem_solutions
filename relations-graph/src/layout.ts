import ELK from 'elkjs/lib/elk.bundled.js';
import { forceCenter, forceLink, forceManyBody, forceSimulation } from 'd3-force';
import type { LayoutMode, LayoutSettings, RelationFlowEdge, RelationFlowNode } from './types';

const elk = new ELK();
const NODE_WIDTH = 210;
const NODE_HEIGHT = 112;

export async function applyLayout(
  nodes: RelationFlowNode[],
  edges: RelationFlowEdge[],
  mode: LayoutMode,
  settings: LayoutSettings,
): Promise<RelationFlowNode[]> {
  if (nodes.length === 0) {
    return [];
  }

  if (mode === 'learning') {
    return applyElkLayout(nodes, edges, settings);
  }

  if (mode === 'circle') {
    return applyCircleLayout(nodes, settings);
  }

  return applyForceLayout(nodes, edges, settings);
}

async function applyElkLayout(
  nodes: RelationFlowNode[],
  edges: RelationFlowEdge[],
  settings: LayoutSettings,
): Promise<RelationFlowNode[]> {
  const graph = await elk.layout({
    id: 'root',
    layoutOptions: {
      'elk.algorithm': 'layered',
      'elk.direction': 'RIGHT',
      'elk.spacing.nodeNode': String(settings.nodeSpacing),
      'elk.layered.spacing.nodeNodeBetweenLayers': String(settings.edgeLength * settings.layerSpacingRatio),
      'elk.layered.nodePlacement.strategy': 'NETWORK_SIMPLEX',
      'elk.edgeRouting': 'ORTHOGONAL',
    },
    children: nodes.map((node) => ({
      id: node.id,
      width: node.width || NODE_WIDTH,
      height: node.height || NODE_HEIGHT,
    })),
    edges: edges
      .filter((edge) => edge.data?.type === 'pre')
      .map((edge) => ({
        id: edge.id,
        sources: [edge.source],
        targets: [edge.target],
      })),
  });

  const positionById = new Map((graph.children || []).map((node) => [node.id, node]));

  return nodes.map((node) => {
    const position = positionById.get(node.id);
    return {
      ...node,
      position: {
        x: position?.x || 0,
        y: position?.y || 0,
      },
    };
  });
}

function applyForceLayout(
  nodes: RelationFlowNode[],
  edges: RelationFlowEdge[],
  settings: LayoutSettings,
): RelationFlowNode[] {
  const simNodes = nodes.map((node, index) => ({
    id: node.id,
    x: node.position.x || Math.cos(index) * settings.edgeLength,
    y: node.position.y || Math.sin(index) * settings.edgeLength,
  }));
  const simLinks = edges.map((edge) => ({ source: edge.source, target: edge.target }));

  forceSimulation(simNodes)
    .force('charge', forceManyBody().strength(-settings.forceStrength))
    .force('link', forceLink(simLinks).id((node: any) => node.id).distance(settings.edgeLength).strength(0.62))
    .force('center', forceCenter(0, 0))
    .stop()
    .tick(260);

  const positionById = new Map(simNodes.map((node) => [node.id, node]));

  return nodes.map((node) => {
    const position = positionById.get(node.id);
    return {
      ...node,
      position: {
        x: position?.x || 0,
        y: position?.y || 0,
      },
    };
  });
}

function applyCircleLayout(nodes: RelationFlowNode[], settings: LayoutSettings): RelationFlowNode[] {
  const radius = Math.max(260, nodes.length * settings.nodeSpacing * 0.42);
  const step = (Math.PI * 2) / Math.max(1, nodes.length);

  return nodes.map((node, index) => ({
    ...node,
    position: {
      x: Math.cos(index * step) * radius,
      y: Math.sin(index * step) * radius,
    },
  }));
}
