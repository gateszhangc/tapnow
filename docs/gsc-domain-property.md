# TapNow GSC Domain Property Runbook

This site only integrates Google Search Console. Do not add GA4 or Microsoft Clarity scripts.

## Property target

- Domain property: `tapnow.lol`
- Canonical homepage: `https://tapnow.lol/`
- Sitemap: `https://tapnow.lol/sitemap.xml`

## Verification steps

1. Open Google Search Console and add the Domain property `tapnow.lol`.
2. Copy the DNS verification record that Google provides.
3. Add the TXT or CNAME record in the Cloudflare DNS zone for `tapnow.lol`.
4. Wait for DNS propagation, then click `Verify`.
5. Keep the DNS verification record in place after verification succeeds.

## Post-verification

1. Submit `https://tapnow.lol/sitemap.xml` in Search Console.
2. Run URL Inspection for `https://tapnow.lol/`.
3. Request indexing for the homepage after deployment is live.
4. Confirm Search Console can fetch the sitemap and the homepage without redirect or access issues.

## Expected site signals

- `robots.txt` is reachable at `https://tapnow.lol/robots.txt`
- `sitemap.xml` is reachable at `https://tapnow.lol/sitemap.xml`
- Homepage returns HTTP 200 and includes canonical `https://tapnow.lol/`
- No `google-site-verification` meta tag is used in the page source for this setup
