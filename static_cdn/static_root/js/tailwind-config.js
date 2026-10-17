tailwind.config = {
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        /* ===== Brand Primary (Logo #AF2C38) ===== */
        "primary": "#AF2C38",
        "primary-container": "#8A222C",
        "primary-fixed": "#F8E8EA",
        "primary-fixed-dim": "#F0D0D4",
        "on-primary": "#FFFFFF",
        "on-primary-container": "#FFFFFF",
        "on-primary-fixed": "#410005",
        "on-primary-fixed-variant": "#8A222C",
        "surface-tint": "#AF2C38",
        "inverse-primary": "#FFB3B0",

        /* ===== Gold accent (low-use) ===== */
        "secondary": "#B8923A",
        "secondary-container": "#F5EBD3",
        "secondary-fixed": "#F5EBD3",
        "secondary-fixed-dim": "#D4B86A",
        "on-secondary": "#FFFFFF",
        "on-secondary-container": "#3D2E0A",
        "on-secondary-fixed": "#3D2E0A",
        "on-secondary-fixed-variant": "#6B5420",

        /* ===== Ink / charcoal surfaces ===== */
        "tertiary": "#1F2430",
        "tertiary-container": "#2A3140",
        "tertiary-fixed": "#E8EAED",
        "tertiary-fixed-dim": "#C5CAD3",
        "on-tertiary": "#FFFFFF",
        "on-tertiary-container": "#C5CAD3",
        "on-tertiary-fixed": "#1F2430",
        "on-tertiary-fixed-variant": "#4A5160",

        /* ===== Neutrals / surfaces ===== */
        "background": "#FAF7F5",
        "on-background": "#1F2430",
        "surface": "#FAF7F5",
        "surface-bright": "#FFFFFF",
        "surface-dim": "#E8E1DE",
        "surface-variant": "#E8E1DE",
        "surface-container": "#F3EEEC",
        "surface-container-low": "#F7F3F1",
        "surface-container-high": "#EFE9E6",
        "surface-container-highest": "#E8E1DE",
        "surface-container-lowest": "#FFFFFF",
        "on-surface": "#1F2430",
        "on-surface-variant": "#6B7280",
        "outline": "#E8E1DE",
        "outline-variant": "#D4CBC6",
        "inverse-surface": "#1F2430",
        "inverse-on-surface": "#FAF7F5",

        /* ===== Status (not brand red) ===== */
        "error": "#C62828",
        "error-container": "#FFDAD6",
        "on-error": "#FFFFFF",
        "on-error-container": "#93000A",
        "success": "#2E7D5B",
        "warning": "#D98E04",

        /* ===== Convenience brand aliases (login etc.) ===== */
        "brand-navy": "#1F2430",
        "brand-navy-hover": "#2A3140",
        "brand-gold": "#B8923A",
        "brand-gold-subtle": "#F5EBD3",
        "brand-surface": "#FAF7F5",
        "brand-ivory": "#FAF7F5",
        "brand-charcoal": "#1F2430",
        "brand-border": "#E8E1DE",
        "brand-primary": "#AF2C38",
        "brand-primary-dark": "#8A222C",
        "brand-primary-tint": "#F8E8EA"
      },
      borderRadius: {
        DEFAULT: "0.125rem",
        lg: "0.25rem",
        xl: "0.5rem",
        full: "0.75rem"
      },
      spacing: {
        "space-lg": "2rem",
        "space-xs": "0.375rem",
        "space-md": "1.25rem",
        "gutter-mobile": "1rem",
        "margin-mobile": "1.25rem",
        margin: "3rem",
        "space-xl": "3rem",
        "space-sm": "0.75rem",
        gutter: "1.5rem"
      },
      fontFamily: {
        "headline-sm": ["Vazirmatn", "Georgia", "serif"],
        "headline-md": ["Vazirmatn", "Georgia", "serif"],
        "headline-lg": ["Vazirmatn", "Georgia", "serif"],
        "headline-lg-mobile": ["Vazirmatn", "Georgia", "serif"],
        "display-hero": ["Vazirmatn", "Georgia", "serif"],
        "display-hero-mobile": ["Vazirmatn", "Georgia", "serif"],
        "label-lg": ["Vazirmatn", "sans-serif"],
        "label-md": ["Vazirmatn", "sans-serif"],
        "label-sm": ["Vazirmatn", "sans-serif"],
        "title-md": ["Vazirmatn", "sans-serif"],
        "body-md": ["Vazirmatn", "sans-serif"],
        "body-lg": ["Vazirmatn", "sans-serif"],
        "body-sm": ["Vazirmatn", "sans-serif"],
        sans: ["Vazirmatn", "system-ui", "sans-serif"],
        serif: ["Georgia", "Vazirmatn", "serif"]
      },
      fontSize: {
        "headline-sm": ["20px", { lineHeight: "30px", fontWeight: "600" }],
        "headline-md": ["24px", { lineHeight: "36px", fontWeight: "600" }],
        "label-lg": ["14px", { lineHeight: "20px", fontWeight: "600" }],
        "headline-lg": ["36px", { lineHeight: "52px", fontWeight: "700" }],
        "label-md": ["12px", { lineHeight: "18px", fontWeight: "500" }],
        "label-sm": ["10px", { lineHeight: "16px", fontWeight: "600" }],
        "title-md": ["18px", { lineHeight: "28px", fontWeight: "600" }],
        "body-md": ["14px", { lineHeight: "24px", fontWeight: "400" }],
        "headline-lg-mobile": ["26px", { lineHeight: "38px", fontWeight: "700" }],
        "body-lg": ["16px", { lineHeight: "28px", fontWeight: "400" }],
        "body-sm": ["12px", { lineHeight: "20px", fontWeight: "400" }],
        "display-hero-mobile": ["32px", { lineHeight: "48px", fontWeight: "800" }],
        "display-hero": ["48px", { lineHeight: "68px", fontWeight: "800" }]
      }
    }
  }
};
