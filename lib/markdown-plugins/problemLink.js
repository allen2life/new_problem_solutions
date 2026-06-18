export function createProblemLinkPlugin(problemManager) {
  return function problemLinkPlugin(md) {
    md.inline.ruler.after('text', 'problem_link', (state, silent) => {
      const pos = state.pos;
      const max = state.posMax;

      if (pos + 4 >= max || state.src[pos] !== '[' || state.src[pos + 1] !== '[') {
        return false;
      }

      const endPos = state.src.indexOf(']]', pos + 2);
      if (endPos === -1) {
        return false;
      }

      const content = state.src.slice(pos + 2, endPos).trim();
      let match = content.match(/^([A-Za-z0-9_]+)\/([A-Za-z0-9_-]+)$/);
      if (!match) {
        match = content.match(/^problem\s*:\s*([A-Za-z0-9_]+)\s*,\s*([A-Za-z0-9_-]+)$/i);
      }
      if (!match) {
        return false;
      }

      if (silent) {
        state.pos = endPos + 2;
        return true;
      }

      const oj = match[1];
      const id = match[2];
      const problem = problemManager?.find(oj, id);
      const href = problemManager?.problem_url(oj, id) || `/problems/${oj}/${id}`;

      const token = state.push('link_open', 'a', 1);
      token.attrSet('href', href);
      token.attrSet('target', '_blank');

      if (problem) {
        token.attrSet('class', 'problem-link');
        const textToken = state.push('text', '', 0);
        textToken.content = `${oj}-${id} ${problem.title || ''}`.trim();
      } else {
        token.attrSet('class', 'problem-link warning');
        const textToken = state.push('text', '', 0);
        textToken.content = `Missing problem: ${oj}/${id}`;
      }

      state.push('link_close', 'a', -1);
      state.pos = endPos + 2;
      return true;
    });
  };
}

export default createProblemLinkPlugin;
