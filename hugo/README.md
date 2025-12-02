# Hugo Site for NKU 640

This directory contains the Hugo version of the NKU 640 course documentation.

## Quick Start

### Local Development

```bash
# From this directory
hugo server

# Or from repository root
cd hugo && hugo server
```

Access at: http://localhost:1313

### Build

```bash
# Production build
hugo --minify

# Build with specific baseURL
hugo --minify --baseURL "https://snavleen.github.io/NKU-640/hugo/"
```

## Structure

```
hugo/
├── archetypes/         # Content templates
├── content/            # Markdown content
│   ├── _index.md      # Homepage
│   └── docs/          # Documentation pages
├── static/            # Static assets (CSS, images)
├── themes/            # Hugo themes
│   └── hugo-book/     # Hugo Book theme
├── hugo.toml          # Hugo configuration
└── public/            # Build output (gitignored)
```

## Configuration

See `hugo.toml` for site configuration:
- **baseURL**: Deployment URL
- **theme**: hugo-book
- **params**: Theme-specific settings

## Theme

Using [Hugo Book Theme](https://github.com/alex-shpak/hugo-book):
- Clean documentation layout
- Built-in search
- Table of contents
- Auto light/dark mode
- Mobile responsive

## Content Management

Content is in `content/docs/` with Hugo front matter:

```yaml
---
title: "Page Title"
weight: 10
bookCollapseSection: true
---
```

### Front Matter Options

- `title`: Page title
- `weight`: Sort order (lower = first)
- `bookCollapseSection`: Collapse in menu
- `bookFlatSection`: Flat section layout
- `bookToc`: Show table of contents
- `bookHidden`: Hide from menu

## Deployment

Automated via GitHub Actions (`.github/workflows/deploy-both.yml`):
1. Build Hugo site
2. Combine with MkDocs build
3. Deploy to GitHub Pages at `/hugo/`

## Live Site

**Hugo Version**: https://snavleen.github.io/NKU-640/hugo/
**MkDocs Version**: https://snavleen.github.io/NKU-640/

## Commands Reference

```bash
# Start development server
hugo server

# Build for production
hugo --minify

# Build with drafts
hugo server --buildDrafts

# Clean build cache
hugo mod clean

# Check Hugo version
hugo version
```

## Troubleshooting

### Port Already in Use

```bash
# Kill existing Hugo server
pkill hugo

# Use different port
hugo server --port 1314
```

### Theme Not Found

Ensure theme exists:
```bash
ls themes/hugo-book
```

### Build Errors

Check front matter syntax:
- Must be valid YAML
- Between `---` markers
- At top of file

## Learn More

- [Hugo Documentation](https://gohugo.io/documentation/)
- [Hugo Book Theme Docs](https://github.com/alex-shpak/hugo-book)
- [Hugo Templates](https://gohugo.io/templates/)
