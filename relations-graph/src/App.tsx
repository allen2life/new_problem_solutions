import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import {
  Background,
  BackgroundVariant,
  Controls,
  ReactFlow,
  ReactFlowProvider,
  useEdgesState,
  useNodesState,
  useReactFlow,
  type NodeMouseHandler,
} from '@xyflow/react';
import '@xyflow/react/dist/style.css';
import './styles.css';

import ProblemNode from './ProblemNode';
import { DetailsPanel } from './DetailsPanel';
import { TagLegend } from './TagLegend';
import { Toolbar } from './Toolbar';
import { addRelationCounts, createFlowGraph, findNode } from './graph-data';
import { applyLayout } from './layout';
import { readInitialUrlState, readSettings, saveSettings, updateUrlState } from './settings';
import type { GraphSettings, RelationFlowEdge, RelationFlowNode, RelationGraphResponse } from './types';

const nodeTypes = { problem: ProblemNode };

export default function App() {
  return (
    <ReactFlowProvider>
      <RelationsGraph />
    </ReactFlowProvider>
  );
}

function RelationsGraph() {
  const initialUrlState = useMemo(() => readInitialUrlState(), []);
  const [data, setData] = useState<RelationGraphResponse | null>(null);
  const [error, setError] = useState('');
  const [query, setQuery] = useState('');
  const [activeId, setActiveId] = useState(initialUrlState.activeId);
  const [hoverId, setHoverId] = useState('');
  const [settings, setSettings] = useState<GraphSettings>(() => ({
    ...readSettings(),
    ...initialUrlState.settingsPatch,
  }));
  const [nodes, setNodes, onNodesChange] = useNodesState<RelationFlowNode>([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState<RelationFlowEdge>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isLayouting, setIsLayouting] = useState(false);
  const layoutSignatureRef = useRef('');
  const flowWrapRef = useRef<HTMLDivElement | null>(null);
  const { fitView, getViewport, setCenter, setViewport } = useReactFlow<RelationFlowNode, RelationFlowEdge>();

  const summaryText = useMemo(() => {
    if (!data) return isLoading ? '正在加载...' : '暂无数据';
    return [
      `${data.summary.relationNodes} 个关系节点`,
      `${data.summary.isolatedNodes} 个孤立题目`,
      `${data.summary.preEdges} 条 pre`,
      `${data.summary.commonEdges} 条 common`,
    ].join(' / ');
  }, [data, isLoading]);

  const selectedNode = useMemo(() => findNode(data, activeId), [data, activeId]);

  const buildFlowGraph = useCallback(() => {
    if (!data) return { nodes: [], edges: [] };
    return createFlowGraph(data, {
      query,
      activeId,
      hoverId,
      showPre: settings.showPre,
      showCommon: settings.showCommon,
      showIsolated: settings.showIsolated,
    });
  }, [activeId, data, hoverId, query, settings.showCommon, settings.showIsolated, settings.showPre]);

  const runLayout = useCallback(async (force = false) => {
    if (!data) return;

    const graph = buildFlowGraph();
    const signature = JSON.stringify({
      nodeIds: graph.nodes.map((node) => node.id).sort(),
      edgeIds: graph.edges.map((edge) => edge.id).sort(),
      layout: settings.layout,
      edgeLength: settings.edgeLength,
      nodeSpacing: settings.nodeSpacing,
      layerSpacingRatio: settings.layerSpacingRatio,
      forceStrength: settings.forceStrength,
    });

    if (!force && signature === layoutSignatureRef.current) {
      setNodes((current) => current.map((node) => {
        const next = graph.nodes.find((item) => item.id === node.id);
        return next ? { ...node, data: next.data } : node;
      }));
      setEdges(graph.edges);
      return;
    }

    layoutSignatureRef.current = signature;
    setIsLayouting(true);
    try {
      const layoutedNodes = await applyLayout(graph.nodes, graph.edges, settings.layout, settings);
      setNodes(layoutedNodes);
      setEdges(graph.edges);
      window.requestAnimationFrame(() => fitView({ padding: 0.18, duration: 360 }));
    } finally {
      setIsLayouting(false);
    }
  }, [buildFlowGraph, data, fitView, setEdges, setNodes, settings]);

  useEffect(() => {
    let cancelled = false;
    setIsLoading(true);

    fetch('/api/relations')
      .then((response) => {
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        return response.json() as Promise<RelationGraphResponse>;
      })
      .then((result) => {
        if (cancelled) return;
        setData(addRelationCounts(result));
        setError('');
      })
      .catch((fetchError) => {
        if (cancelled) return;
        setError(`关系图加载失败：${fetchError.message}`);
      })
      .finally(() => {
        if (!cancelled) setIsLoading(false);
      });

    return () => {
      cancelled = true;
    };
  }, []);

  useEffect(() => {
    saveSettings(settings);
    updateUrlState(activeId, settings);
  }, [activeId, settings]);

  useEffect(() => {
    runLayout(false);
  }, [runLayout]);

  useEffect(() => {
    if (!activeId || nodes.length === 0) return;
    const focused = nodes.find((node) => node.id === activeId);
    if (!focused) return;
    setCenter(focused.position.x + 105, focused.position.y + 56, { zoom: 1, duration: 320 });
  }, [activeId, nodes, setCenter]);

  const handleSettingsChange = useCallback((patch: Partial<GraphSettings>) => {
    setSettings((current) => ({ ...current, ...patch }));
  }, []);

  const handleNodeClick: NodeMouseHandler<RelationFlowNode> = useCallback((_, node) => {
    setActiveId(node.id);
  }, []);

  const handleNodeDoubleClick: NodeMouseHandler<RelationFlowNode> = useCallback((_, node) => {
    window.location.href = node.data.url;
  }, []);

  const handleWheel = useCallback((event: React.WheelEvent<HTMLDivElement>) => {
    if (!flowWrapRef.current) return;
    event.preventDefault();

    const bounds = flowWrapRef.current.getBoundingClientRect();
    const viewport = getViewport();
    const localX = event.clientX - bounds.left;
    const localY = event.clientY - bounds.top;
    const flowX = (localX - viewport.x) / viewport.zoom;
    const flowY = (localY - viewport.y) / viewport.zoom;
    const zoomFactor = Math.exp(-event.deltaY * 0.0018 * settings.wheelSensitivity);
    const nextZoom = Math.max(0.12, Math.min(2.2, viewport.zoom * zoomFactor));

    setViewport({
      x: localX - flowX * nextZoom,
      y: localY - flowY * nextZoom,
      zoom: nextZoom,
    }, { duration: 80 });
  }, [getViewport, setViewport, settings.wheelSensitivity]);

  return (
    <main className="relations-graph-app">
      <Toolbar
        settings={settings}
        query={query}
        summaryText={summaryText}
        onSettingsChange={handleSettingsChange}
        onQueryChange={setQuery}
        onApplyLayout={() => runLayout(true)}
        onFit={() => fitView({ padding: 0.18, duration: 320 })}
      />

      <div ref={flowWrapRef} className="relations-flow-wrap" aria-busy={isLoading || isLayouting} onWheel={handleWheel}>
        {error ? (
          <div className="graph-error">{error}</div>
        ) : (
          <ReactFlow
            nodes={nodes}
            edges={edges}
            nodeTypes={nodeTypes}
            onNodesChange={onNodesChange}
            onEdgesChange={onEdgesChange}
            onNodeClick={handleNodeClick}
            onNodeDoubleClick={handleNodeDoubleClick}
            onNodeMouseEnter={(_, node) => setHoverId(node.id)}
            onNodeMouseLeave={() => setHoverId('')}
            onPaneClick={() => setActiveId('')}
            fitView
            minZoom={0.12}
            maxZoom={2.2}
            panOnScroll={false}
            selectionOnDrag
            zoomOnScroll={false}
            zoomOnPinch
            zoomActivationKeyCode={null}
            panActivationKeyCode={null}
            nodeDragThreshold={2}
            defaultEdgeOptions={{ reconnectable: false }}
            proOptions={{ hideAttribution: true }}
            zoomOnDoubleClick={false}
            preventScrolling
            connectionLineStyle={{ stroke: '#64748b' }}
            translateExtent={[[-12000, -12000], [12000, 12000]]}
            nodeExtent={[[-12000, -12000], [12000, 12000]]}
            fitViewOptions={{ padding: 0.18 }}
            panOnDrag
          >
            <Background variant={BackgroundVariant.Dots} gap={24} size={1.2} color="#cbd5e1" />
            <Controls position="bottom-right" showInteractive={false} />
          </ReactFlow>
        )}

        {(isLoading || isLayouting) && (
          <div className="graph-loading">{isLoading ? '正在加载关系图...' : '正在计算布局...'}</div>
        )}
      </div>

      <DetailsPanel node={selectedNode} />
      {settings.showLegend && data && <TagLegend tags={data.tagStats} />}
    </main>
  );
}
