# AdGuard AI

**Create smarter. Verify better. Advertise confidently.**

AdGuard AI helps businesses create ads with AI, then independently checks them for accuracy, quality and brand consistency before publishing.

> Status: early development. Built step by step; see [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md) for the workflow.
>
> Full project plan, features, corner cases and costs: [docs/PROJECT_OVERVIEW.md](docs/PROJECT_OVERVIEW.md).

## The problem

Existing AI ad makers can change product appearance or packaging, generate wrong prices or invented benefits, produce generic content, and break brand consistency. Businesses still review every ad by hand.

## The approach

1. A business stores a product and brand profile: the single source of truth.
2. AI writes ad text using only that profile.
3. A template places the **original** product photo and overlays text. The photo is never regenerated.
4. Verification checks prices, details, claims, spelling, brand rules and layout.
5. Every check returns one of three results: **Verified**, **Issue found** or **Cannot verify**.
6. A human approves, and the final asset and report are exported.

## MVP features

- Product and brand profiles
- Grounded ad text generation
- Template-based ad creation
- Price and product detail verification
- OCR text checking
- Unsupported claim detection
- Brand consistency checking
- Explainable verification reports

## Planned stack (free tiers first)

| Component | Technology |
| --- | --- |
| Frontend | React, Tailwind CSS |
| Backend | Python, FastAPI |
| Database | PostgreSQL (Supabase or Neon free tier) |
| LLM | Gemini API, Groq (free tiers) |
| OCR | Tesseract |
| Vision | OpenCV, CLIP |
| ML | Scikit-learn, PyTorch |

## Repository layout

```
backend/    FastAPI app, database models, verification modules
frontend/   React and Tailwind web app
tests/      Unit tests and the verification evaluation set
docs/       Project documentation and contributing guide
```

## Getting started

Setup instructions will be added as each component is built. Copy `.env.example` to `.env` and fill in your own keys. Never commit `.env`.

## Limitations

- Verification cannot guarantee 100% accuracy; a human approval step is always required.
- Creative quality is subjective and sales performance cannot be guaranteed.
- Product image similarity does not prove product identity.
- Free API tiers have rate limits that may change.
- OCR and text quality are weaker for Bangla than for English.
