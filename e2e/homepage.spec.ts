import { test, expect } from '@playwright/test';

test.describe('Homepage Tests', () => {
  const BASE_URL = 'https://coach-matrix-d2cd1e717f81.herokuapp.com/';

  test.beforeEach(async ({ page }) => {
    // Start intercepting network requests before navigation
    await page.route('**/*', route => route.continue());
  });

  test('should load homepage and verify basic structure', async ({ page }) => {
    // Navigate to the homepage
    const response = await page.goto(BASE_URL);
    
    // Verify the page load was successful
    expect(response?.status()).toBe(200);
    
    // Wait for the page to be fully loaded
    await page.waitForLoadState('networkidle');

    // Basic structure checks
    await expect(page.locator('body')).toBeVisible();
    
    // Take a screenshot for visual verification
    await page.screenshot({ path: 'e2e/screenshots/homepage.png' });
  });

  test('should verify homepage UI elements and content', async ({ page }) => {
    await page.goto(BASE_URL);
    await page.waitForLoadState('networkidle');

    // Monitor console for errors
    page.on('console', msg => {
      if (msg.type() === 'error') {
        console.error(`Page error: ${msg.text()}`);
      }
    });

    // Basic structure checks
    await expect(page.locator('body')).toBeVisible();

    // Navigation checks
    const nav = page.locator('nav').first();
    await expect(nav).toBeVisible();

    // Content checks
    const main = page.locator('main').first();
    await expect(main).toBeVisible();

    // Look for common landing page elements
    await expect(page.getByRole('heading').first()).toBeVisible();
    
    // Verify links exist
    const links = page.getByRole('link');
    const linkCount = await links.count();
    expect(linkCount).toBeGreaterThan(0);
    console.log(`Found ${linkCount} links on the page`);

    // Verify footer presence
    const footer = page.locator('footer').first();
    await expect(footer).toBeVisible();
  });

  test('should verify responsive behavior', async ({ page }) => {
    // Set viewport to mobile size
    await page.setViewportSize({ width: 375, height: 667 });
    await page.goto(BASE_URL);
    await page.waitForLoadState('networkidle');
    await page.screenshot({ path: 'e2e/screenshots/homepage-mobile.png' });

    // Set viewport to tablet size
    await page.setViewportSize({ width: 768, height: 1024 });
    await page.screenshot({ path: 'e2e/screenshots/homepage-tablet.png' });

    // Set viewport to desktop size
    await page.setViewportSize({ width: 1280, height: 720 });
    await page.screenshot({ path: 'e2e/screenshots/homepage-desktop.png' });
  });
}); 