import test from 'node:test';
import assert from 'node:assert/strict';
import { buildAccessUrls } from '../lib/access-urls.js';

test('buildAccessUrls includes localhost and LAN IPv4 addresses', () => {
  const mockInterfaces = {
    lo: [{ address: '127.0.0.1', family: 'IPv4', internal: true }],
    eth0: [
      { address: '192.168.1.20', family: 'IPv4', internal: false },
      { address: 'fe80::1', family: 'IPv6', internal: false },
    ],
    wlan0: [{ address: '10.0.0.5', family: 'IPv4', internal: false }],
  };

  const urls = buildAccessUrls(3000, mockInterfaces);

  assert.deepEqual(urls, [
    'http://127.0.0.1:3000',
    'http://192.168.1.20:3000',
    'http://10.0.0.5:3000',
  ]);
});
