// Make the QR codes the views show for the repos: node qr.mjs
import QRCode from 'qrcode';
import { mkdirSync, writeFileSync } from 'node:fs';
mkdirSync('public/qr', { recursive: true });
for (const [name, url] of [['meaning-model', 'https://github.com/emergent-wisdom/meaning-model'], ['story', 'https://github.com/emergent-wisdom/story']]) {
  writeFileSync(`public/qr/${name}.svg`, await QRCode.toString(url, { type: 'svg', errorCorrectionLevel: 'M', margin: 2, color: { dark: '#000000', light: '#ffffff' } }));
}
