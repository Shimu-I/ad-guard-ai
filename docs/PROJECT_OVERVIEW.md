# AdGuard AI: Project Overview, Features, Corner Cases and Value

Written 2026-11-13.

## 1. Project summary

AdGuard AI is a platform that helps businesses create ads with AI, then independently checks them for accuracy, quality and brand consistency before publishing. It is feasible to build as an MVP on free resources, provided the scope stays tight.

**Core value proposition:** Create smarter. Verify better. Advertise confidently.

**Target customers**

- Small and medium e-commerce businesses
- Online retailers
- Digital marketing agencies
- Any business that produces frequent promotional content

**Expected business value**

- Less manual advertisement review
- Fewer inaccurate ads reaching customers
- Consistent brand identity across ads
- Faster ad production
- More confidence before publication

## 2. The problem

Existing AI ad makers produce attractive content but cannot be trusted to publish it unchecked, so businesses still review every ad by hand.

- They can change product appearance or packaging.
- They can generate wrong prices or product details.
- They can invent product benefits that are not supported.
- Their content is often generic.
- They struggle to keep brand identity consistent.
- Their creative scores do not guarantee actual sales.

## 3. Proposed solution

AdGuard AI pairs ad generation with an independent verification step, and both work from one source of truth: the product and brand profile.

1. The business uploads product images, details, prices, claims and brand guidelines.
2. The AI writes ad text using only that profile.
3. A template places the original product photo and overlays the text. The photo is never regenerated.
4. Verification checks prices, details, claims, spelling, brand rules and layout quality.
5. Each check returns one of three outcomes: **Verified**, **Issue found**, or **Cannot verify**.
6. The user reviews the report, fixes issues, and the ad is re-verified after every fix.
7. A human approves the ad, and the final asset and report are exported.

**Key design rule:** admit uncertainty. A "Cannot verify" result is better than a forced pass or fail.

## 4. Features

The MVP has nine features, all buildable on free resources. Later features need more time or paid tools.

| # | Feature | What it does | Stage |
| --- | --- | --- | --- |
| 1 | Product and brand profiles | Stores name, price, specs, allowed claims, brand colors, fonts and logo as the source of truth | MVP |
| 2 | Grounded text generation | LLM writes headlines, captions and promo text using only the profile | MVP |
| 3 | Template-based ad creation | Places the original product photo in a template and overlays text | MVP |
| 4 | Price and detail verification | Checks every price, discount, unit and detail against the profile | MVP |
| 5 | OCR check | Reads the rendered ad and compares it to the intended text; catches typos | MVP |
| 6 | Unsupported claim detection | Flags claims not backed by the profile, such as "best" or "#1" | MVP |
| 7 | Brand consistency check | Compares colors, logo placement and fonts to the brand profile | MVP |
| 8 | Explainable report | Lists each issue with severity, reason and suggested fix | MVP |
| 9 | Approve and export | Human approval, then export of the final image and report | MVP |
| 10 | Logo detection with a trained model | Finds logos in uploaded or rendered images | Later |
| 11 | Packaging-change detection | Detects subtle changes to product packaging | Later |
| 12 | Advanced quality scoring | Hierarchy and CTA visibility beyond simple rules | Later |
| 13 | Bulk generation and team accounts | Many ads at once; multiple users and brands | Later |
| 14 | Platform-specific sizes and video ads | Facebook, Instagram and banner sizes; video | Later |

## 5. What problems this solves

AdGuard AI fully solves wrong prices and typos, mostly solves photo changes and invented claims, and cannot solve sales prediction.

| Existing limitation | Can AdGuard AI solve it? | How |
| --- | --- | --- |
| Wrong prices or product details | Yes | Ads are generated from structured data, then checked against it. This is the strongest feature. |
| Typos and wrong text in the final image | Yes | OCR on the rendered ad, compared with the known text. |
| Black-box AI scores | Yes | Every verdict has a reason, and the app says "Cannot verify" instead of guessing. |
| Enterprise tools are expensive and complex | Yes | A simple, free or low-cost workflow aimed at small businesses. |
| AI changes product look or packaging | Mostly | The photo is never regenerated. A pixel or hash check confirms it was not altered. |
| Invented product benefits | Mostly | Claims are compared to the profile and unsupported ones are flagged. Some subtle cases will be missed. |
| Generic content | Partly | Grounding in product data and brand voice helps, but free LLMs limit creativity. |
| Poor brand consistency | Partly | Colors, fonts and logo placement are checkable. Tone and overall feel are not. |
| Manual review is still needed | Partly | Common errors are caught first, but a human still approves. |
| Creative scores do not predict sales | No | Nobody can guarantee this. The app gives rule-based quality checks with reasons, not fake performance scores. |

## 6. Competitors and differentiation

AdGuard AI competes on verification, not on content generation.

| Competitor | Main limitation or opportunity |
| --- | --- |
| Canva | Primarily design-focused; factual product verification remains important. |
| AdCreative.ai | Creative scores cannot guarantee actual advertising performance. |
| Creatify | AI video and product extraction can introduce inconsistencies. |
| Adobe GenStudio | Comprehensive but enterprise-oriented and potentially complex for smaller businesses. |

**Our differentiation**

- Product-grounded ad generation
- Independent factual and visual verification
- Unsupported claim detection
- Explainable quality reports
- Original product photo preservation
- Affordable workflow for small businesses

This comparison is based on the project plan and has not been re-checked against the competitors' current features.

## 7. Tech stack and free-resource feasibility

The whole stack can run on free tools and free tiers for development and a demo. Free-tier limits change, so check current terms before relying on them.

| Component | Technology | Free option |
| --- | --- | --- |
| Frontend | React, Tailwind CSS | Vercel free tier |
| Backend | Python, FastAPI | Render free tier |
| Database | PostgreSQL | Supabase or Neon free tier |
| NLP | LLM APIs, RAG | Gemini and Groq free tiers |
| Computer vision | OpenCV, CLIP | Open source; Hugging Face Spaces for heavy models |
| OCR | Tesseract | Open source |
| ML | Scikit-learn, PyTorch | Open source |

**Main free-resource risks**

- LLM free tiers have rate and daily limits. Add caching, retries and a swappable LLM layer.
- Free backends sleep and have little CPU and RAM. Run heavy models locally for the demo if needed.
- Free providers may use submitted data. Avoid confidential data and tell users.
- Free storage fills up quickly with images. Compress them and store them outside the database.

**Feasibility:** as a final-year or portfolio project this is achievable if scoped tightly and measured honestly. As a production product businesses can trust, it would need paid APIs, better models and more data.

## 8. Corner cases

These are grouped by module. The most important rule across all of them is to return one of three outcomes: Verified, Issue found, or Cannot verify.

### 8.1 Product and brand input

- Missing fields such as price, description or brand guidelines. Block generation or warn clearly.
- Conflicting data between description, specs and price. Ask the user to resolve it.
- Price formats vary: "1,299", "1299.00", "৳1,299", "BDT 1299", "$12.99".
- Multiple currencies, or a price that changed after the profile was created.
- Discounts: original price, sale price and "50% off" must be mathematically consistent.
- Variants (sizes, colors, bundles) with different prices.
- Product images that are low-resolution, blurry, watermarked, cropped or on a busy background.
- Multiple products in one image, or the wrong image uploaded.
- Very long descriptions, special characters, emojis, or mixed Bangla and English text.
- Duplicate products uploaded under different names.
- Brand guidelines in a PDF with no machine-readable colors or fonts.
- Brands with several logo versions (light, dark, icon-only).

### 8.2 AI text generation

- The LLM invents a price, discount, feature, warranty or "best seller" claim.
- Superlatives such as "best", "#1", "cheapest" or "guaranteed results".
- Health, safety or medical claims for food, cosmetics or supplements.
- Comparative claims against competitors with no evidence.
- Output too long for the ad format's character limits.
- Wrong or mixed language, or poor-quality Bangla output.
- Generic, repetitive output when the product has little data.
- Different results on every run, so verification cannot assume stable output.
- Prompt injection: a product description containing text like "ignore previous instructions".
- Offensive or culturally inappropriate wording.

### 8.3 Template-based visual creation

- Text overflows its box, especially long product names or Bangla text.
- Product photo has the wrong aspect ratio and cropping cuts off the product.
- Low contrast between text and a busy photo background.
- Transparent PNGs, CMYK images or unusual file formats.
- Fonts that do not support Bangla or special characters and render as boxes.
- Different platform sizes (Facebook, Instagram story, banner) breaking the layout.
- Large images exceeding free server memory.

### 8.4 Price and product detail verification

- A price appears in several places and only some are wrong.
- The price appears both in the image and in the caption, so both must be checked.
- "From ৳999" or "up to 50% off" is not an exact price and needs special rules.
- Equivalent formatting ("1,299" vs "1299") must not be flagged.
- Correct number but wrong currency symbol.
- Unit mismatches such as 500g vs 0.5kg or 1L vs 1000ml.
- Shortened product names that are still correct.
- Phone numbers, dates, offer deadlines and URLs in the ad that are not in the product data.
- Expired promotion dates.

### 8.5 OCR text checking

- Stylized, curved, rotated, outlined or very small text.
- Text over gradients or photos.
- Bangla and mixed-script text, where Tesseract is weaker.
- Misreads such as "0" vs "O", "1" vs "l", an unrecognized "৳", or dropped decimal points.
- OCR picks up text printed on the product packaging, not the ad text. Separate the template layer from the photo layer.
- OCR reads nothing. The system must say "Cannot verify", never "Passed".
- Spell-check flags brand names, product names and Bangla-English transliterations as errors.
- **Mitigation:** because the ad is built from a template, the exact text placed is already known. Compare OCR output to that known text and use OCR mainly to confirm the render worked.

### 8.6 Unsupported claim detection

- A true claim is phrased differently from the product data and gets falsely flagged.
- A false claim sounds similar to a supported one and is missed.
- Implied claims such as "doctor recommended", "eco-friendly" or "premium quality".
- Subjective opinions and factual claims need separate handling.
- Numbers and statistics in the ad, such as "3x faster" or "99% satisfaction".
- Negation: "not available in black" misread as "available in black".
- The verifier LLM hallucinates or gives inconsistent verdicts on repeated runs.
- A claim needs outside knowledge that is not in the profile. Mark "Cannot verify" instead of guessing.
- Legal or regulated claims that vary by country.

### 8.7 Product image integrity

- Similar-looking images of different products scoring high on CLIP similarity.
- The same product photographed from another angle scoring low.
- Lighting, background or resizing changes lowering the similarity score.
- A photo edited before upload, so the "original" is not the true original.
- Small packaging changes (a color or label change) that CLIP does not notice.
- One similarity threshold that works for some products but not others.
- **Mitigation:** if the pipeline never regenerates the product photo, verify integrity with a hash or pixel comparison of the placed image. This is far more reliable than CLIP.

### 8.8 Brand consistency

- Colors that are close but not exact because of compression, anti-aliasing or lighting.
- Brands with many colors, gradients or transparency.
- A logo that is correctly placed but resized, distorted or too small.
- Logo detection failing on low-resolution, rotated or partly hidden logos.
- Font detection from an image is unreliable, so check fonts at render time instead.
- Tone-of-voice rules (formal vs casual) that are hard to measure.
- Sub-brands, seasonal campaigns and co-branded ads.

### 8.9 Quality evaluation

- Contrast ratio passes but the text is still hard to read (thin fonts, busy background).
- The CTA is present but visually hidden, or several CTAs compete.
- Accessibility for color-blind users and small mobile screens.
- Scores differ from human opinion, and "good" varies by industry.
- Over-trusting a numeric score. Show reasons, not just a number.

### 8.10 Reports, fixing and export

- Many issues found at once. Prioritize by severity: critical, warning, suggestion.
- An auto-fix introduces a new error. Re-verify after every fix.
- A false positive blocks a correct ad. Offer "override with reason".
- An ad is edited after approval. Invalidate the approval and re-run verification.
- Export in the wrong size, resolution or format for the platform.
- Report wording that is unclear to non-technical users.
- Keep version history and an audit trail of what was approved.

### 8.11 Users and workflow

- Multiple users editing the same product or ad at once.
- Agencies with many client brands. Keep each brand's data isolated.
- A user deletes a product that existing ads still use.
- A user ignores all warnings and publishes anyway. Record it; the human decides.
- Very large batches of ads.

### 8.12 Free-resource and infrastructure limits

- Gemini or Groq rate limit hit mid-process. Add retries, queueing and clear messages.
- Free API terms or limits change without notice. Keep the LLM layer swappable.
- Free-tier provider may use submitted data. Avoid confidential data.
- Backend sleeps after inactivity, so the first request is slow or times out.
- CLIP or PyTorch exceeds free RAM. Use smaller models or run locally.
- Free database storage fills up with images.
- Concurrent users overload the free server. Limit demo access.
- Internet outage during a live demo. Prepare a recorded fallback and cached results.

### 8.13 Legal, ethical and trust

- Users upload copyrighted images or other brands' logos.
- Ads for restricted products such as alcohol, tobacco, medicine or adult content.
- Regional advertising rules. The tool should flag issues, not give legal advice.
- Users treating "verified" as a guarantee. Use wording like "no issues detected".
- Weaker performance for Bangla and other non-English content.

### 8.14 Evaluating the project itself

- No ground-truth dataset exists. Build 30 to 50 test ads with known injected errors.
- A test set that is too easy makes results look better than they are.
- Measuring only accuracy. Also report false positives, false negatives and the "Cannot verify" rate.
- No baseline. Compare against manual review time.
- A small test sample. State this honestly.

## 9. Limitations, claims and evaluation

The project reduces review effort and flags likely issues. It does not guarantee correctness.

**Project limitations**

- AI verification cannot guarantee 100% accuracy.
- Creative quality is subjective.
- Product similarity does not prove product identity.
- Sales performance cannot be guaranteed.
- Free API usage has restrictions.
- Human approval remains necessary.

**Safe to claim**

- Reduces manual review effort.
- Detects price, text and unsupported-claim errors.
- Protects the original product photo.
- Explains every issue it finds.

**Do not claim**

- That it guarantees accuracy or detects every false claim.
- That it predicts sales or ad performance.
- That it replaces human approval.

**Evaluation plan**

1. Create 30 to 50 test ads with deliberately injected errors (wrong price, typo, fake claim, off-brand color).
2. Run the verifier and record what it catches, what it misses, and what it falsely flags.
3. Report the "Cannot verify" rate alongside accuracy.
4. Compare review time with and without the tool.

## 10. Next steps and roadmap

Build on free resources first, and move to paid APIs only if the MVP proves its value.

1. **Foundation:** product and brand profile storage, plus the database and backend setup.
2. **Generation:** grounded text generation and template-based ad rendering with the original photo preserved.
3. **Core verification:** price and detail checks, OCR comparison, and unsupported claim detection.
4. **Brand and quality:** color, font and logo-placement checks, and rule-based contrast and CTA checks.
5. **Reports and approval:** explainable reports with three outcomes, re-verification after fixes, approval and export.
6. **Evaluation:** build the test set of ads with injected errors, measure results, and write up limitations honestly.
7. **Decide:** if results are strong, move to paid APIs, better models and Bangla-focused improvements.

The time needed for each step is not estimated here, since it depends on team size and available weeks.

## 11. Cost and resources: free vs paid

The full MVP can be built on free resources. Paid upgrades are needed only for real users, better Bangla support and data privacy. All prices below are approximate, written from memory and not checked against current pricing pages, so verify before budgeting.

### 11.1 What free resources cover

| Area | Free tool | What it covers |
| --- | --- | --- |
| Frontend hosting | Vercel or Netlify free tier | Demo site |
| Backend hosting | Render free tier | FastAPI API (sleeps when idle, slow first request) |
| Database | Supabase or Neon free tier | Product and brand profiles, reports |
| Image storage | Supabase Storage or Cloudinary free tier | Product photos and exported ads |
| LLM | Gemini and Groq free tiers | Ad text and claim checking (rate limited) |
| OCR | Tesseract | Text reading (weak on Bangla and stylized fonts) |
| Vision | OpenCV, open-source CLIP | Color checks, similarity, hash comparison |
| Heavy models | Hugging Face Spaces or a local machine | CLIP and PyTorch |
| Ad rendering | Pillow or OpenCV templates | Photo plus text overlay |

**Free resources can deliver:** the full MVP for a demo, a project submission and a handful of test users.

**Free resources cannot deliver:**

- Reliable use by many real users, because of rate limits and sleeping servers
- Strong Bangla OCR and text quality
- Logo recognition and packaging-change detection
- Confidential business data handling, since free providers may use submitted data

### 11.2 What paid resources add

| Upgrade | Approx. cost | What you gain |
| --- | --- | --- |
| Paid LLM API (Gemini, OpenAI, Anthropic) | About $5 to $50 per month at low volume, scaling with usage | Higher limits, better claim checking, better Bangla, data privacy terms |
| Always-on backend (Render, Railway, Fly.io) | About $7 to $25 per month | No sleeping, more RAM and CPU |
| Paid database and storage | About $0 to $25 per month | More storage, backups |
| GPU or model hosting (Hugging Face, Modal, Replicate) | Pay per use, about $0.50 to $2 per hour for a GPU | Heavier vision models, logo detection |
| Cloud OCR (Google Vision, AWS Textract) | About $1.50 per 1,000 pages after a free allowance | Much better OCR, including Bangla |
| Domain and email | About $10 to $15 per year | A real product URL |

A realistic paid setup for a small pilot (always-on backend, paid LLM API, cloud OCR and a domain) is roughly $30 to $100 per month, depending on volume.

### 11.3 Recommended upgrade order

1. **Now:** build everything on free resources and prove the verification works with the test set.
2. **First paid upgrades:** cloud OCR (biggest accuracy gain, especially for Bangla), then a paid LLM API (better claim detection), then an always-on backend.
3. **Wait until there are users:** GPU hosting and trained logo detection.
