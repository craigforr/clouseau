/**
 * @vitest-environment node
 */
import { describe, it, expect, beforeAll, afterAll } from 'vitest';
import { createServer, ViteDevServer } from 'vite';

describe('Frontend Dev Server', () => {
  let server: ViteDevServer;
  const TEST_PORT = 5199; // Use different port to avoid conflicts

  beforeAll(async () => {
    server = await createServer({
      configFile: './vite.config.ts',
      server: {
        port: TEST_PORT,
        strictPort: true,
      },
    });
    await server.listen();
  }, 30000);

  afterAll(async () => {
    if (server) {
      await server.close();
    }
  });

  it('returns 200 on the root path', async () => {
    const response = await fetch(`http://localhost:${TEST_PORT}/`);
    expect(response.status).toBe(200);
  });

  it('serves HTML content', async () => {
    const response = await fetch(`http://localhost:${TEST_PORT}/`);
    const contentType = response.headers.get('content-type');
    expect(contentType).toContain('text/html');
  });

  it('includes the app title in the HTML', async () => {
    const response = await fetch(`http://localhost:${TEST_PORT}/`);
    const html = await response.text();
    expect(html).toContain('Clouseau');
  });
});
