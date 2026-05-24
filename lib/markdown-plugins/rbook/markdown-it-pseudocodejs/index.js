import { createRequire } from 'module';

const require = createRequire(import.meta.url);
const pseudocode = require('./pseudocode.js-1.1.0/pseudocode.min.cjs');

function pseudocodeBlockRule(state, start, end, silent) {
  let firstLine;
  let lastLine = '';
  let lastPos;
  let found = false;
  let pos = state.bMarks[start] + state.tShift[start];
  let max = state.eMarks[start];

  if (pos + 14 > max) return false;
  if (state.src.slice(pos, pos + 14) !== '::: pseudocode') return false;

  pos += 14;
  firstLine = state.src.slice(pos, max);

  if (silent) return true;
  if (firstLine.trim().slice(-3) === ':::') {
    firstLine = firstLine.trim().slice(0, -3);
    found = true;
  }

  let next = start;
  while (!found) {
    next += 1;
    if (next >= end) break;

    pos = state.bMarks[next] + state.tShift[next];
    max = state.eMarks[next];

    if (pos < max && state.tShift[next] < state.blkIndent) {
      break;
    }

    if (state.src.slice(pos, max).trim().slice(-3) === ':::') {
      lastPos = state.src.slice(0, max).lastIndexOf(':::');
      lastLine = state.src.slice(pos, lastPos);
      found = true;
    }
  }

  state.line = next + 1;

  const token = state.push('pseudocode_block', 'pseudocode', 0);
  token.block = true;
  token.content = `${firstLine && firstLine.trim() ? `${firstLine}\n` : ''}${
    state.getLines(start + 1, next, state.tShift[start], true)
  }${lastLine && lastLine.trim() ? lastLine : ''}`;
  token.map = [start, state.line];
  token.markup = '::: pseudocode';
  return true;
}

export default function pseudocodePlugin(md, options = {}) {
  const pseudocodeBlock = (code) => {
    try {
      return `<p>${pseudocode.renderToString(code, options)}</p>`;
    } catch (error) {
      if (options.throwOnError) {
        throw error;
      }
      return md.utils.escapeHtml(code);
    }
  };

  md.block.ruler.after('blockquote', 'pseudocode_block', pseudocodeBlockRule, {
    alt: ['paragraph', 'reference', 'blockquote', 'list']
  });
  md.renderer.rules.pseudocode_block = (tokens, idx) => `${pseudocodeBlock(tokens[idx].content)}\n`;
}
