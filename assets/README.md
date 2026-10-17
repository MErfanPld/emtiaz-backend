# Assets Structure

```
assets/
  css/           # Page-specific styles (extracted from HTML)
    about.css
    blog_detail.css
    blogs.css
    dashboard.css
    home_detail.css
    homes.css
    index.css
    info.css
    login.css
  js/
    tailwind-config.js   # Shared Tailwind theme/colors
    mobile-menu.js       # Shared mobile navigation
    login.js             # Login page interactions
  logo.svg
  responsive.css         # Shared responsive utilities
```

Each HTML page links to:
- `assets/css/{page}.css`
- `assets/responsive.css`
- `assets/js/tailwind-config.js` (after Tailwind CDN)
- `assets/js/mobile-menu.js` (before `</body>`)
