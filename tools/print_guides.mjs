// Print guide HTML files to A4 PDFs with Playwright Chromium.
import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';
import { pathToFileURL } from 'node:url';

async function loadChromium() {
  const candidates = [
    process.env.PLAYWRIGHT_MODULE,
    '/workspace/qa-tools/node_modules/playwright',
    path.resolve('/workspace/qa-tools/node_modules/playwright'),
  ].filter(Boolean);
  for (const loc of candidates) {
    try {
      const require = createRequire(path.join(loc, 'package.json'));
      return require('playwright').chromium;
    } catch {}
    try {
      const mod = await import(pathToFileURL(path.join(loc, 'index.js')).href);
      return (mod.chromium || mod.default?.chromium);
    } catch {}
  }
  throw new Error('Cannot load Playwright. Set PLAYWRIGHT_MODULE to the playwright package directory.');
}
const chromium = await loadChromium();

const htmlDir = process.argv[2];
const outDir = process.argv[3];
if (!htmlDir || !outDir) {
  console.error('Usage: node tools/print_guides.mjs <htmlDir> <outDir>');
  process.exit(1);
}
fs.mkdirSync(outDir, { recursive: true });

const files = fs.readdirSync(htmlDir).filter(f => f.endsWith('.html')).sort();
if (!files.length) {
  console.error('No HTML guides in', htmlDir);
  process.exit(1);
}

const browser = await chromium.launch({ args: ['--no-proxy-server'] });
try {
  for (const file of files) {
    const src = path.resolve(htmlDir, file);
    const dest = path.resolve(outDir, file.replace(/\.html$/, '.pdf'));
    const context = await browser.newContext({ viewport: { width: 794, height: 1123 } });
    const page = await context.newPage();
    await page.goto('file://' + src, { waitUntil: 'networkidle', timeout: 30000 });
    await page.evaluate(() => document.fonts && document.fonts.ready);
    await page.waitForTimeout(200);
    await page.pdf({
      path: dest,
      printBackground: true,
      preferCSSPageSize: true,
      margin: { top: '0', right: '0', bottom: '0', left: '0' },
    });
    await context.close();
    const kb = Math.round(fs.statSync(dest).size / 1024);
    console.log('Wrote', dest, kb + 'KB');
  }
} finally {
  await browser.close();
}
