"""
Styles CSS personnalisés pour Stokkel Dashboard - Design Moderne
Version 2.0 - Startup Grade Design
"""

import streamlit as st

def apply_custom_styles():
    """Applique les styles CSS personnalisés ultra-modernes"""
    st.markdown("""
        <style>
        /* Import de Google Fonts - Plus modernes */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Poppins:wght@600;700;800&display=swap');

        /* Variables CSS - Palette Moderne */
        :root {
            --primary-color: #6366f1;
            --primary-dark: #4f46e5;
            --primary-light: #818cf8;
            --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            --primary-gradient-soft: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
            --success-color: #10b981;
            --success-light: #34d399;
            --warning-color: #f59e0b;
            --warning-light: #fbbf24;
            --danger-color: #ef4444;
            --danger-light: #f87171;
            --info-color: #3b82f6;
            --gray-50: #fafafa;
            --gray-100: #f5f5f5;
            --gray-200: #e5e5e5;
            --gray-300: #d4d4d4;
            --gray-400: #a3a3a3;
            --gray-500: #737373;
            --gray-600: #525252;
            --gray-700: #404040;
            --gray-800: #262626;
            --gray-900: #171717;
            --border-radius: 1rem;
            --border-radius-lg: 1.5rem;
            --border-radius-full: 9999px;
            --shadow-xs: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
            --shadow-sm: 0 2px 4px 0 rgba(0, 0, 0, 0.06);
            --shadow-md: 0 4px 12px -2px rgba(0, 0, 0, 0.08);
            --shadow-lg: 0 10px 25px -5px rgba(0, 0, 0, 0.1);
            --shadow-xl: 0 20px 40px -10px rgba(0, 0, 0, 0.15);
            --shadow-2xl: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
            --glass-bg: rgba(255, 255, 255, 0.7);
            --glass-border: rgba(255, 255, 255, 0.18);
        }
        
        /* Reset et base */
        * {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }

        /* Main container avec dégradé moderne */
        .main {
            padding: 2rem 3rem;
            background: linear-gradient(135deg, #667eea08 0%, #764ba208 50%, #f093fb05 100%);
            min-height: 100vh;
            position: relative;
        }

        /* Background pattern subtil */
        .main::before {
            content: "";
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-image:
                radial-gradient(circle at 20% 50%, rgba(102, 126, 234, 0.03) 0%, transparent 50%),
                radial-gradient(circle at 80% 80%, rgba(118, 75, 162, 0.03) 0%, transparent 50%);
            pointer-events: none;
            z-index: 0;
        }

        /* Headers ultra-modernes */
        .main-header {
            font-family: 'Poppins', sans-serif;
            font-size: 3.5rem;
            font-weight: 800;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            text-align: center;
            margin-bottom: 0.75rem;
            letter-spacing: -0.03em;
            line-height: 1.1;
            animation: fadeInUp 0.6s ease-out;
        }

        .sub-header {
            font-size: 1.25rem;
            color: var(--gray-600);
            text-align: center;
            margin-bottom: 3rem;
            font-weight: 500;
            animation: fadeInUp 0.6s ease-out 0.1s backwards;
            line-height: 1.6;
        }

        h2 {
            font-family: 'Poppins', sans-serif;
            color: var(--gray-900);
            font-weight: 700;
            margin-bottom: 1.5rem;
            padding-bottom: 0.75rem;
            border-bottom: 3px solid transparent;
            background: linear-gradient(to right, var(--primary-color) 0%, transparent 100%) left bottom no-repeat;
            background-size: 100% 3px;
            position: relative;
        }

        h2::before {
            content: "";
            position: absolute;
            bottom: -3px;
            left: 0;
            width: 60px;
            height: 3px;
            background: var(--primary-gradient);
            border-radius: 2px;
        }

        h3 {
            font-family: 'Poppins', sans-serif;
            color: var(--gray-800);
            font-weight: 600;
            margin: 1.5rem 0 1rem 0;
            letter-spacing: -0.01em;
        }
        
        /* Cards avec Glassmorphism ultra-moderne */
        .metric-card {
            background: var(--glass-bg);
            backdrop-filter: blur(20px) saturate(180%);
            -webkit-backdrop-filter: blur(20px) saturate(180%);
            padding: 2rem;
            border-radius: var(--border-radius-lg);
            border: 1px solid var(--glass-border);
            box-shadow: var(--shadow-md);
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            height: 100%;
            position: relative;
            overflow: hidden;
        }

        .metric-card::before {
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: var(--primary-gradient);
            transform: scaleX(0);
            transform-origin: left;
            transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        }

        .metric-card:hover {
            box-shadow: var(--shadow-xl);
            transform: translateY(-8px) scale(1.02);
            border-color: rgba(102, 126, 234, 0.3);
            background: rgba(255, 255, 255, 0.9);
        }

        .metric-card:hover::before {
            transform: scaleX(1);
        }

        .metric-card h3 {
            font-family: 'Poppins', sans-serif;
            background: var(--primary-gradient);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-size: 1.125rem;
            font-weight: 700;
            margin: 0 0 0.75rem 0;
            border: none;
        }

        .metric-card p {
            color: var(--gray-700);
            font-size: 0.9375rem;
            margin: 0;
            line-height: 1.7;
            font-weight: 500;
        }

        /* Feature cards - Design premium */
        .feature-card {
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.9) 0%, rgba(255, 255, 255, 0.7) 100%);
            backdrop-filter: blur(20px);
            padding: 2.5rem;
            border-radius: var(--border-radius-lg);
            border: 2px solid transparent;
            background-clip: padding-box;
            box-shadow: var(--shadow-lg);
            transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
            cursor: pointer;
            position: relative;
            overflow: hidden;
        }

        .feature-card::after {
            content: "";
            position: absolute;
            inset: 0;
            border-radius: var(--border-radius-lg);
            padding: 2px;
            background: var(--primary-gradient);
            -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
            -webkit-mask-composite: xor;
            mask-composite: exclude;
            opacity: 0;
            transition: opacity 0.4s ease;
        }

        .feature-card:hover {
            box-shadow: var(--shadow-2xl);
            transform: translateY(-12px) scale(1.03);
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(255, 255, 255, 0.85) 100%);
        }

        .feature-card:hover::after {
            opacity: 1;
        }

        .feature-icon {
            font-size: 3.5rem;
            margin-bottom: 1.25rem;
            filter: drop-shadow(0 4px 8px rgba(102, 126, 234, 0.2));
            animation: float 3s ease-in-out infinite;
        }
        
        /* Alert boxes - Design moderne avec glow effect */
        .alert-box {
            padding: 1.5rem 1.75rem;
            border-radius: var(--border-radius);
            margin-bottom: 1.5rem;
            border-left: 4px solid;
            box-shadow: var(--shadow-md);
            animation: slideInRight 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            backdrop-filter: blur(10px);
            position: relative;
            overflow: hidden;
        }

        .alert-box::before {
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            opacity: 0.05;
            background: linear-gradient(45deg, transparent 30%, white 50%, transparent 70%);
            transform: translateX(-100%);
        }

        .alert-box:hover::before {
            animation: shimmer 2s infinite;
        }

        @keyframes slideInRight {
            from {
                opacity: 0;
                transform: translateX(-30px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }

        @keyframes shimmer {
            to {
                transform: translateX(100%);
            }
        }
        
        .alert-critical {
            background-color: #fef2f2;
            border-color: var(--danger-color);
            color: #991b1b;
        }
        
        .alert-warning {
            background-color: #fffbeb;
            border-color: var(--warning-color);
            color: #92400e;
        }
        
        .alert-success {
            background-color: #f0fdf4;
            border-color: var(--success-color);
            color: #065f46;
        }
        
        .alert-info {
            background-color: #eff6ff;
            border-color: var(--primary-color);
            color: #1e40af;
        }
        
        /* Buttons ultra-modernes avec glow effect */
        .stButton > button {
            background: var(--primary-gradient);
            color: white;
            border-radius: var(--border-radius-full);
            padding: 0.875rem 2rem;
            border: none;
            font-weight: 600;
            font-size: 1rem;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 4px 14px 0 rgba(102, 126, 234, 0.39);
            width: 100%;
            position: relative;
            overflow: hidden;
            cursor: pointer;
            letter-spacing: 0.02em;
        }

        .stButton > button::before {
            content: "";
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
            transition: left 0.5s;
        }

        .stButton > button:hover::before {
            left: 100%;
        }

        .stButton > button:hover {
            background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
            box-shadow: 0 8px 24px 0 rgba(102, 126, 234, 0.5);
            transform: translateY(-3px) scale(1.02);
        }

        .stButton > button:active {
            transform: translateY(-1px) scale(0.98);
            box-shadow: 0 4px 12px 0 rgba(102, 126, 234, 0.4);
        }

        /* Primary button variant */
        .stButton > button[kind="primary"] {
            background: var(--primary-gradient);
            box-shadow: 0 6px 20px 0 rgba(102, 126, 234, 0.45);
        }

        .stButton > button[kind="primary"]:hover {
            box-shadow: 0 10px 30px 0 rgba(102, 126, 234, 0.6);
        }

        /* Secondary button - Modern outline */
        .stButton > button[kind="secondary"] {
            background: transparent;
            color: var(--primary-color);
            border: 2px solid var(--primary-color);
            box-shadow: none;
        }

        .stButton > button[kind="secondary"]:hover {
            background: var(--primary-gradient-soft);
            border-color: var(--primary-light);
            color: var(--primary-dark);
        }
        
        /* Metrics - Design premium */
        [data-testid="stMetricValue"] {
            font-family: 'Poppins', sans-serif;
            font-size: 2.5rem;
            font-weight: 800;
            background: var(--primary-gradient);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            letter-spacing: -0.02em;
        }

        [data-testid="stMetricLabel"] {
            font-size: 0.8125rem;
            font-weight: 600;
            color: var(--gray-600);
            text-transform: uppercase;
            letter-spacing: 0.08em;
            margin-bottom: 0.5rem !important;
        }

        [data-testid="stMetricDelta"] {
            font-size: 0.875rem;
            font-weight: 700;
            padding: 0.25rem 0.75rem;
            border-radius: var(--border-radius-full);
            backdrop-filter: blur(10px);
        }

        /* Delta positive */
        [data-testid="stMetricDelta"] svg[fill*="green"],
        [data-testid="stMetricDelta"]:has(svg[fill*="green"]) {
            background: rgba(16, 185, 129, 0.1);
            color: var(--success-color) !important;
        }

        /* Delta negative */
        [data-testid="stMetricDelta"] svg[fill*="red"],
        [data-testid="stMetricDelta"]:has(svg[fill*="red"]) {
            background: rgba(239, 68, 68, 0.1);
            color: var(--danger-color) !important;
        }
        
        /* DataFrames */
        .dataframe {
            border: 1px solid var(--gray-200) !important;
            border-radius: var(--border-radius);
            overflow: hidden;
        }
        
        .dataframe th {
            background: var(--gray-100) !important;
            color: var(--gray-700) !important;
            font-weight: 600 !important;
            text-transform: uppercase;
            font-size: 0.75rem;
            letter-spacing: 0.05em;
            padding: 0.75rem !important;
        }
        
        .dataframe td {
            padding: 0.75rem !important;
            border-bottom: 1px solid var(--gray-200) !important;
        }
        
        .dataframe tr:hover {
            background-color: var(--gray-50) !important;
        }
        
        /* Inputs */
        .stTextInput > div > div > input,
        .stNumberInput > div > div > input,
        .stSelectbox > div > div > select {
            border-radius: var(--border-radius);
            border: 2px solid var(--gray-200);
            padding: 0.75rem;
            font-size: 1rem;
            transition: all 0.2s ease;
        }
        
        .stTextInput > div > div > input:focus,
        .stNumberInput > div > div > input:focus,
        .stSelectbox > div > div > select:focus {
            border-color: var(--primary-color);
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
        }
        
        /* File uploader */
        [data-testid="stFileUploader"] {
            background: white;
            border: 2px dashed var(--gray-300);
            border-radius: var(--border-radius);
            padding: 2rem;
            text-align: center;
            transition: all 0.3s ease;
        }
        
        [data-testid="stFileUploader"]:hover {
            border-color: var(--primary-color);
            background: var(--gray-50);
        }
        
        /* Sidebar ultra-moderne avec glassmorphism */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #1e1b4b 0%, #312e81 50%, #4c1d95 100%);
            padding: 1.5rem 1rem;
            position: relative;
            overflow: hidden;
        }

        [data-testid="stSidebar"]::before {
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background:
                radial-gradient(circle at 30% 20%, rgba(139, 92, 246, 0.1) 0%, transparent 50%),
                radial-gradient(circle at 70% 80%, rgba(236, 72, 153, 0.1) 0%, transparent 50%);
            pointer-events: none;
        }

        [data-testid="stSidebar"] .css-1d391kg {
            color: white;
        }

        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3 {
            color: white;
            text-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
        }

        /* Sidebar buttons avec effet neon */
        [data-testid="stSidebar"] .stButton > button {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            color: white;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: none;
        }

        [data-testid="stSidebar"] .stButton > button:hover {
            background: rgba(255, 255, 255, 0.2);
            border-color: rgba(255, 255, 255, 0.4);
            transform: translateX(5px);
            box-shadow: 0 0 20px rgba(139, 92, 246, 0.3);
        }

        /* Primary button in sidebar */
        [data-testid="stSidebar"] .stButton > button[kind="primary"],
        [data-testid="stSidebar"] .stButton > button[data-baseweb="button"][kind="primary"] {
            background: var(--primary-gradient) !important;
            border: none !important;
            box-shadow: 0 4px 15px rgba(139, 92, 246, 0.4) !important;
        }

        [data-testid="stSidebar"] .stButton > button[kind="primary"]:hover {
            box-shadow: 0 6px 20px rgba(139, 92, 246, 0.6) !important;
            transform: translateX(5px) scale(1.02) !important;
        }
        
        /* Expander */
        .streamlit-expanderHeader {
            background-color: var(--gray-50);
            border-radius: var(--border-radius);
            font-weight: 600;
            color: var(--gray-700);
        }
        
        .streamlit-expanderHeader:hover {
            background-color: var(--gray-100);
        }
        
        /* Tabs ultra-modernes */
        .stTabs [data-baseweb="tab-list"] {
            gap: 0.75rem;
            background: rgba(255, 255, 255, 0.6);
            backdrop-filter: blur(10px);
            border-radius: var(--border-radius-lg);
            padding: 0.5rem;
            border: 1px solid var(--glass-border);
            box-shadow: var(--shadow-sm);
        }

        .stTabs [data-baseweb="tab"] {
            border-radius: var(--border-radius);
            padding: 0.875rem 2rem;
            font-weight: 600;
            color: var(--gray-600);
            background-color: transparent;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
        }

        .stTabs [data-baseweb="tab"]::after {
            content: "";
            position: absolute;
            bottom: 0;
            left: 50%;
            width: 0;
            height: 3px;
            background: var(--primary-gradient);
            border-radius: 2px;
            transform: translateX(-50%);
            transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }

        .stTabs [data-baseweb="tab"]:hover {
            background-color: rgba(102, 126, 234, 0.05);
            color: var(--primary-color);
        }

        .stTabs [aria-selected="true"] {
            background: white;
            color: var(--primary-color);
            box-shadow: var(--shadow-md);
            font-weight: 700;
        }

        .stTabs [aria-selected="true"]::after {
            width: 80%;
        }
        
        /* Progress bar */
        .stProgress > div > div > div > div {
            background: linear-gradient(90deg, var(--primary-color) 0%, var(--primary-light) 100%);
        }
        
        /* Spinner */
        .stSpinner > div {
            border-top-color: var(--primary-color) !important;
        }
        
        /* Success/Error messages */
        .stSuccess {
            background-color: #f0fdf4;
            color: #065f46;
            border-left: 4px solid var(--success-color);
            border-radius: var(--border-radius);
            padding: 1rem;
        }
        
        .stError {
            background-color: #fef2f2;
            color: #991b1b;
            border-left: 4px solid var(--danger-color);
            border-radius: var(--border-radius);
            padding: 1rem;
        }
        
        .stWarning {
            background-color: #fffbeb;
            color: #92400e;
            border-left: 4px solid var(--warning-color);
            border-radius: var(--border-radius);
            padding: 1rem;
        }
        
        .stInfo {
            background-color: #eff6ff;
            color: #1e40af;
            border-left: 4px solid var(--primary-color);
            border-radius: var(--border-radius);
            padding: 1rem;
        }
        
        /* Loading skeleton */
        .skeleton {
            background: linear-gradient(90deg, var(--gray-200) 25%, var(--gray-100) 50%, var(--gray-200) 75%);
            background-size: 200% 100%;
            animation: loading 1.5s ease-in-out infinite;
            border-radius: var(--border-radius);
        }
        
        @keyframes loading {
            0% { background-position: 200% 0; }
            100% { background-position: -200% 0; }
        }
        
        /* Charts */
        .js-plotly-plot {
            border-radius: var(--border-radius);
            box-shadow: var(--shadow-sm);
        }
        
        /* Status badges */
        .status-badge {
            display: inline-block;
            padding: 0.25rem 0.75rem;
            border-radius: 9999px;
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        
        .status-critical {
            background-color: #fef2f2;
            color: var(--danger-color);
        }
        
        .status-warning {
            background-color: #fffbeb;
            color: var(--warning-color);
        }
        
        .status-success {
            background-color: #f0fdf4;
            color: var(--success-color);
        }
        
        /* Tooltips */
        [data-testid="stTooltipIcon"] {
            color: var(--gray-400);
        }
        
        /* Scrollbar */
        ::-webkit-scrollbar {
            width: 10px;
            height: 10px;
        }
        
        ::-webkit-scrollbar-track {
            background: var(--gray-100);
            border-radius: 10px;
        }
        
        ::-webkit-scrollbar-thumb {
            background: var(--gray-300);
            border-radius: 10px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: var(--gray-400);
        }
        
        /* Animations ultra-modernes */
        @keyframes fadeIn {
            from {
                opacity: 0;
            }
            to {
                opacity: 1;
            }
        }

        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        @keyframes fadeInDown {
            from {
                opacity: 0;
                transform: translateY(-30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        @keyframes float {
            0%, 100% {
                transform: translateY(0);
            }
            50% {
                transform: translateY(-10px);
            }
        }

        @keyframes pulse {
            0%, 100% {
                opacity: 1;
                transform: scale(1);
            }
            50% {
                opacity: 0.8;
                transform: scale(1.05);
            }
        }

        @keyframes slideInLeft {
            from {
                opacity: 0;
                transform: translateX(-50px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }

        @keyframes scaleIn {
            from {
                opacity: 0;
                transform: scale(0.9);
            }
            to {
                opacity: 1;
                transform: scale(1);
            }
        }

        @keyframes rotate {
            from {
                transform: rotate(0deg);
            }
            to {
                transform: rotate(360deg);
            }
        }

        @keyframes gradient-shift {
            0% {
                background-position: 0% 50%;
            }
            50% {
                background-position: 100% 50%;
            }
            100% {
                background-position: 0% 50%;
            }
        }

        .fade-in {
            animation: fadeIn 0.6s ease-out;
        }

        .fade-in-up {
            animation: fadeInUp 0.6s ease-out;
        }

        .slide-in-left {
            animation: slideInLeft 0.6s ease-out;
        }

        .scale-in {
            animation: scaleIn 0.6s ease-out;
        }
        
        /* Responsive */
        @media (max-width: 768px) {
            .main-header {
                font-size: 2rem;
            }
            
            .sub-header {
                font-size: 1rem;
            }
            
            .metric-card {
                padding: 1rem;
            }
        }
        </style>
    """, unsafe_allow_html=True)


def render_page_header(title: str, subtitle: str = "", icon: str = ""):
    """Render un header de page standardisé"""
    if icon:
        st.markdown(f'<h1 class="main-header">{icon} {title}</h1>', unsafe_allow_html=True)
    else:
        st.markdown(f'<h1 class="main-header">{title}</h1>', unsafe_allow_html=True)
    
    if subtitle:
        st.markdown(f'<p class="sub-header">{subtitle}</p>', unsafe_allow_html=True)


def render_metric_card(title: str, content: str, icon: str = ""):
    """Render une carte métrique"""
    icon_html = f'<span class="feature-icon">{icon}</span>' if icon else ''
    st.markdown(f"""
        <div class="metric-card">
            {icon_html}
            <h3>{title}</h3>
            <p>{content}</p>
        </div>
    """, unsafe_allow_html=True)


def render_alert(message: str, alert_type: str = "info", title: str = ""):
    """
    Render une alerte stylisée
    
    Args:
        message: Message à afficher
        alert_type: Type d'alerte ('critical', 'warning', 'success', 'info')
        title: Titre optionnel
    """
    icons = {
        'critical': '🔴',
        'warning': '🟡',
        'success': '🟢',
        'info': 'ℹ️'
    }
    
    icon = icons.get(alert_type, 'ℹ️')
    title_html = f'<strong>{icon} {title}</strong><br>' if title else f'<strong>{icon}</strong> '
    
    st.markdown(f"""
        <div class="alert-box alert-{alert_type}">
            {title_html}{message}
        </div>
    """, unsafe_allow_html=True)


def render_status_badge(text: str, status: str = "success"):
    """Render un badge de statut"""
    return f'<span class="status-badge status-{status}">{text}</span>'