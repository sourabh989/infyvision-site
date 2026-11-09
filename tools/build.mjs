import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { execFileSync } from 'node:child_process';
import { build } from 'esbuild';
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
process.chdir(root);
await fs.rm(path.join(root,'site'),{recursive:true,force:true});
execFileSync('python3', ['tools/generate.py'], {stdio:'inherit'});
const target = path.resolve(root, 'public');
await fs.rm(target,{recursive:true,force:true});
await fs.mkdir(target,{recursive:true});
await fs.cp(path.join(root,'site'),target,{recursive:true});
const assets = path.join(target,'assets');
const fonts = [
  ['@fontsource-variable/plus-jakarta-sans','plus-jakarta-sans-latin-wght-normal.woff2','jakarta-latin.woff2']
];
for(const [pkg,src,name] of fonts) await fs.copyFile(path.join(root,'node_modules',pkg,'files',src),path.join(assets,name));
execFileSync(path.join(root,'node_modules/.bin/tailwindcss'),['-i','src/input.css','-o',path.join(assets,'site.css'),'--minify'],{stdio:'inherit'});
await build({entryPoints:['src/site.js'],bundle:true,minify:true,target:['es2020'],outfile:path.join(assets,'site.js'),legalComments:'eof'});
const licenses = [];
for(const pkg of ['tailwindcss','esbuild','@fontsource-variable/plus-jakarta-sans']) {
  const dir=path.join(root,'node_modules',pkg);
  const manifest=JSON.parse(await fs.readFile(path.join(dir,'package.json'),'utf8'));
  const names=await fs.readdir(dir);
  const name=names.find(n=>/^licen[cs]e(\.|$)/i.test(n)) || names.find(n=>/^ofl/i.test(n));
  licenses.push(`${pkg} ${manifest.version}\n${name ? await fs.readFile(path.join(dir,name),'utf8') : 'See package distribution license.'}`);
}
await fs.writeFile(path.join(assets,'THIRD-PARTY-LICENSES.txt'),licenses.join('\n\n---------------------\n\n'));
console.log('Clean static output:',target);
