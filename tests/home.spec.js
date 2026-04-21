const { test, expect } = require("@playwright/test");

test.describe("TapNow static keyword site", () => {
  test("desktop homepage renders TapNow content, metadata, and workflow interaction", async ({ page }) => {
    await page.goto("/");

    await expect(page).toHaveTitle(/TapNow \| AI Creative Canvas Guide/i);
    await expect(page.locator("h1")).toHaveText("TapNow");
    await expect(page.locator('meta[name="description"]')).toHaveAttribute("content", /Independent guide to TapNow/i);
    await expect(page.locator('meta[name="keywords"]')).toHaveAttribute("content", /Tapflow/i);
    await expect(page.locator('link[rel="canonical"]')).toHaveAttribute("href", "https://tapnow.lol/");
    await expect(page.locator('meta[property="og:locale"]')).toHaveAttribute("content", "en_US");
    await expect(page.locator('meta[property="og:image"]')).toHaveAttribute("content", "https://tapnow.lol/assets/brand/social-card.png");

    await expect(page.getByRole("link", { name: "Official TapNow" })).toHaveAttribute("href", "https://www.tapnow.ai/");
    await expect(page.getByRole("link", { name: "Official website" })).toHaveAttribute("href", "https://www.tapnow.ai/");
    await expect(page.getByRole("link", { name: "Creator program", exact: true })).toHaveAttribute(
      "href",
      "https://www.tapnow.ai/creator-program"
    );
    await expect(page.getByRole("heading", { name: "What people usually mean when they search for TapNow." })).toBeVisible();
    await expect(page.getByRole("heading", { name: "A creative AI workspace built around connected production." })).toBeVisible();
    await expect(page.getByRole("heading", { name: "From brief to finished asset, every step stays visible." })).toBeVisible();
    await expect(page.getByText("This site is an independent keyword guide.")).toBeVisible();

    await page.locator('[data-node="video"]').click();
    await expect(page.locator("[data-workflow-copy]")).toHaveText(/Turn selected frames and scripts into motion output/i);

    const schemaTypes = await page.locator('script[type="application/ld+json"]').evaluateAll((nodes) =>
      nodes.map((node) => JSON.parse(node.textContent || "{}")["@type"])
    );
    expect(schemaTypes).toEqual(expect.arrayContaining(["WebSite", "WebPage", "FAQPage"]));

    const html = await page.content();
    expect(html).not.toMatch(/google-site-verification|gtag\(|googletagmanager|google-analytics|clarity/i);

    await expect(page.locator(".guide-points li")).toHaveCount(3);
    await expect(page.locator(".feature-card")).toHaveCount(3);
    await expect(page.locator(".case-grid article")).toHaveCount(4);
    await expect(page.locator(".faq-list details")).toHaveCount(5);

    for (const image of await page.locator("img").all()) {
      await image.scrollIntoViewIfNeeded();
    }

    const imagesLoaded = await page.evaluate(() =>
      Array.from(document.images).every((image) => image.complete && image.naturalWidth > 0)
    );
    expect(imagesLoaded).toBe(true);
  });

  test("mobile layout has no horizontal overflow and keeps primary sections accessible", async ({ browser }) => {
    const context = await browser.newContext({
      viewport: { width: 390, height: 844 },
      isMobile: true
    });
    const page = await context.newPage();

    await page.goto("/");

    await expect(page.locator("h1")).toBeVisible();
    await expect(page.getByRole("link", { name: "Guide", exact: true })).toBeVisible();
    await page.getByRole("link", { name: "Guide", exact: true }).click();
    await expect(page.locator("#guide")).toBeInViewport();

    const overflow = await page.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
    expect(overflow).toBeLessThanOrEqual(1);

    await expect(page.locator(".guide-points li")).toHaveCount(3);
    await expect(page.locator(".flow-node")).toHaveCount(4);
    await expect(page.locator(".case-grid article")).toHaveCount(4);
    await context.close();
  });

  test("health check and search files are available", async ({ request }) => {
    const health = await request.get("/healthz");
    expect(health.ok()).toBe(true);
    expect(await health.json()).toEqual({ ok: true });

    const robots = await request.get("/robots.txt");
    expect(await robots.text()).toContain("Sitemap: https://tapnow.lol/sitemap.xml");

    const sitemap = await request.get("/sitemap.xml");
    expect(await sitemap.text()).toContain("<loc>https://tapnow.lol/</loc>");
    expect(await sitemap.text()).toContain("<lastmod>2026-04-21</lastmod>");
  });
});
