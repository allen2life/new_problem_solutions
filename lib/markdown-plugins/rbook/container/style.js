export default [
  'style',
  {
    validate(params) {
      return /^style\s+/.test(params.trim());
    },
    render(tokens, idx) {
      const params = tokens[idx].info.trim();
      if (tokens[idx].nesting === 1) {
        const style = params.replace(/^style\s+/, '');
        return `<div style="${style}">\n`;
      }
      return '</div>\n';
    }
  }
];
