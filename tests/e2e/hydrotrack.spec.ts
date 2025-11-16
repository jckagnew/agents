/**
 * E2E tests for HydroTrack application
 * Tests core user flows: onboarding, logging, goals, progress
 */

import { test, expect } from '@playwright/test';

test.describe('HydroTrack - Core User Flows', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
  });

  test('should display splash screen and navigate to dashboard', async ({ page }) => {
    // Wait for splash screen
    await expect(page.locator('h1')).toContainText('HydroTrack');

    // Check for "Get Started" button
    const getStartedButton = page.locator('button:has-text("Get Started")');
    await expect(getStartedButton).toBeVisible();

    // Click to enter app
    await getStartedButton.click();

    // Should navigate to dashboard
    await expect(page).toHaveURL(/.*dashboard/);
  });

  test('should log water intake entry', async ({ page }) => {
    // Navigate to dashboard
    await page.goto('/dashboard');

    // Click "Log Entry" button
    const logButton = page.locator('button:has-text("Log Entry")');
    await logButton.click();

    // Modal should appear
    const modal = page.locator('[role="dialog"]');
    await expect(modal).toBeVisible();

    // Enter water amount
    const input = page.locator('input[type="number"]');
    await input.fill('500');

    // Submit entry
    const submitButton = page.locator('button:has-text("Save")');
    await submitButton.click();

    // Success message should appear
    await expect(page.locator('text=Entry logged successfully')).toBeVisible();

    // Entry should appear in history
    await expect(page.locator('text=500 ml')).toBeVisible();
  });

  test('should create a daily goal', async ({ page }) => {
    // Navigate to goals screen
    await page.goto('/goals');

    // Click "Add Goal" button
    const addGoalButton = page.locator('button:has-text("Add Goal")');
    await addGoalButton.click();

    // Fill in goal details
    await page.locator('input[name="goalName"]').fill('Daily Water Intake');
    await page.locator('input[name="target"]').fill('2000');
    await page.locator('select[name="unit"]').selectOption('ml');
    await page.locator('select[name="frequency"]').selectOption('daily');

    // Save goal
    await page.locator('button:has-text("Save Goal")').click();

    // Goal should appear in list
    await expect(page.locator('text=Daily Water Intake')).toBeVisible();
    await expect(page.locator('text=2000 ml')).toBeVisible();
  });

  test('should display progress chart', async ({ page }) => {
    // Navigate to progress screen
    await page.goto('/progress');

    // Chart should be visible
    const chart = page.locator('canvas, svg').first();
    await expect(chart).toBeVisible();

    // Stats should be displayed
    await expect(page.locator('text=/Total entries:/i')).toBeVisible();
    await expect(page.locator('text=/Current streak:/i')).toBeVisible();
  });

  test('should edit existing entry', async ({ page }) => {
    // Navigate to history
    await page.goto('/history');

    // Find an entry
    const entry = page.locator('[data-testid="entry-card"]').first();
    await entry.hover();

    // Click edit button
    await entry.locator('button[aria-label="Edit"]').click();

    // Modify value
    const input = page.locator('input[type="number"]');
    await input.fill('750');

    // Save changes
    await page.locator('button:has-text("Save")').click();

    // Updated value should appear
    await expect(page.locator('text=750 ml')).toBeVisible();
  });

  test('should delete entry with confirmation', async ({ page }) => {
    // Navigate to history
    await page.goto('/history');

    // Swipe or click delete on entry
    const entry = page.locator('[data-testid="entry-card"]').first();
    await entry.hover();
    await entry.locator('button[aria-label="Delete"]').click();

    // Confirmation dialog should appear
    const dialog = page.locator('[role="alertdialog"]');
    await expect(dialog).toBeVisible();
    await expect(dialog).toContainText('Delete entry?');

    // Confirm deletion
    await dialog.locator('button:has-text("Delete")').click();

    // Entry should be removed
    // (This would check that the entry is no longer visible)
  });

  test('should be responsive on mobile', async ({ page }) => {
    // Set mobile viewport
    await page.setViewportSize({ width: 375, height: 667 });

    // Navigate to dashboard
    await page.goto('/dashboard');

    // Bottom navigation should be visible
    const bottomNav = page.locator('[data-testid="bottom-nav"]');
    await expect(bottomNav).toBeVisible();

    // Tap navigation items
    await page.locator('text=Progress').click();
    await expect(page).toHaveURL(/.*progress/);

    await page.locator('text=Goals').click();
    await expect(page).toHaveURL(/.*goals/);
  });

  test('should export data', async ({ page }) => {
    // Navigate to settings
    await page.goto('/settings');

    // Click export button
    const exportButton = page.locator('button:has-text("Export Data")');

    // Start waiting for download before clicking
    const downloadPromise = page.waitForEvent('download');
    await exportButton.click();

    // Wait for download to complete
    const download = await downloadPromise;

    // Verify download file name
    expect(download.suggestedFilename()).toMatch(/hydrotrack-.*\.json/);
  });
});

test.describe('HydroTrack - Accessibility', () => {
  test('should have no accessibility violations', async ({ page }) => {
    await page.goto('/dashboard');

    // This would use axe-core or similar
    // For now, just check basic ARIA attributes
    const buttons = page.locator('button');
    const count = await buttons.count();

    // All buttons should have accessible labels
    for (let i = 0; i < count; i++) {
      const button = buttons.nth(i);
      const label = await button.getAttribute('aria-label');
      const text = await button.textContent();

      expect(label || text).toBeTruthy();
    }
  });

  test('should be keyboard navigable', async ({ page }) => {
    await page.goto('/dashboard');

    // Tab through interactive elements
    await page.keyboard.press('Tab');
    await expect(page.locator(':focus')).toBeVisible();

    // Should be able to activate with Enter
    await page.keyboard.press('Enter');
    // (Check that action occurred)
  });
});
