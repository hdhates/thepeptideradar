import { chromium } from 'playwright';

const OUT = 'C:/Users/hugod/peptideradar';

(async () => {
  const browser = await chromium.launch();

  // ── MOBILE (390x844) ──────────────────────────────────────────────────────
  const mobile = await browser.newContext({
    viewport: { width: 390, height: 844 },
    userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1'
  });

  // 1. Homepage above fold
  {
    const page = await mobile.newPage();
    await page.goto('https://thepeptideradar.com', { waitUntil: 'networkidle' });
    await page.waitForTimeout(2000);
    await page.screenshot({ path: `${OUT}/full3-mobile-home.png`, clip: { x: 0, y: 0, width: 390, height: 844 } });
    await page.close();
    console.log('1/8 full3-mobile-home.png done');
  }

  // 2. Hamburger menu open
  {
    const page = await mobile.newPage();
    await page.goto('https://thepeptideradar.com', { waitUntil: 'networkidle' });
    await page.waitForTimeout(2000);

    // Try several common selectors for hamburger / nav toggle
    const selectors = [
      'button[aria-label*="menu" i]',
      'button[aria-label*="nav" i]',
      '.hamburger',
      '.menu-toggle',
      '.nav-toggle',
      '[class*="hamburger"]',
      '[class*="menu-btn"]',
      '[class*="nav-toggle"]',
      'header button',
      'nav button'
    ];
    let clicked = false;
    for (const sel of selectors) {
      const el = await page.$(sel);
      if (el) {
        await el.click();
        clicked = true;
        console.log(`  Hamburger clicked via: ${sel}`);
        break;
      }
    }
    if (!clicked) console.log('  WARNING: no hamburger button found');
    await page.waitForTimeout(800);
    await page.screenshot({ path: `${OUT}/full3-mobile-nav-open.png`, clip: { x: 0, y: 0, width: 390, height: 844 } });
    await page.close();
    console.log('2/8 full3-mobile-nav-open.png done');
  }

  // 3. Scroll to supplier cards section
  {
    const page = await mobile.newPage();
    await page.goto('https://thepeptideradar.com', { waitUntil: 'networkidle' });
    await page.waitForTimeout(2000);
    await page.evaluate(() => {
      const candidates = [
        document.querySelector('#directory'),
        document.querySelector('#suppliers'),
        document.querySelector('.supplier-cards'),
        document.querySelector('.suppliers'),
        document.querySelector('[class*="directory"]'),
        [...document.querySelectorAll('[class*="card"]')][0],
        [...document.querySelectorAll('article')][0],
        [...document.querySelectorAll('section')][1],
      ].filter(Boolean);
      if (candidates[0]) {
        candidates[0].scrollIntoView({ behavior: 'instant' });
      } else {
        window.scrollBy(0, 900);
      }
    });
    await page.waitForTimeout(600);
    await page.screenshot({ path: `${OUT}/full3-mobile-directory.png`, clip: { x: 0, y: 0, width: 390, height: 844 } });
    await page.close();
    console.log('3/8 full3-mobile-directory.png done');
  }

  // 4. BPC-157 guide page (mobile)
  {
    const page = await mobile.newPage();
    await page.goto('https://thepeptideradar.com/peptides/bpc-157.html', { waitUntil: 'networkidle' });
    await page.waitForTimeout(2000);
    await page.screenshot({ path: `${OUT}/full3-mobile-guide.png`, clip: { x: 0, y: 0, width: 390, height: 844 } });
    await page.close();
    console.log('4/8 full3-mobile-guide.png done');
  }

  await mobile.close();

  // ── DESKTOP (1440x900) ────────────────────────────────────────────────────
  const desktop = await browser.newContext({
    viewport: { width: 1440, height: 900 }
  });

  // 5. Homepage
  {
    const page = await desktop.newPage();
    await page.goto('https://thepeptideradar.com', { waitUntil: 'networkidle' });
    await page.waitForTimeout(2000);
    await page.screenshot({ path: `${OUT}/full3-desktop-home.png`, clip: { x: 0, y: 0, width: 1440, height: 900 } });
    await page.close();
    console.log('5/8 full3-desktop-home.png done');
  }

  // 6. Scroll to directory / supplier cards
  {
    const page = await desktop.newPage();
    await page.goto('https://thepeptideradar.com', { waitUntil: 'networkidle' });
    await page.waitForTimeout(2000);
    await page.evaluate(() => {
      const candidates = [
        document.querySelector('#directory'),
        document.querySelector('#suppliers'),
        document.querySelector('.supplier-cards'),
        document.querySelector('.suppliers'),
        document.querySelector('[class*="directory"]'),
        [...document.querySelectorAll('[class*="card"]')][0],
        [...document.querySelectorAll('article')][0],
        [...document.querySelectorAll('section')][1],
      ].filter(Boolean);
      if (candidates[0]) {
        candidates[0].scrollIntoView({ behavior: 'instant' });
      } else {
        window.scrollBy(0, 900);
      }
    });
    await page.waitForTimeout(600);
    await page.screenshot({ path: `${OUT}/full3-desktop-directory.png`, clip: { x: 0, y: 0, width: 1440, height: 900 } });
    await page.close();
    console.log('6/8 full3-desktop-directory.png done');
  }

  // 7. BPC-157 guide page (desktop)
  {
    const page = await desktop.newPage();
    await page.goto('https://thepeptideradar.com/peptides/bpc-157.html', { waitUntil: 'networkidle' });
    await page.waitForTimeout(2000);
    await page.screenshot({ path: `${OUT}/full3-desktop-guide.png`, clip: { x: 0, y: 0, width: 1440, height: 900 } });
    await page.close();
    console.log('7/8 full3-desktop-guide.png done');
  }

  // 8. Peptides listing page (desktop)
  {
    const page = await desktop.newPage();
    await page.goto('https://thepeptideradar.com/peptides/', { waitUntil: 'networkidle' });
    await page.waitForTimeout(2000);
    await page.screenshot({ path: `${OUT}/full3-desktop-peptides.png`, clip: { x: 0, y: 0, width: 1440, height: 900 } });
    await page.close();
    console.log('8/8 full3-desktop-peptides.png done');
  }

  await desktop.close();
  await browser.close();
  console.log('\nALL SCREENSHOTS COMPLETE');
})().catch(e => { console.error(e); process.exit(1); });
