# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Static website for **Waikereru** (www.waikereru.org) — an ecological sanctuary near Gisborne, New Zealand, run by the Longbush Ecological Trust. Built with **Jekyll** using the **Minimal Mistakes** theme, hosted on GitHub Pages.

## Commands

```bash
# Install Ruby dependencies and serve locally
bundle install
bundle exec jekyll serve

# Build the site to _site/
bundle exec jekyll build

# Rebuild the minified JS (after editing assets/js/_main.js)
npm run build:js
```

There are no lint or test scripts.

## Architecture

### Content Types

- **Blog posts** live in `_posts/` as `YYYY-MM-DD-slug.md`. Every post uses `layout: single`, `classes: wide`, and `categories: - News` (primary). A `teaser` image in the header is required for grid/social display.
- **Static pages** live in `_pages/` (e.g., `history.md`, `team.md`, `support.md`). Use `layout: single` or `layout: splash`.
- **Data files** in `_data/` drive navigation (`navigation.yml`) and UI text (`ui-text.yml`).
- **Images** are organized by topic in `assets/images/<topic>/`. Post images go in `assets/images/news/`. Image paths use the `/assets/images/...` absolute form.

### Jekyll Configuration (`_config.yml`)

- Custom skin: `waikereru` (green links `#2f6338`, red headings `#FB0303`)
- Permalink format: `/:categories/:title/`
- Pagination: 5 posts per page
- Plugins: `jekyll-paginate`, `jekyll-sitemap`, `jekyll-gist`, `jekyll-feed`, `jemoji`
- Post defaults: `layout: single`, `author_profile: true`, `share: true`, `related: true`
- HTML compression enabled (disabled in development)

### Custom Includes

- `{% include figure image_path="/assets/images/news/filename.jpg" %}` — embeds images with optional captions (use this, NOT Markdown `![]()`)
- `{% include video id="..." provider="youtube" %}` — responsive video embed
- `{% include image-comparison.html image_id="..." before="..." after="..." %}` — Knight Lab Juxtapose before/after slider (JS loaded from CDN)

### Sass/CSS

The custom Waikereru skin is at `_sass/minimal-mistakes/skins/_waikereru.scss`. Override theme styles there. The entry point is `assets/css/main.scss`.

### JavaScript

Custom JS is in `assets/js/_main.js`. After editing, run `npm run build:js` to minify into `assets/js/main.min.js`. jQuery 3.3.1 and several plugins (FitVids, GreedyNav, Magnific Popup, Smooth Scroll) are bundled.

## Creating a New Blog Post

1. Create `_posts/YYYY-MM-DD-slug.md` with this front matter:

```markdown
---
title: "Post Title"
layout: single
classes: wide
header:
  teaser: /assets/images/news/teaser-image.jpg
categories:
  - News
---
```

2. Use `{% include figure image_path="/assets/images/news/image.jpg" %}` for all inline images
3. Copy images to `assets/images/news/`

### Email-to-Post Skill

A Claude Code skill at `.claude/skills/process-email/` can parse `.eml` files into new blog posts. Triggered by `/process-email`, it extracts subject/date/body/images, saves images to `assets/images/news/`, and writes the post to `_posts/`.

## Key File Locations

| Purpose | Path |
|---|---|
| Config | `_config.yml` |
| Posts | `_posts/` |
| Pages | `_pages/` |
| Navigation | `_data/navigation.yml` |
| UI text | `_data/ui-text.yml` |
| Custom skin | `_sass/minimal-mistakes/skins/_waikereru.scss` |
| Custom JS | `assets/js/_main.js` |
| Post images | `assets/images/news/` |
| Documents (PDFs) | `assets/documents/` |
