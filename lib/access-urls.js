export function buildAccessUrls(port, networkInterfaces) {
  const urls = new Set([`http://127.0.0.1:${port}`]);

  for (const entries of Object.values(networkInterfaces || {})) {
    for (const info of entries || []) {
      if (info.family === 'IPv4' && info.internal === false) {
        urls.add(`http://${info.address}:${port}`);
      }
    }
  }

  return Array.from(urls);
}
