# Contributing and workflow

This project is built one step at a time. Each step gets its own branch, is reviewed, then merged.

## Branches

- `main` always holds reviewed, working code.
- One branch per step, named `step-NN-short-name`, for example `step-02-backend-skeleton`.
- Small fixes use `fix/short-name`.

## Commits

Use short, imperative messages with a type prefix:

- `feat:` new functionality
- `fix:` bug fix
- `docs:` documentation only
- `test:` tests only
- `chore:` setup, config, tooling

Example: `feat: add price normalization for BDT and USD formats`

## Pull requests

1. Open a pull request from the step branch into `main`.
2. Describe what the step adds and what was tested.
3. State anything that could not be tested, for example parts that need packages or models not available in the build environment.
4. Merge after review.

## Build steps

1. Repo setup
2. Backend skeleton and database models
3. Product and brand profiles
4. Grounded text generation
5. Template ad rendering
6. Verification: prices and details
7. Verification: OCR
8. Verification: unsupported claims
9. Verification: brand and image integrity
10. Reports and approval
11. Frontend
12. Test set and evaluation
13. Deployment and docs

## Secrets

Never commit API keys or `.env`. Use `.env.example` to document required variables.
