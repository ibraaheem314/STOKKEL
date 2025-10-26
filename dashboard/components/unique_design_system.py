"""
🎨 STOKKEL UNIQUE DESIGN SYSTEM
=================================

Design inspiré de Lokad, Vekia et meilleures startups B2B 2024
- Data-first (pas de décorations inutiles)
- Minimaliste fonctionnel
- Identité visuelle unique et mémorable
- Professionnel sans être générique

Philosophie Design:
- "Les données sont la star, pas le design"
- Clarté > Beauté
- Fonctionnel > Décoratif
- Unique > Tendance
"""

def get_design_system():
    """
    Retourne le design system complet de Stokkel
    
    PALETTE DE COULEURS UNIQUE STOKKEL
    ===================================
    Inspirée des couleurs de l'Afrique de l'Ouest + Supply Chain moderne
    
    PRIMARY: Orange terracotta (chaleur africaine + urgence supply chain)
    SECONDARY: Bleu pétrole profond (data, fiabilité)
    ACCENT: Jaune safran (attention, alertes)
    NEUTRAL: Grès chauds (élégance discrète)
    
    PAS DE: violet, rose, gradients arc-en-ciel
    """
    
    return {
        # ============================================
        # PALETTE COULEURS UNIQUE STOKKEL
        # ============================================
        "colors": {
            # Couleurs Primaires (Brand Identity)
            "primary": {
                "main": "#D2691E",        # Terracotta Orange (signature Stokkel)
                "light": "#E8944A",       # Orange clair
                "dark": "#A0522D",        # Sienna foncé
                "subtle": "#F4E4D7",      # Crème orange (backgrounds)
            },
            
            # Couleurs Secondaires (Data & Fiabilité)
            "secondary": {
                "main": "#1B4965",        # Bleu pétrole profond
                "light": "#2C6E8C",       # Bleu canard
                "dark": "#0F2B3A",        # Bleu nuit
                "subtle": "#E8F1F5",      # Bleu très pâle
            },
            
            # Accent (Alertes & Actions)
            "accent": {
                "main": "#F4A261",        # Jaune safran (alertes)
                "warning": "#E76F51",     # Corail (critique)
                "success": "#2A9D8F",     # Turquoise (succès)
            },
            
            # Neutres (Typography & Backgrounds)
            "neutral": {
                "900": "#1A1A1A",         # Noir charbon
                "800": "#2D2D2D",         # Gris anthracite
                "700": "#4A4A4A",         # Gris foncé
                "600": "#6B6B6B",         # Gris moyen
                "500": "#8C8C8C",         # Gris
                "400": "#ADADAD",         # Gris clair
                "300": "#CECECE",         # Gris très clair
                "200": "#E8E8E8",         # Crème
                "100": "#F5F5F5",         # Off-white
                "50": "#FAFAFA",          # Presque blanc
                "white": "#FFFFFF",       # Blanc pur
            },
            
            # Couleurs Sémantiques (Status)
            "status": {
                "critical": "#D32F2F",    # Rouge vif
                "high": "#E76F51",        # Corail
                "medium": "#F4A261",      # Safran
                "low": "#2A9D8F",         # Turquoise
                "success": "#2A9D8F",     # Turquoise
                "info": "#1B4965",        # Bleu pétrole
            },
        },
        
        # ============================================
        # TYPOGRAPHIE DISTINCTIVE
        # ============================================
        "typography": {
            # Fonts (pas Inter/Poppins générique)
            "fonts": {
                "sans": "'IBM Plex Sans', -apple-system, system-ui, sans-serif",  # Pro mais chaleureux
                "mono": "'IBM Plex Mono', 'Courier New', monospace",  # Pour données/code
                "display": "'IBM Plex Sans', sans-serif",  # Headings
            },
            
            # Scale (8pt grid system)
            "sizes": {
                "xs": "12px",      # 12px
                "sm": "14px",      # 14px
                "base": "16px",    # 16px
                "lg": "18px",      # 18px
                "xl": "20px",      # 20px
                "2xl": "24px",     # 24px
                "3xl": "30px",     # 30px
                "4xl": "36px",     # 36px
                "5xl": "48px",     # 48px
            },
            
            # Weights
            "weights": {
                "light": "300",
                "normal": "400",
                "medium": "500",
                "semibold": "600",
                "bold": "700",
            },
            
            # Line Heights (optimal readability)
            "lineHeights": {
                "tight": "1.2",
                "base": "1.5",
                "relaxed": "1.75",
            },
        },
        
        # ============================================
        # SPACING (8pt Grid System)
        # ============================================
        "spacing": {
            "xs": "4px",
            "sm": "8px",
            "md": "16px",
            "lg": "24px",
            "xl": "32px",
            "2xl": "48px",
            "3xl": "64px",
            "4xl": "96px",
        },
        
        # ============================================
        # BORDERS & RADIUS
        # ============================================
        "borders": {
            "width": {
                "thin": "1px",
                "base": "2px",
                "thick": "3px",
            },
            "radius": {
                "none": "0",
                "sm": "4px",      # Subtil
                "md": "8px",      # Standard
                "lg": "12px",     # Cards
                "xl": "16px",     # Large cards
                "full": "9999px", # Pills
            },
        },
        
        # ============================================
        # SHADOWS (Subtiles, pas excessives)
        # ============================================
        "shadows": {
            "none": "none",
            "xs": "0 1px 2px rgba(0, 0, 0, 0.05)",
            "sm": "0 2px 4px rgba(0, 0, 0, 0.06)",
            "md": "0 4px 6px rgba(0, 0, 0, 0.07)",
            "lg": "0 10px 15px rgba(0, 0, 0, 0.08)",
            "xl": "0 20px 25px rgba(0, 0, 0, 0.10)",
            # Shadow spéciale Stokkel (warm)
            "stokkel": "0 4px 12px rgba(210, 105, 30, 0.15)",
        },
        
        # ============================================
        # ANIMATIONS (Subtiles & Professionnelles)
        # ============================================
        "animations": {
            "duration": {
                "fast": "150ms",
                "base": "250ms",
                "slow": "400ms",
            },
            "easing": {
                "default": "cubic-bezier(0.4, 0, 0.2, 1)",
                "in": "cubic-bezier(0.4, 0, 1, 1)",
                "out": "cubic-bezier(0, 0, 0.2, 1)",
                "inOut": "cubic-bezier(0.4, 0, 0.2, 1)",
            },
        },
        
        # ============================================
        # COMPOSANTS SPECIFIQUES
        # ============================================
        "components": {
            # Cards Style Lokad/Vekia (fonctionnelles)
            "card": {
                "background": "#FFFFFF",
                "border": "1px solid #E8E8E8",
                "borderRadius": "8px",
                "padding": "24px",
                "shadow": "0 2px 4px rgba(0, 0, 0, 0.06)",
                "hoverShadow": "0 4px 12px rgba(210, 105, 30, 0.15)",
            },
            
            # Data Tables (star du show)
            "table": {
                "headerBg": "#1B4965",
                "headerColor": "#FFFFFF",
                "rowHoverBg": "#F4E4D7",
                "borderColor": "#E8E8E8",
                "fontSize": "14px",
            },
            
            # Buttons (clairs, pas de gradients)
            "button": {
                "primary": {
                    "bg": "#D2691E",
                    "color": "#FFFFFF",
                    "hoverBg": "#A0522D",
                },
                "secondary": {
                    "bg": "#FFFFFF",
                    "color": "#1B4965",
                    "border": "2px solid #1B4965",
                    "hoverBg": "#E8F1F5",
                },
                "danger": {
                    "bg": "#D32F2F",
                    "color": "#FFFFFF",
                    "hoverBg": "#B71C1C",
                },
            },
            
            # KPI Cards (mise en avant des chiffres)
            "kpi": {
                "background": "#FFFFFF",
                "border": "2px solid #E8E8E8",
                "borderRadius": "12px",
                "numberColor": "#D2691E",
                "numberSize": "36px",
                "numberWeight": "700",
                "labelColor": "#6B6B6B",
                "labelSize": "14px",
            },
            
            # Charts (data-centric)
            "chart": {
                "colors": [
                    "#D2691E",  # Primary
                    "#1B4965",  # Secondary
                    "#F4A261",  # Accent
                    "#2A9D8F",  # Success
                    "#E76F51",  # Warning
                ],
                "gridColor": "#E8E8E8",
                "axisColor": "#6B6B6B",
            },
            
            # Alerts (style Vekia)
            "alert": {
                "critical": {
                    "bg": "#FFEBEE",
                    "border": "#D32F2F",
                    "icon": "🚨",
                },
                "warning": {
                    "bg": "#FFF3E0",
                    "border": "#F4A261",
                    "icon": "⚠️",
                },
                "success": {
                    "bg": "#E0F2F1",
                    "border": "#2A9D8F",
                    "icon": "✅",
                },
                "info": {
                    "bg": "#E8F1F5",
                    "border": "#1B4965",
                    "icon": "ℹ️",
                },
            },
        },
        
        # ============================================
        # LAYOUT PRINCIPES
        # ============================================
        "layout": {
            "maxWidth": "1280px",     # Max container width
            "sidebarWidth": "280px",  # Sidebar fixe
            "headerHeight": "64px",   # Header height
            "gridGap": "24px",        # Gap entre éléments
            "contentPadding": "32px", # Padding contenu principal
        },
    }


def get_css_variables(design_system):
    """
    Génère les CSS variables pour tout le design system
    Pour utilisation dans Streamlit st.markdown()
    """
    ds = design_system
    
    css_vars = []
    
    # Colors
    for category, colors in ds["colors"].items():
        if isinstance(colors, dict):
            for name, value in colors.items():
                css_vars.append(f"--color-{category}-{name}: {value};")
        else:
            css_vars.append(f"--color-{category}: {colors};")
    
    # Typography
    for key, value in ds["typography"]["sizes"].items():
        css_vars.append(f"--font-size-{key}: {value};")
    
    for key, value in ds["typography"]["weights"].items():
        css_vars.append(f"--font-weight-{key}: {value};")
    
    # Spacing
    for key, value in ds["spacing"].items():
        css_vars.append(f"--spacing-{key}: {value};")
    
    # Borders
    for key, value in ds["borders"]["radius"].items():
        css_vars.append(f"--radius-{key}: {value};")
    
    return "\n    ".join(css_vars)


def apply_stokkel_design():
    """
    CSS MASTER pour appliquer le design system Stokkel
    À utiliser dans dashboard/app.py
    """
    
    ds = get_design_system()
    
    css = f"""
    <style>
    /* ============================================
       STOKKEL DESIGN SYSTEM - VARIABLES CSS
       ============================================ */
    :root {{
        {get_css_variables(ds)}
        
        /* Fonts */
        --font-sans: {ds["typography"]["fonts"]["sans"]};
        --font-mono: {ds["typography"]["fonts"]["mono"]};
        --font-display: {ds["typography"]["fonts"]["display"]};
    }}
    
    /* ============================================
       RESET & BASE STYLES
       ============================================ */
    
    /* Import IBM Plex Sans (distinctive) */
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;500;600;700&family=IBM+Plex+Mono:wght@400;600&display=swap');
    
    /* Reset Streamlit defaults */
    .stApp {{
        background: {ds["colors"]["neutral"]["50"]};
        font-family: var(--font-sans);
        color: {ds["colors"]["neutral"]["900"]};
    }}
    
    /* Remove Streamlit branding */
    #MainMenu, footer, header {{
        visibility: hidden;
    }}
    
    /* ============================================
       SIDEBAR UNIQUE STOKKEL
       ============================================ */
    
    section[data-testid="stSidebar"] {{
        background: {ds["colors"]["secondary"]["main"]};
        border-right: none;
        box-shadow: 4px 0 12px rgba(0, 0, 0, 0.05);
    }}
    
    section[data-testid="stSidebar"] .element-container {{
        color: {ds["colors"]["neutral"]["white"]};
    }}
    
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {{
        color: {ds["colors"]["neutral"]["white"]};
        font-weight: 600;
        font-family: var(--font-display);
    }}
    
    section[data-testid="stSidebar"] p {{
        color: {ds["colors"]["secondary"]["subtle"]};
    }}
    
    /* Navigation Links Style */
    section[data-testid="stSidebar"] .stRadio > label {{
        background: transparent;
        padding: 12px 16px;
        border-radius: 8px;
        transition: all 0.25s ease;
        color: {ds["colors"]["neutral"]["white"]};
        font-weight: 500;
    }}
    
    section[data-testid="stSidebar"] .stRadio > label:hover {{
        background: {ds["colors"]["secondary"]["light"]};
        transform: translateX(4px);
    }}
    
    section[data-testid="stSidebar"] .stRadio [role="radio"][aria-checked="true"] + label {{
        background: {ds["colors"]["primary"]["main"]};
        color: {ds["colors"]["neutral"]["white"]};
        font-weight: 600;
        box-shadow: 0 4px 12px rgba(210, 105, 30, 0.3);
    }}
    
    /* ============================================
       HEADER & TITLES
       ============================================ */
    
    h1 {{
        font-family: var(--font-display);
        font-size: {ds["typography"]["sizes"]["4xl"]};
        font-weight: {ds["typography"]["weights"]["bold"]};
        color: {ds["colors"]["secondary"]["main"]};
        line-height: 1.2;
        margin-bottom: {ds["spacing"]["lg"]};
        letter-spacing: -0.02em;
    }}
    
    h2 {{
        font-family: var(--font-display);
        font-size: {ds["typography"]["sizes"]["3xl"]};
        font-weight: {ds["typography"]["weights"]["semibold"]};
        color: {ds["colors"]["secondary"]["dark"]};
        margin-bottom: {ds["spacing"]["md"]};
        border-left: 4px solid {ds["colors"]["primary"]["main"]};
        padding-left: {ds["spacing"]["md"]};
    }}
    
    h3 {{
        font-family: var(--font-display);
        font-size: {ds["typography"]["sizes"]["2xl"]};
        font-weight: {ds["typography"]["weights"]["semibold"]};
        color: {ds["colors"]["neutral"]["800"]};
        margin-bottom: {ds["spacing"]["sm"]};
    }}
    
    /* ============================================
       CARDS (Style Lokad/Vekia - Fonctionnelles)
       ============================================ */
    
    .stokkel-card {{
        background: {ds["components"]["card"]["background"]};
        border: {ds["components"]["card"]["border"]};
        border-radius: {ds["components"]["card"]["borderRadius"]};
        padding: {ds["components"]["card"]["padding"]};
        box-shadow: {ds["components"]["card"]["shadow"]};
        transition: all 0.25s ease;
    }}
    
    .stokkel-card:hover {{
        box-shadow: {ds["components"]["card"]["hoverShadow"]};
        transform: translateY(-2px);
    }}
    
    /* Metrics Cards (KPI) */
    .stokkel-kpi {{
        background: {ds["components"]["kpi"]["background"]};
        border: {ds["components"]["kpi"]["border"]};
        border-radius: {ds["components"]["kpi"]["borderRadius"]};
        padding: {ds["spacing"]["lg"]};
        text-align: center;
        transition: all 0.25s ease;
    }}
    
    .stokkel-kpi:hover {{
        border-color: {ds["colors"]["primary"]["main"]};
        box-shadow: {ds["shadows"]["stokkel"]};
    }}
    
    .stokkel-kpi-number {{
        font-size: {ds["components"]["kpi"]["numberSize"]};
        font-weight: {ds["components"]["kpi"]["numberWeight"]};
        color: {ds["components"]["kpi"]["numberColor"]};
        font-family: var(--font-display);
        line-height: 1;
        margin-bottom: {ds["spacing"]["xs"]};
    }}
    
    .stokkel-kpi-label {{
        font-size: {ds["components"]["kpi"]["labelSize"]};
        color: {ds["components"]["kpi"]["labelColor"]};
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-weight: {ds["typography"]["weights"]["medium"]};
    }}
    
    /* ============================================
       DATA TABLES (Star du show)
       ============================================ */
    
    .stokkel-table {{
        width: 100%;
        border-collapse: separate;
        border-spacing: 0;
        background: white;
        border-radius: 8px;
        overflow: hidden;
        box-shadow: {ds["shadows"]["sm"]};
    }}
    
    .stokkel-table thead {{
        background: {ds["components"]["table"]["headerBg"]};
        color: {ds["components"]["table"]["headerColor"]};
    }}
    
    .stokkel-table th {{
        padding: 16px;
        text-align: left;
        font-weight: {ds["typography"]["weights"]["semibold"]};
        font-size: {ds["typography"]["sizes"]["sm"]};
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }}
    
    .stokkel-table td {{
        padding: 16px;
        border-top: 1px solid {ds["components"]["table"]["borderColor"]};
        font-size: {ds["components"]["table"]["fontSize"]};
        font-family: var(--font-mono);
    }}
    
    .stokkel-table tbody tr:hover {{
        background: {ds["components"]["table"]["rowHoverBg"]};
    }}
    
    /* Streamlit native table styling */
    .stDataFrame {{
        border: 1px solid {ds["colors"]["neutral"]["300"]};
        border-radius: 8px;
        overflow: hidden;
    }}
    
    .stDataFrame thead tr {{
        background: {ds["colors"]["secondary"]["main"]};
        color: white;
    }}
    
    .stDataFrame thead th {{
        padding: 16px !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-size: 13px !important;
    }}
    
    .stDataFrame tbody tr:hover {{
        background: {ds["colors"]["primary"]["subtle"]};
    }}
    
    /* ============================================
       BUTTONS (Clairs, pas de gradients)
       ============================================ */
    
    .stButton button {{
        background: {ds["components"]["button"]["primary"]["bg"]};
        color: {ds["components"]["button"]["primary"]["color"]};
        border: none;
        border-radius: 8px;
        padding: 12px 24px;
        font-weight: {ds["typography"]["weights"]["semibold"]};
        font-size: {ds["typography"]["sizes"]["base"]};
        transition: all 0.25s ease;
        box-shadow: {ds["shadows"]["sm"]};
        font-family: var(--font-sans);
    }}
    
    .stButton button:hover {{
        background: {ds["components"]["button"]["primary"]["hoverBg"]};
        box-shadow: {ds["shadows"]["md"]};
        transform: translateY(-1px);
    }}
    
    .stButton button:active {{
        transform: translateY(0);
    }}
    
    /* Secondary Button */
    .stButton.secondary button {{
        background: {ds["components"]["button"]["secondary"]["bg"]};
        color: {ds["components"]["button"]["secondary"]["color"]};
        border: {ds["components"]["button"]["secondary"]["border"]};
    }}
    
    .stButton.secondary button:hover {{
        background: {ds["components"]["button"]["secondary"]["hoverBg"]};
    }}
    
    /* ============================================
       ALERTS (Style Vekia)
       ============================================ */
    
    .stokkel-alert {{
        padding: {ds["spacing"]["md"]};
        border-radius: 8px;
        border-left: 4px solid;
        display: flex;
        align-items: center;
        gap: {ds["spacing"]["sm"]};
        margin-bottom: {ds["spacing"]["md"]};
    }}
    
    .stokkel-alert-critical {{
        background: {ds["components"]["alert"]["critical"]["bg"]};
        border-color: {ds["components"]["alert"]["critical"]["border"]};
    }}
    
    .stokkel-alert-warning {{
        background: {ds["components"]["alert"]["warning"]["bg"]};
        border-color: {ds["components"]["alert"]["warning"]["border"]};
    }}
    
    .stokkel-alert-success {{
        background: {ds["components"]["alert"]["success"]["bg"]};
        border-color: {ds["components"]["alert"]["success"]["border"]};
    }}
    
    .stokkel-alert-info {{
        background: {ds["components"]["alert"]["info"]["bg"]};
        border-color: {ds["components"]["alert"]["info"]["border"]};
    }}
    
    /* ============================================
       CHARTS (Plotly customization)
       ============================================ */
    
    .js-plotly-plot {{
        border-radius: 8px;
        box-shadow: {ds["shadows"]["sm"]};
    }}
    
    /* ============================================
       FORMS & INPUTS
       ============================================ */
    
    .stTextInput input,
    .stNumberInput input,
    .stSelectbox select {{
        border: 2px solid {ds["colors"]["neutral"]["300"]};
        border-radius: 8px;
        padding: 12px 16px;
        font-size: {ds["typography"]["sizes"]["base"]};
        font-family: var(--font-sans);
        transition: all 0.25s ease;
    }}
    
    .stTextInput input:focus,
    .stNumberInput input:focus,
    .stSelectbox select:focus {{
        border-color: {ds["colors"]["primary"]["main"]};
        box-shadow: 0 0 0 3px {ds["colors"]["primary"]["subtle"]};
        outline: none;
    }}
    
    /* ============================================
       METRICS (Streamlit st.metric)
       ============================================ */
    
    [data-testid="stMetricValue"] {{
        font-size: {ds["typography"]["sizes"]["4xl"]};
        font-weight: {ds["typography"]["weights"]["bold"]};
        color: {ds["colors"]["primary"]["main"]};
        font-family: var(--font-display);
    }}
    
    [data-testid="stMetricLabel"] {{
        font-size: {ds["typography"]["sizes"]["sm"]};
        color: {ds["colors"]["neutral"]["600"]};
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-weight: {ds["typography"]["weights"]["medium"]};
    }}
    
    [data-testid="stMetricDelta"] {{
        font-size: {ds["typography"]["sizes"]["base"]};
        font-family: var(--font-mono);
    }}
    
    /* ============================================
       EXPANDERS (Accordéons)
       ============================================ */
    
    .streamlit-expanderHeader {{
        background: {ds["colors"]["neutral"]["100"]};
        border-radius: 8px;
        padding: 16px;
        font-weight: {ds["typography"]["weights"]["semibold"]};
        transition: all 0.25s ease;
    }}
    
    .streamlit-expanderHeader:hover {{
        background: {ds["colors"]["primary"]["subtle"]};
        color: {ds["colors"]["primary"]["dark"]};
    }}
    
    /* ============================================
       FILE UPLOADER
       ============================================ */
    
    .stFileUploader {{
        border: 2px dashed {ds["colors"]["primary"]["light"]};
        border-radius: 12px;
        padding: {ds["spacing"]["2xl"]};
        background: {ds["colors"]["primary"]["subtle"]};
        transition: all 0.25s ease;
    }}
    
    .stFileUploader:hover {{
        border-color: {ds["colors"]["primary"]["main"]};
        background: white;
    }}
    
    /* ============================================
       TABS
       ============================================ */
    
    .stTabs [data-baseweb="tab-list"] {{
        gap: {ds["spacing"]["sm"]};
        border-bottom: 2px solid {ds["colors"]["neutral"]["300"]};
    }}
    
    .stTabs [data-baseweb="tab"] {{
        padding: 12px 24px;
        border-radius: 8px 8px 0 0;
        font-weight: {ds["typography"]["weights"]["semibold"]};
        color: {ds["colors"]["neutral"]["600"]};
        transition: all 0.25s ease;
    }}
    
    .stTabs [data-baseweb="tab"]:hover {{
        background: {ds["colors"]["neutral"]["100"]};
        color: {ds["colors"]["primary"]["main"]};
    }}
    
    .stTabs [aria-selected="true"] {{
        background: {ds["colors"]["primary"]["main"]};
        color: white;
    }}
    
    /* ============================================
       CUSTOM UTILITY CLASSES
       ============================================ */
    
    .text-primary {{
        color: {ds["colors"]["primary"]["main"]};
    }}
    
    .text-secondary {{
        color: {ds["colors"]["secondary"]["main"]};
    }}
    
    .bg-subtle {{
        background: {ds["colors"]["neutral"]["50"]};
    }}
    
    .font-mono {{
        font-family: var(--font-mono);
    }}
    
    .font-display {{
        font-family: var(--font-display);
    }}
    
    /* ============================================
       RESPONSIVE DESIGN
       ============================================ */
    
    @media (max-width: 768px) {{
        h1 {{
            font-size: {ds["typography"]["sizes"]["3xl"]};
        }}
        
        h2 {{
            font-size: {ds["typography"]["sizes"]["2xl"]};
        }}
        
        .stokkel-card {{
            padding: {ds["spacing"]["md"]};
        }}
    }}
    
    /* ============================================
       ANIMATIONS SUBTILES
       ============================================ */
    
    @keyframes fadeInUp {{
        from {{
            opacity: 0;
            transform: translateY(20px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}
    
    .animate-fade-in-up {{
        animation: fadeInUp 0.5s ease-out;
    }}
    
    /* ============================================
       SCROLLBAR CUSTOM
       ============================================ */
    
    ::-webkit-scrollbar {{
        width: 10px;
        height: 10px;
    }}
    
    ::-webkit-scrollbar-track {{
        background: {ds["colors"]["neutral"]["100"]};
    }}
    
    ::-webkit-scrollbar-thumb {{
        background: {ds["colors"]["primary"]["light"]};
        border-radius: 5px;
    }}
    
    ::-webkit-scrollbar-thumb:hover {{
        background: {ds["colors"]["primary"]["main"]};
    }}
    
    </style>
    """
    
    return css


# ============================================
# HELPER FUNCTIONS
# ============================================

def create_kpi_card(label, value, delta=None, icon="📊"):
    """
    Crée une KPI card style Stokkel
    
    Args:
        label: Libellé du KPI
        value: Valeur principale
        delta: Changement (optionnel)
        icon: Emoji icon
    """
    
    delta_html = ""
    if delta:
        delta_color = "#2A9D8F" if delta >= 0 else "#D32F2F"
        delta_symbol = "↑" if delta >= 0 else "↓"
        delta_html = f'<div style="color: {delta_color}; font-size: 16px; margin-top: 8px;">{delta_symbol} {abs(delta)}%</div>'
    
    return f"""
    <div class="stokkel-kpi">
        <div style="font-size: 32px; margin-bottom: 8px;">{icon}</div>
        <div class="stokkel-kpi-number">{value}</div>
        <div class="stokkel-kpi-label">{label}</div>
        {delta_html}
    </div>
    """


def create_alert(message, alert_type="info"):
    """
    Crée une alerte style Vekia
    
    Args:
        message: Message de l'alerte
        alert_type: Type (critical, warning, success, info)
    """
    
    icons = {
        "critical": "🚨",
        "warning": "⚠️",
        "success": "✅",
        "info": "ℹ️",
    }
    
    icon = icons.get(alert_type, "ℹ️")
    
    return f"""
    <div class="stokkel-alert stokkel-alert-{alert_type}">
        <span style="font-size: 24px;">{icon}</span>
        <span style="font-weight: 500;">{message}</span>
    </div>
    """


def create_section_header(title, subtitle=None):
    """
    Crée un header de section style Stokkel
    """
    
    subtitle_html = ""
    if subtitle:
        subtitle_html = f'<p style="color: #6B6B6B; font-size: 16px; margin-top: 8px;">{subtitle}</p>'
    
    return f"""
    <div style="margin-bottom: 32px;">
        <h2 style="color: #1B4965; font-size: 30px; font-weight: 600; margin-bottom: 8px; border-left: 4px solid #D2691E; padding-left: 16px;">
            {title}
        </h2>
        {subtitle_html}
    </div>
    """
