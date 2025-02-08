import { PlaywrightTestConfig } from '@playwright/test';

const config: PlaywrightTestConfig = {
  testDir: './e2e',
  timeout: 30000,
  retries: 2,
  use: {
    headless: false,
    viewport: { width: 1280, height: 720 },
    actionTimeout: 15000,
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },
  projects: [
    {
      name: 'webkit',
      use: {
        browserName: 'webkit',
      },
    },
  ],
  reporter: [
    ['html'],
    ['list']
  ],
};

export default config; 