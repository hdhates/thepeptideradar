const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch();
  const context = await browser.newContext({
    viewport: { width: 390, height: 844 },
    userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1'
  });
  const page = await context.newPage();
  await page.goto('https://thepeptideradar.com', { waitUntil: 'networkidle', timeout: 30000 });
  await page.screenshot({ path: 'C:\\Users\\hugod\\peptideradar\\check-mobile.png', fullPage: false });
  await browser.close();
  console.log('Screenshot saved.');
})();
