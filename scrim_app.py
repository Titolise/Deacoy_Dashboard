import streamlit as st
import pymongo
import requests
import os
import base64
import json
import certifi  # REQUIRED: pip install certifi

# Page configuration
st.set_page_config(
    page_title="Deacoy Dashboard", 
    page_icon="logo.png", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# Initialize session state
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# Enhanced Authentication System
def check_password():
    """Professional authentication with enhanced UX"""
    if st.session_state.authenticated:
        return True
    
    # Safety check for secrets
    if "auth" not in st.secrets:
        st.error("⚠️ Secrets configuration error: 'auth' section missing.")
        return False
        
    def password_entered():
        if st.session_state["password"] == st.secrets["auth"]["password"]:
            st.session_state["authenticated"] = True
            del st.session_state["password"]
        else:
            st.session_state["authenticated"] = False

    # Professional login styling - Updated to Deep Violet Theme
    st.markdown("""
    <style>
        .login-container {
            background: linear-gradient(135deg, #050505 0%, #1a1025 50%, #2e1065 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        }
        
        .login-card {
            background: rgba(20, 10, 30, 0.4);
            backdrop-filter: blur(40px);
            border: 1px solid rgba(139, 92, 246, 0.1);
            border-radius: 24px;
            padding: 4rem 3rem;
            box-shadow: 
                0 8px 32px rgba(0, 0, 0, 0.6),
                0 0 0 1px rgba(139, 92, 246, 0.1) inset;
            text-align: center;
            max-width: 480px;
            width: 100%;
            position: relative;
        }
        
        .login-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 1px;
            background: linear-gradient(90deg, transparent, rgba(139, 92, 246, 0.5), transparent);
        }
        
        .login-header {
            margin-bottom: 3rem;
            display: flex;
            flex-direction: row;
            align-items: center;
            justify-content: center;
            gap: 1.5rem;
        }
        
        .login-logo {
            width: 70px;
            height: 70px;
            border-radius: 50%;
            border: 2px solid #8b5cf6;
            box-shadow: 0 4px 15px rgba(139, 92, 246, 0.4);
            object-fit: cover;
            order: 2;
        }
        
        .login-logo-placeholder {
            width: 70px;
            height: 70px;
            border-radius: 50%;
            border: 2px solid #8b5cf6;
            box-shadow: 0 4px 15px rgba(139, 92, 246, 0.4);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 2rem;
            background: linear-gradient(135deg, #7c3aed 0%, #a78bfa 100%);
            order: 2;
        }
        
        .login-text {
            order: 1;
            text-align: left;
        }
        
        .login-title {
            background: linear-gradient(135deg, #a78bfa 0%, #c4b5fd 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-size: 3rem;
            font-weight: 700;
            margin: 0 0 0.5rem 0;
            line-height: 1.1;
            letter-spacing: -0.02em;
            text-shadow: 0 0 30px rgba(139, 92, 246, 0.3);
        }
        
        .login-subtitle {
            color: rgba(255, 255, 255, 0.6);
            margin: 0;
            font-size: 1.1rem;
            font-weight: 400;
            letter-spacing: 0.02em;
        }
        
        .stTextInput > div > div > input {
            background: rgba(0, 0, 0, 0.2) !important;
            border: 1px solid rgba(139, 92, 246, 0.2) !important;
            border-radius: 16px !important;
            color: rgba(255, 255, 255, 0.9) !important;
            padding: 1.25rem 1.5rem !important;
            font-size: 1rem !important;
            text-align: center !important;
            transition: all 0.3s ease !important;
        }
        
        .stTextInput > div > div > input:focus {
            border-color: #8b5cf6 !important;
            box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.2) !important;
            background: rgba(139, 92, 246, 0.1) !important;
        }
        
        .stTextInput > div > div > input::placeholder {
            color: rgba(255, 255, 255, 0.4) !important;
        }
    </style>
    """, unsafe_allow_html=True)

    # Login form
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            # Try to load logo for login page
            try:
                import base64
                import os
                if os.path.exists("logo.png"):
                    with open("logo.png", "rb") as f:
                        logo_data = base64.b64encode(f.read()).decode()
                    logo_html = f'<img src="data:image/png;base64,{logo_data}" class="login-logo" alt="Deacoy Logo">'
                else:
                    logo_html = '<div class="login-logo-placeholder">⚡</div>'
            except:
                logo_html = '<div class="login-logo-placeholder">⚡</div>'
            
            st.markdown(f"""
            <div class="login-card">
                <div class="login-header">
                    <div class="login-text">
                        <h1 class="login-title">Deacoy</h1>
                        <p class="login-subtitle">LIT Dashboard</p>
                    </div>
                    {logo_html}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.text_input("", type="password", key="password", on_change=password_entered, placeholder="Enter access code...")
            
            if "password" in st.session_state and st.session_state.get("password"):
                if not st.session_state.authenticated:
                    st.error("Access denied. Please check your credentials.")

    return st.session_state.authenticated

# Stop execution if not authenticated
if not check_password():
    st.stop()

# Professional CSS Framework - UPDATED TO DEEP VIOLET THEME
st.markdown("""
<style>
    /* Professional Design System Variables - Violet/Dark Theme */
    :root {
        /* Base Backgrounds */
        --bg-primary: #09090b;   /* Very dark zinc/black */
        --bg-secondary: #18181b; /* Dark zinc */
        --bg-card: #27272a;      /* Lighter zinc for cards */
        
        /* Main Accent (Violet/Purple) */
        --accent-primary: #8b5cf6;   /* Violet 500 */
        --accent-secondary: #a78bfa; /* Violet 400 */
        --accent-tertiary: #7c3aed;  /* Violet 600 */
        
        /* Text Colors */
        --text-primary: #f8fafc;
        --text-secondary: #a1a1aa;
        --text-muted: #71717a;
        
        /* Status Colors */
        --success: #10b981; /* Emerald 500 */
        --warning: #f59e0b; /* Amber 500 */
        --danger: #ef4444;  /* Red 500 */
        
        /* Borders & Shadows */
        --border: #3f3f46;
        --shadow: rgba(0, 0, 0, 0.4);
        
        /* Primary Palette (Violet) */
        --primary-50: #f5f3ff;
        --primary-100: #ede9fe;
        --primary-200: #ddd6fe;
        --primary-300: #c4b5fd;
        --primary-400: #a78bfa;
        --primary-500: #8b5cf6;
        --primary-600: #7c3aed;
        --primary-700: #6d28d9;
        --primary-800: #5b21b6;
        --primary-900: #4c1d95;
        
        /* Neutrals (Zinc) */
        --neutral-50: #fafafa;
        --neutral-100: #f4f4f5;
        --neutral-200: #e4e4e7;
        --neutral-300: #d4d4d8;
        --neutral-400: #a1a1aa;
        --neutral-500: #71717a;
        --neutral-600: #52525b;
        --neutral-700: #3f3f46;
        --neutral-800: #27272a;
        --neutral-900: #18181b;
        
        --success-500: #10b981;
        --warning-500: #f59e0b;
        --error-500: #ef4444;
        
        --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
        --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
        
        --radius-sm: 8px;
        --radius-md: 12px;
        --radius-lg: 16px;
        --radius-xl: 24px;
        
        --spacing-xs: 0.25rem;
        --spacing-sm: 0.5rem;
        --spacing-md: 1rem;
        --spacing-lg: 1.5rem;
        --spacing-xl: 2rem;
        --spacing-2xl: 3rem;
    }
    
    /* Global Styles */
    .stApp {
        background: radial-gradient(circle at top center, #1e1b2e 0%, var(--bg-primary) 100%);
        color: var(--text-primary);
        font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }
    
    .main .block-container {
        padding: var(--spacing-xl) var(--spacing-lg);
        max-width: 1400px;
    }
    
    /* Modern Typography */
    h1, h2, h3, h4 {
        color: var(--text-primary);
        font-weight: 700;
        line-height: 1.2;
        letter-spacing: -0.025em;
    }
    
    h1 {
        text-align: center;
        font-size: clamp(2rem, 4vw, 3rem);
        background: linear-gradient(135deg, var(--accent-secondary), var(--accent-primary));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        padding-bottom: 2rem;
        margin-bottom: 3rem;
        position: relative;
        text-shadow: 0 0 40px rgba(139, 92, 246, 0.3);
    }
    
    h1::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 50%;
        transform: translateX(-50%);
        width: 100px;
        height: 3px;
        background: linear-gradient(90deg, transparent, var(--accent-primary), transparent);
        border-radius: 2px;
        box-shadow: 0 0 10px var(--accent-primary);
    }
    
    h2 {
        font-size: 1.75rem;
        color: var(--accent-secondary);
        margin: 2.5rem 0 1.5rem 0;
        padding-bottom: 0.75rem;
        border-bottom: 2px solid var(--border);
        position: relative;
    }
    
    h3 {
        font-size: 1.5rem;
        color: var(--text-primary);
        margin: 2rem 0 1rem 0;
    }
    
    /* Professional Glass Morphism Cards */
    .stat-card, .modern-card {
        background: rgba(30, 30, 40, 0.4);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(139, 92, 246, 0.1);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        position: relative;
        overflow: hidden;
        transition: all 0.3s ease;
    }
    
    .stat-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(139, 92, 246, 0.3), transparent);
    }
    
    .stat-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.4), 0 10px 10px -5px rgba(0, 0, 0, 0.3);
        border-color: rgba(139, 92, 246, 0.3);
    }
    
    /* Enhanced Team Colors */
    .gmb-blue {
        color: var(--accent-secondary) !important;
        font-weight: 600;
        text-shadow: 0 0 10px rgba(139, 92, 246, 0.4);
    }
    
    .opponent-red {
        color: var(--danger) !important;
        font-weight: 600;
        text-shadow: 0 0 10px rgba(239, 68, 68, 0.3);
    }
    
    .win {
        color: var(--success) !important;
        font-weight: 700;
        text-shadow: 0 0 10px rgba(16, 185, 129, 0.3);
    }
    
    .loss {
        color: var(--danger) !important;
        font-weight: 700;
        text-shadow: 0 0 10px rgba(239, 68, 68, 0.3);
    }
    
    /* Modern Sidebar Enhancement */
    .css-1d391kg, [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(20, 20, 25, 0.9) 0%, rgba(10, 10, 15, 0.95) 100%);
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(139, 92, 246, 0.1);
    }
    
    .css-1d391kg .css-17eq0hr, [data-testid="stSidebar"] .css-17eq0hr {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        border-radius: 12px;
        margin-bottom: 1rem;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    /* Sidebar Header Centering */
    .sidebar-header {
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        padding: 1rem 0;
        gap: 0.5rem;
    }
    
    .sidebar-header img {
        display: block;
        margin: 0 auto;
        border: 2px solid var(--accent-primary);
        box-shadow: 0 0 15px rgba(139, 92, 246, 0.3);
    }
    
    .sidebar-header div {
        text-align: center;
    }
    
    /* Enhanced DataFrames */
    .dataframe-container {
        background: rgba(30, 30, 40, 0.3);
        backdrop-filter: blur(15px);
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        overflow: hidden;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.2);
    }
    
    .stDataFrame {
        background: transparent;
        border-radius: var(--radius-lg);
        overflow: hidden;
    }
    
    .stDataFrame table {
        font-size: 0.875rem;
    }
    
    .stDataFrame th {
        background: rgba(139, 92, 246, 0.1) !important;
        color: var(--accent-secondary) !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
        font-size: 0.75rem !important;
        border-bottom: 1px solid rgba(139, 92, 246, 0.2) !important;
    }
    
    .stDataFrame td {
        color: var(--neutral-300) !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.04) !important;
    }
    
    /* Modern Buttons */
    .stButton > button {
        background: linear-gradient(135deg, var(--accent-primary), var(--accent-tertiary)) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(139, 92, 246, 0.3) !important;
        text-transform: uppercase !important;
        letter-spacing: 0.025em !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 10px 20px rgba(139, 92, 246, 0.4) !important;
        background: linear-gradient(135deg, var(--primary-400) 0%, var(--primary-500) 100%) !important;
    }
    
    /* Enhanced Form Elements */
    .stSelectbox > div > div > div, .stTextInput > div > div > input {
        background: rgba(0, 0, 0, 0.3) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 10px !important;
        color: var(--text-primary) !important;
        backdrop-filter: blur(10px) !important;
        transition: all 0.3s ease !important;
    }
    
    .stSelectbox > div > div > div:focus, .stTextInput > div > div > input:focus {
        border-color: var(--accent-primary) !important;
        box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.2) !important;
    }
    
    /* Modern Radio Buttons */
    .stRadio > div {
        background: rgba(30, 30, 40, 0.3) !important;
        border-radius: 12px !important;
        padding: 1rem !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(10px) !important;
    }
    
    /* Enhanced Progress Bars */
    .stProgress > div {
        background-color: rgba(63, 63, 70, 0.5) !important;
        border-radius: 20px !important;
        height: 12px !important;
        overflow: hidden !important;
        box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.2) !important;
    }
    
    .stProgress > div > div > div {
        background: linear-gradient(90deg, var(--accent-tertiary), var(--accent-secondary)) !important;
        border-radius: 20px !important;
        transition: all 0.5s ease !important;
        box-shadow: 0 0 15px rgba(139, 92, 246, 0.5) !important;
    }
    
    /* Champion Icons Enhancement */
    .champion-icon {
        border: 3px solid var(--accent-primary);
        border-radius: 50%;
        box-shadow: 0 4px 15px rgba(139, 92, 246, 0.3);
    }
    
    /* Alert Boxes */
    .stAlert {
        background: rgba(30, 30, 40, 0.6) !important;
        border: 1px solid var(--accent-primary) !important;
        border-radius: 12px !important;
        backdrop-filter: blur(15px) !important;
    }
    
    /* Metric Cards Enhancement */
    .metric-value {
        font-size: 2.25rem !important;
        font-weight: 800 !important;
        background: linear-gradient(135deg, var(--accent-secondary), var(--accent-primary));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0.5rem 0 !important;
        filter: drop-shadow(0 2px 10px rgba(139, 92, 246, 0.2));
    }
    
    .metric-label {
        color: var(--text-secondary) !important;
        font-size: 0.9rem !important;
        font-weight: 500 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
        margin-bottom: 0.25rem !important;
    }
    
    .metric-delta {
        font-size: 0.85rem !important;
        font-weight: 600 !important;
        margin-top: 0.5rem !important;
    }
    
    /* Player Cards for Items Display */
    .player-items-row {
        background: rgba(30, 30, 40, 0.3);
        backdrop-filter: blur(15px);
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 1rem;
        border: 1px solid rgba(255, 255, 255, 0.05);
        display: flex;
        align-items: center;
        gap: 1rem;
        transition: all 0.3s ease;
    }
    
    .player-items-row:hover {
        transform: translateY(-1px);
        border-color: rgba(139, 92, 246, 0.3);
        background: rgba(30, 30, 40, 0.5);
    }
    
    .champion-section {
        display: flex;
        flex-direction: column;
        align-items: center;
        min-width: 80px;
    }
    
    .items-section {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        flex-wrap: wrap;
    }
    
    .player-info-section {
        display: flex;
        flex-direction: column;
        align-items: center;
        margin-top: 0.5rem;
    }
    
    .player-name {
        font-weight: 600;
        font-size: 0.9rem;
        color: var(--text-primary);
        margin: 0;
        text-align: center;
    }
    
    .player-score {
        font-size: 0.8rem;
        color: var(--text-secondary);
        text-align: center;
        margin: 0;
    }
    
    /* Status Indicators */
    .status-win {
        color: var(--success-500);
        background: rgba(16, 185, 129, 0.1);
        padding: var(--spacing-xs) var(--spacing-sm);
        border-radius: var(--radius-sm);
        font-weight: 600;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .status-loss {
        color: var(--error-500);
        background: rgba(239, 68, 68, 0.1);
        padding: var(--spacing-xs) var(--spacing-sm);
        border-radius: var(--radius-sm);
        font-weight: 600;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    /* Champion Cards */
    .champion-card {
        background: rgba(30, 30, 40, 0.3);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: var(--radius-lg);
        padding: var(--spacing-lg);
        transition: all 0.3s ease;
        text-align: center;
    }
    
    .champion-card:hover {
        transform: translateY(-2px);
        border-color: var(--accent-primary);
        box-shadow: 0 10px 30px -10px rgba(139, 92, 246, 0.3);
    }
    
    .champion-image {
        width: 64px;
        height: 64px;
        border-radius: 50%;
        border: 2px solid var(--primary-500);
        margin: 0 auto var(--spacing-md) auto;
        display: block;
        box-shadow: 0 0 15px rgba(139, 92, 246, 0.3);
    }
    
    .champion-name {
        font-weight: 600;
        color: var(--text-primary);
        margin: 0 0 var(--spacing-xs) 0;
    }
    
    .champion-stats {
        font-size: 0.875rem;
        color: rgba(255, 255, 255, 0.6);
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .main .block-container {
            padding: var(--spacing-md) var(--spacing-sm);
        }
        
        .stat-card {
            padding: var(--spacing-lg);
        }
        
        .metric-value {
            font-size: 2rem;
        }
        
        h2 {
            font-size: 1.5rem;
        }
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Enhanced metric cards function - EXACTLY AS ORIGINAL
def styled_metric(label, value, delta=None, delta_color="normal"):
    html = f"""
    <div class="stat-card">
        <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
            <p class="metric-label">{label}</p>
        </div>
        <p class="metric-value">{value}</p>
    """
    
    if delta:
        color_class = "gmb-blue" if delta_color == "blue" else "win" if delta_color == "good" else "loss" if delta_color == "bad" else ""
        html += f'<p class="metric-delta {color_class}">{delta}</p>'
    
    html += "</div>"
    return st.markdown(html, unsafe_allow_html=True)

# Connect to MongoDB Atlas - UPDATED FOR ROBUSTNESS
@st.cache_resource
def get_db():
    try:
        if "database" not in st.secrets:
            st.error("⚠️ Missing 'database' section in secrets.toml")
            return None
            
        connection_string = st.secrets["database"]["mongodb_connection_string"]
        
        # Use certifi for SSL Certificate Verification - Fixes connection errors on many platforms
        # Added timeouts to fail faster if IP is blocked (default is 30s, reduced to 5s)
        client = pymongo.MongoClient(
            connection_string, 
            tlsCAFile=certifi.where(),
            serverSelectionTimeoutMS=35000, 
            connectTimeoutMS=35000,
            socketTimeoutMS=35000
        )
        
        # Test connection explicitly
        client.admin.command('ping')
        
        return client.ClusterLit
    except Exception as e:
        error_msg = str(e)
        st.error(f"Failed to connect to database: {error_msg}")
        
        # Enhanced Error Diagnosis
        if "ServerSelectionTimeoutError" in error_msg:
            st.warning("⚠️ **Network Error:** Could not reach MongoDB. \n\n"
                       "**Likely Cause:** Your IP address is not whitelisted in MongoDB Atlas.\n\n"
                       "**Fix:** Go to MongoDB Atlas -> Network Access -> Add IP Address -> 'Allow Access from Anywhere' (0.0.0.0/0).")
        elif "AuthenticationFailed" in error_msg:
            st.warning("⚠️ **Auth Error:** The username or password in your connection string is incorrect.")
        elif "SSL" in error_msg:
            st.warning("⚠️ **SSL Error:** There is an issue with the secure connection. The 'certifi' fix should handle this, but your network might be intercepting traffic.")
            
        return None

# Get champion data - EXACTLY AS ORIGINAL
@st.cache_data(ttl=3600)
def get_champion_data():
    versions = requests.get("https://ddragon.leagueoflegends.com/api/versions.json").json()
    latest = versions[0]
    champs = requests.get(f"https://ddragon.leagueoflegends.com/cdn/{latest}/data/en_US/champion.json").json()
    
    champ_mapping = {}
    for key, data in champs["data"].items():
        champ_name = data["name"]
        champ_mapping[champ_name.lower()] = key
        champ_mapping[champ_name.lower().replace(" ", "")] = key
        champ_mapping[champ_name.lower().replace("'", "")] = key
        champ_mapping[champ_name.lower().replace(" ", "").replace("'", "")] = key
        
        if champ_name == "Wukong":
            champ_mapping["monkeyking"] = key
        elif champ_name == "Nunu & Willump":
            champ_mapping["nunu"] = key
        
    return champs["data"], latest, champ_mapping

# Helper function to find champion key - EXACTLY AS ORIGINAL
def find_champion_key(champion_name, champion_data, champ_mapping):
    if not champion_name:
        return None
    
    champ_key = next((k for k, v in champion_data.items() if v["name"] == champion_name), None)
    if champ_key:
        return champ_key
    
    normalized_name = champion_name.lower().replace(" ", "").replace("'", "")
    if normalized_name in champ_mapping:
        return champ_mapping[normalized_name]
    
    for key, data in champion_data.items():
        if champion_name.lower() in data["name"].lower() or data["name"].lower() in champion_name.lower():
            return key
    
    if champion_name in champion_data:
        return champion_name
    
    return None

@st.cache_data(ttl=300)
def load_scrims():
    db = get_db()
    if db is None:
        return []
        
    try:
        return list(db.Deacoy_Scrims.find())
    except Exception as e:
        st.error(f"Error loading scrims: {e}")
        return []

# Load data
champion_data, ddragon_version, champ_mapping = get_champion_data()
scrims_data = load_scrims()

# Calculate stats for sidebar
total_scrims = len(scrims_data) if scrims_data else 0
team_wins = 0
team_games = 0
team_win_rate = 0

# Players list for ID matching in stats calculation
stats_players = ["Fratellin", "Hamudis", "Sharon", "Kyte", "Fornari"]

if scrims_data:
    for scrim in scrims_data:
        participants = scrim.get("participants", [])
        our_team_id = None
        
        # Find our team ID
        for participant in participants:
            riot_name = participant.get("RIOT_ID_GAME_NAME", "")
            clean_player_name = riot_name
            for prefix in ["DEA "]:
                if riot_name.startswith(prefix):
                    clean_player_name = riot_name[len(prefix):]
                    break
            
            if clean_player_name in stats_players:
                our_team_id = participant.get("TEAM")
                break
        
        if our_team_id:
            team_games += 1
            # Check for win
            for participant in participants:
                riot_name = participant.get("RIOT_ID_GAME_NAME", "")
                clean_player_name = riot_name
                for prefix in ["DEA "]:
                    if riot_name.startswith(prefix):
                        clean_player_name = riot_name[len(prefix):]
                        break
                
                if (clean_player_name in stats_players and 
                    participant.get("TEAM") == our_team_id and 
                    participant.get("WIN") == "Win"):
                    team_wins += 1
                    break
    
    team_win_rate = (team_wins / team_games * 100) if team_games > 0 else 0

# Enhanced sidebar with modern design - UPDATED TO DEEP VIOLET
with st.sidebar:
    # Header with logo and text inline
    st.markdown("""
    <div class="sidebar-header">
        <img src="data:image/png;base64,{}" width="40" style="border-radius: 50%;">
        <div>
            <h1 style="font-size: 1.8rem; margin: 0; background: linear-gradient(135deg, #a78bfa, #c4b5fd); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-shadow: 0 0 10px rgba(139, 92, 246, 0.3);">
                Deacoy
            </h1>
            <p style="color: #a1a1aa; font-size: 0.9rem; margin: 0;">Scrims Dashboard</p>
        </div>
    </div>
    """.format(
        # Try to load logo and convert to base64, or use empty string if it fails
        __import__('base64').b64encode(open("logo.png", "rb").read()).decode() if __import__('os').path.exists("logo.png") else ""
    ), unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Scrim Stats in Sidebar
    if scrims_data:
        st.markdown(f"""
        <div class="modern-card" style="padding: 1rem; margin: 1rem 0;">
            <h4 style="margin: 0 0 0.5rem 0; color: #a78bfa;">Quick Stats</h4>
            <p style="margin: 0.25rem 0; font-size: 0.9rem;"><strong>{total_scrims}</strong> Total Games</p>
            <p style="margin: 0.25rem 0; font-size: 0.9rem;"><strong>{team_wins}W - {team_games-team_wins}L</strong></p>
            <p style="margin: 0.25rem 0; font-size: 0.9rem; color: {'#10b981' if team_win_rate >= 50 else '#ef4444'};">
                <strong>{team_win_rate:.1f}%</strong> Win Rate
            </p>
        </div>
        """, unsafe_allow_html=True)

# Main Page - Scrims Analysis
st.title("Scrims Analysis")

# scrims_data already loaded above

if not scrims_data:
    st.warning("No scrims data found in database. Please check your connection string or import scrim data first.")
else:
    # Define player roles - Updated keys to base names for cleaner matching
    players = {
        "Fratellin": "Top",
        "Hamudis": "Jungle", 
        "Sharon": "Mid",
        "Kyte": "ADC",
        "Fornari": "Support"
    }
    
    # Role colors for better visual distinction
    role_colors = {
        "Top": "#e11d48",      # Red
        "Jungle": "#10b981",   # Green  
        "Mid": "#3b82f6",      # Blue
        "ADC": "#f59e0b",      # Orange
        "Support": "#8b5cf6"   # Purple
    }
    
    # Create tabs for different views
    tab1, tab2 = st.tabs(["Champion Analysis", "Game Browser"])
    
    with tab1:
        # Collect champion data for players
        team_champion_data = {}
        
        # Process each scrim
        for scrim in scrims_data:
            participants = scrim.get("participants", [])
            
            # Find team ID by looking for our players
            team_id = None
            for participant in participants:
                riot_name = participant.get("RIOT_ID_GAME_NAME", "")
                # Extract player name without prefix
                clean_player_name = riot_name
                for prefix in ["DEA "]:
                    if riot_name.startswith(prefix):
                        clean_player_name = riot_name[len(prefix):]
                        break
                
                if clean_player_name in players:
                    team_id = participant.get("TEAM")
                    break
            
            # Process each participant
            for participant in participants:
                riot_name = participant.get("RIOT_ID_GAME_NAME", "")
                champion = participant.get("SKIN", "")
                win_status = participant.get("WIN", "")
                participant_team_id = participant.get("TEAM")
                
                # Extract player name without prefix
                clean_player_name = riot_name
                for prefix in ["DEA "]:
                    if riot_name.startswith(prefix):
                        clean_player_name = riot_name[len(prefix):]
                        break
                
                # Check if this is one of our players
                if clean_player_name in players and participant_team_id == team_id:
                    role = players[clean_player_name]
                    
                    # Initialize role data if needed
                    if role not in team_champion_data:
                        team_champion_data[role] = {}
                    if champion not in team_champion_data[role]:
                        team_champion_data[role][champion] = {"wins": 0, "games": 0}
                    
                    # Count the game
                    team_champion_data[role][champion]["games"] += 1
                    if win_status == "Win":
                        team_champion_data[role][champion]["wins"] += 1
        
        # Display results
        st.markdown("""
        <div style="text-align: center; margin-bottom: 2rem;">
            <h2 style="background: linear-gradient(135deg, #a78bfa, #c4b5fd); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 0.5rem;">
                Champion Performance by Role
            </h2>
            <p style="color: #a1a1aa; font-size: 1.1rem;">Analyzing champion win rates for each team member in scrims</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Create 5 columns layout for roles
        roles = ["Top", "Jungle", "Mid", "ADC", "Support"]
        cols = st.columns(5)
        
        for i, role in enumerate(roles):
            with cols[i]:
                player_name = [k for k, v in players.items() if v == role][0]
                role_color = role_colors.get(role, "#3b82f6")
                
                # Role header
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, {role_color}20, {role_color}10); 
                            border: 2px solid {role_color}; 
                            border-radius: 16px; 
                            padding: 1rem; 
                            margin-bottom: 1rem;
                            text-align: center;
                            backdrop-filter: blur(10px);
                            display: flex;
                            flex-direction: column;
                            align-items: center;
                            justify-content: center;">
                    <h3 style="color: {role_color}; margin: 0; font-size: 1.4rem; font-weight: 700; text-align: center; width: 100%;">
                        {role}
                    </h3>
                    <p style="color: #a1a1aa; margin: 0.25rem 0 0 0; font-size: 0.9rem; text-align: center; width: 100%;">
                        {player_name}
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                # Champions for this role
                if role in team_champion_data and team_champion_data[role]:
                    # Prepare data for this role
                    role_data = []
                    for champion, stats in team_champion_data[role].items():
                        if stats["games"] > 0:
                            win_rate = (stats["wins"] / stats["games"]) * 100
                            role_data.append({
                                "champion": champion,
                                "games": stats["games"],
                                "wins": stats["wins"],
                                "losses": stats["games"] - stats["wins"],
                                "win_rate": win_rate
                            })
                    
                    # Sort by games played, then by win rate
                    role_data.sort(key=lambda x: (x["games"], x["win_rate"]), reverse=True)
                    
                    # Initialize session state for this role's expansion
                    expand_key = f"expand_{role.lower()}_champions"
                    if expand_key not in st.session_state:
                        st.session_state[expand_key] = False
                    
                    # Determine how many champions to show
                    show_all = st.session_state[expand_key]
                    champions_to_show = role_data if show_all else role_data[:5]
                    
                    # Display champions in compact cards
                    for j, champ_data in enumerate(champions_to_show):
                        champion_name = champ_data["champion"]
                        win_rate = champ_data["win_rate"]
                        games = champ_data["games"]
                        wins = champ_data["wins"]
                        
                        # Get champion image
                        champ_key = find_champion_key(champion_name, champion_data, champ_mapping)
                        
                        # Champion card with role color theme
                        st.markdown(f"""
                        <div style="background: rgba(30, 30, 40, 0.4); 
                                    border: 1px solid {role_color}50; 
                                    border-radius: 12px; 
                                    padding: 0.75rem; 
                                    margin-bottom: 0.75rem;
                                    text-align: center;
                                    transition: all 0.3s ease;">
                            <div style="margin-bottom: 0.5rem;">
                                {'<img src="https://ddragon.leagueoflegends.com/cdn/' + ddragon_version + '/img/champion/' + champ_key + '.png" width="50" style="border-radius: 8px; border: 2px solid ' + role_color + ';">' if champ_key else '<div style="width: 50px; height: 50px; background: ' + role_color + '30; border-radius: 8px; display: flex; align-items: center; justify-content: center; margin: 0 auto; border: 2px solid ' + role_color + ';"><span style="color: ' + role_color + ';">?</span></div>'}
                            </div>
                            <div style="font-weight: 600; color: {role_color}; font-size: 0.85rem; margin-bottom: 0.25rem;">
                                {champion_name}
                            </div>
                            <div style="color: #f8fafc; font-size: 0.75rem; margin-bottom: 0.25rem;">
                                <strong>{win_rate:.0f}%</strong> WR
                            </div>
                            <div style="color: #a1a1aa; font-size: 0.7rem;">
                                {wins}W-{games-wins}L ({games}g)
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Show expand/collapse button if there are more than 5 champions
                    if len(role_data) > 5:
                        remaining_count = len(role_data) - 5
                        button_text = "Show Less" if show_all else f"Show {remaining_count} More"
                        button_icon = "▲" if show_all else "▼"
                        
                        if st.button(f"{button_icon} {button_text}", key=f"toggle_{role.lower()}_champions", use_container_width=True):
                            st.session_state[expand_key] = not st.session_state[expand_key]
                            st.rerun()
                else:
                    # No data for this role
                    st.markdown(f"""
                    <div style="background: rgba(30, 30, 40, 0.2); 
                                border: 1px dashed {role_color}50; 
                                border-radius: 12px; 
                                padding: 1rem; 
                                text-align: center;
                                color: #a1a1aa;">
                        <p style="margin: 0; font-size: 0.8rem;">No champions played</p>
                    </div>
                    """, unsafe_allow_html=True)
        
        # Summary statistics removed from here as requested
    
    with tab2:
        # ALL THE GAME BROWSER CODE
        st.markdown("""
        <div style="text-align: center; margin-bottom: 2rem;">
            <h2 style="background: linear-gradient(135deg, #a78bfa, #c4b5fd); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 0.5rem;">
                Scrim Games Browser
            </h2>
            <p style="color: #a1a1aa; font-size: 1.1rem;">Browse all scrim games with draft information and filtering</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Prepare game data for browsing
        scrim_games = []
        all_our_champions = set()
        all_enemy_champions = set()
        all_game_versions = set()
        
        for scrim_index, scrim in enumerate(scrims_data):
            participants = scrim.get("participants", [])
            game_version = scrim.get("gameVersion", "Unknown")
            game_duration = scrim.get("gameDuration", {})
            if isinstance(game_duration, dict):
                game_duration = int(game_duration.get("$numberInt", 0))
            else:
                game_duration = int(game_duration) if game_duration else 0
            
            # Extract major version (e.g., "15.13" from "15.13.693.1076")
            version_parts = game_version.split(".")
            if len(version_parts) >= 2:
                major_version = f"{version_parts[0]}.{version_parts[1]}"
                all_game_versions.add(major_version)
            else:
                major_version = game_version
            
            # Find our team ID
            our_team_id = None
            for participant in participants:
                riot_name = participant.get("RIOT_ID_GAME_NAME", "")
                clean_player_name = riot_name
                
                for prefix in ["DEA "]:
                    if riot_name.startswith(prefix):
                        clean_player_name = riot_name[len(prefix):]
                        break
                
                if clean_player_name in players:
                    our_team_id = participant.get("TEAM")
                    break
            
            if our_team_id is None:
                continue
            
            # Calculate team totals for KP%, objectives, damage, and gold
            team_stats = {}
            for participant in participants:
                team_id = participant.get("TEAM")
                if team_id not in team_stats:
                    team_stats[team_id] = {
                        "kills": 0,
                        "dragons": 0,
                        "barons": 0,
                        "heralds": 0,
                        "grubs": 0,
                        "total_damage": 0,
                        "total_gold": 0
                    }
                
                # Sum up team stats
                team_stats[team_id]["kills"] += int(participant.get("CHAMPIONS_KILLED", 0))
                team_stats[team_id]["dragons"] += int(participant.get("DRAGON_KILLS", 0))
                team_stats[team_id]["barons"] += int(participant.get("BARON_KILLS", 0))
                team_stats[team_id]["heralds"] += int(participant.get("RIFT_HERALD_KILLS", 0))
                team_stats[team_id]["grubs"] += int(participant.get("HORDE_KILLS", 0))
                team_stats[team_id]["total_damage"] += int(participant.get("TOTAL_DAMAGE_DEALT_TO_CHAMPIONS", 0))
                team_stats[team_id]["total_gold"] += int(participant.get("GOLD_EARNED", 0))
            
            # Separate teams
            our_team = []
            enemy_team = []
            game_result = None
            our_team_objectives = {}
            enemy_team_objectives = {}
            
            for participant in participants:
                riot_name = participant.get("RIOT_ID_GAME_NAME", "")
                champion = participant.get("SKIN", "Unknown")
                win_status = participant.get("WIN", "")
                team_id = participant.get("TEAM")
                
                # Extract stats
                kills = int(participant.get("CHAMPIONS_KILLED", 0))
                deaths = int(participant.get("NUM_DEATHS", 0))
                assists = int(participant.get("ASSISTS", 0))
                minions_killed = int(participant.get("MINIONS_KILLED", 0))
                neutral_minions = int(participant.get("NEUTRAL_MINIONS_KILLED", 0))
                cs = minions_killed + neutral_minions
                damage_dealt = int(participant.get("TOTAL_DAMAGE_DEALT_TO_CHAMPIONS", 0))
                gold_earned = int(participant.get("GOLD_EARNED", 0))
                
                # Calculate Kill Participation %
                team_total_kills = team_stats[team_id]["kills"]
                if team_total_kills > 0:
                    kp = ((kills + assists) / team_total_kills) * 100
                else:
                    kp = 0
                
                # Calculate Damage %
                team_total_damage = team_stats[team_id]["total_damage"]
                if team_total_damage > 0:
                    damage_percent = (damage_dealt / team_total_damage) * 100
                else:
                    damage_percent = 0
                
                # Calculate Gold %
                team_total_gold = team_stats[team_id]["total_gold"]
                if team_total_gold > 0:
                    gold_percent = (gold_earned / team_total_gold) * 100
                else:
                    gold_percent = 0
                
                clean_player_name = riot_name
                for prefix in ["DEA "]:
                    if riot_name.startswith(prefix):
                        clean_player_name = riot_name[len(prefix):]
                        break
                
                participant_data = {
                    "player": clean_player_name,
                    "champion": champion,
                    "full_name": riot_name,
                    "kills": kills,
                    "deaths": deaths,
                    "assists": assists,
                    "cs": cs,
                    "kp": kp,
                    "damage_percent": damage_percent,
                    "gold_percent": gold_percent
                }
                
                if team_id == our_team_id:
                    our_team.append(participant_data)
                    all_our_champions.add(champion)
                    if win_status == "Win":
                        game_result = "WIN"
                    elif win_status == "Fail":
                        game_result = "LOSS"
                    # Store our team objectives
                    if not our_team_objectives:
                        our_team_objectives = {
                            "dragons": team_stats[team_id]["dragons"],
                            "barons": team_stats[team_id]["barons"],
                            "heralds": team_stats[team_id]["heralds"],
                            "grubs": team_stats[team_id]["grubs"]
                        }
                else:
                    enemy_team.append(participant_data)
                    all_enemy_champions.add(champion)
                    # Store enemy team objectives
                    if not enemy_team_objectives:
                        enemy_team_objectives = {
                            "dragons": team_stats[team_id]["dragons"],
                            "barons": team_stats[team_id]["barons"],
                            "heralds": team_stats[team_id]["heralds"],
                            "grubs": team_stats[team_id]["grubs"]
                        }
            
            # Determine side (assuming team 100 is blue, 200 is red)
            our_side = "BLUE" if our_team_id == 100 else "RED"
            enemy_side = "RED" if our_team_id == 100 else "BLUE"
            
            if len(our_team) == 5 and len(enemy_team) == 5:
                scrim_games.append({
                    "index": scrim_index,
                    "our_team": our_team,
                    "enemy_team": enemy_team,
                    "our_objectives": our_team_objectives,
                    "enemy_objectives": enemy_team_objectives,
                    "result": game_result,
                    "our_side": our_side,
                    "enemy_side": enemy_side,
                    "game_version": major_version,
                    "full_version": game_version,
                    "duration": game_duration
                })
        
        # Sort games by most recent (highest index first)
        scrim_games.sort(key=lambda x: x["index"], reverse=True)
        
        if not scrim_games:
            st.warning("No valid scrim games found with complete team data.")
        else:
            # Filtering section
            st.subheader("🔍 Filter Games")
            
            # Game version filter
            sorted_versions = sorted(list(all_game_versions), reverse=True)
            selected_versions = st.multiselect(
                "Game Versions",
                sorted_versions,
                default=[],
                key="scrim_version_filter"
            )
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                result_filter = st.radio("Result", ["All", "WIN", "LOSS"], key="scrim_result_filter")
                
            with col2:
                side_filter = st.radio("Our Side", ["All", "BLUE", "RED"], key="scrim_side_filter")
            
            with col3:
                our_champions_list = ["All"] + sorted(list(all_our_champions))
                our_champion_filter = st.selectbox("Our Champion", our_champions_list, key="scrim_our_champ")
            
            with col4:
                enemy_champions_list = ["All"] + sorted(list(all_enemy_champions))
                enemy_champion_filter = st.selectbox("Enemy Champion", enemy_champions_list, key="scrim_enemy_champ")
            
            # Apply filters
            filtered_games = scrim_games.copy()
            
            # Apply version filter
            if selected_versions:
                filtered_games = [g for g in filtered_games if g["game_version"] in selected_versions]
            
            if result_filter != "All":
                filtered_games = [g for g in filtered_games if g["result"] == result_filter]
            
            if side_filter != "All":
                filtered_games = [g for g in filtered_games if g["our_side"] == side_filter]
            
            if our_champion_filter != "All":
                filtered_games = [g for g in filtered_games if any(p["champion"] == our_champion_filter for p in g["our_team"])]
            
            if enemy_champion_filter != "All":
                filtered_games = [g for g in filtered_games if any(p["champion"] == enemy_champion_filter for p in g["enemy_team"])]
            
            # Calculate win rate for filtered games
            filter_wins = 0
            filter_games = len(filtered_games)
            for game in filtered_games:
                if game["result"] == "WIN":
                    filter_wins += 1
            
            filter_win_rate = (filter_wins / filter_games * 100) if filter_games > 0 else 0
            
            # Display filtered results with win rate
            col_title, col_winrate = st.columns([3, 1])
            
            with col_title:
                st.subheader(f"📋 Games ({len(filtered_games)} games)")
            
            with col_winrate:
                if filter_games > 0:
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #a78bfa, #c4b5fd); 
                                border-radius: 8px; 
                                padding: 0.75rem; 
                                text-align: center;">
                        <p style="color: white; margin: 0; font-size: 0.9rem;">Filter Win Rate</p>
                        <p style="color: white; margin: 0; font-size: 1.5rem; font-weight: bold;">
                            {filter_win_rate:.1f}%
                        </p>
                        <p style="color: rgba(255,255,255,0.8); margin: 0; font-size: 0.8rem;">
                            {filter_wins}W - {filter_games - filter_wins}L
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
            
            if not filtered_games:
                st.warning("No games match the selected filters.")
            else:
                # Display games
                for game in filtered_games:
                    result_color = "#10b981" if game["result"] == "WIN" else "#ef4444"
                    
                    with st.container():
                        # Game header
                        st.markdown(f"""
                        <div style="background: linear-gradient(135deg, {result_color}20, {result_color}10); 
                                    border-left: 4px solid {result_color}; 
                                    border-radius: 12px; 
                                    padding: 1rem; 
                                    margin: 1rem 0;
                                    backdrop-filter: blur(10px);">
                            <h4 style="color: {result_color}; margin: 0; display: flex; align-items: center; gap: 1rem;">
                                <span>{game["result"]}</span>
                                <span style="color: #a1a1aa; font-size: 1rem; font-weight: 400;">
                                    • Our Side: {game["our_side"]} • Game #{game["index"] + 1} • Version: {game["game_version"]}
                                </span>
                            </h4>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Team drafts
                        col1, col_sep, col2 = st.columns([5, 1, 5])
                        
                        with col1:
                            st.markdown(f"""
                            <h5 style="color: #8b5cf6; margin-bottom: 0.5rem; text-align: center;">
                                Deacoy ({game["our_side"]} Side)
                            </h5>
                            """, unsafe_allow_html=True)
                            
                            # Team objectives display
                            our_objectives = game.get("our_objectives", {})
                            st.markdown(f"""
                            <div style="display: flex; justify-content: center; gap: 1rem; margin-bottom: 1rem;">
                                <div style="text-align: center; background: rgba(59, 130, 246, 0.1); border-radius: 6px; padding: 0.5rem;">
                                    <div style="color: #8b5cf6; font-size: 1.2rem; font-weight: bold;">{our_objectives.get("dragons", 0)}</div>
                                    <div style="color: #a1a1aa; font-size: 0.7rem;">🐉 Dragons</div>
                                </div>
                                <div style="text-align: center; background: rgba(139, 92, 246, 0.1); border-radius: 6px; padding: 0.5rem;">
                                    <div style="color: #a78bfa; font-size: 1.2rem; font-weight: bold;">{our_objectives.get("grubs", 0)}</div>
                                    <div style="color: #a1a1aa; font-size: 0.7rem;">🐛 Grubs</div>
                                </div>
                                <div style="text-align: center; background: rgba(236, 72, 153, 0.1); border-radius: 6px; padding: 0.5rem;">
                                    <div style="color: #ec4899; font-size: 1.2rem; font-weight: bold;">{our_objectives.get("heralds", 0)}</div>
                                    <div style="color: #a1a1aa; font-size: 0.7rem;">👁️ Heralds</div>
                                </div>
                                <div style="text-align: center; background: rgba(168, 85, 247, 0.1); border-radius: 6px; padding: 0.5rem;">
                                    <div style="color: #a855f7; font-size: 1.2rem; font-weight: bold;">{our_objectives.get("barons", 0)}</div>
                                    <div style="color: #a1a1aa; font-size: 0.7rem;">👑 Barons</div>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Our team champions
                            for player_data in game["our_team"]:
                                champion = player_data["champion"]
                                player = player_data["player"]
                                kills = player_data.get("kills", 0)
                                deaths = player_data.get("deaths", 0)
                                assists = player_data.get("assists", 0)
                                cs = player_data.get("cs", 0)
                                kp = player_data.get("kp", 0)
                                damage_percent = player_data.get("damage_percent", 0)
                                gold_percent = player_data.get("gold_percent", 0)
                                champ_key = find_champion_key(champion, champion_data, champ_mapping)
                                
                                # Get role for player
                                role = players.get(player, "Unknown")
                                role_color = role_colors.get(role, "#a1a1aa")
                                
                                # Calculate KDA ratio
                                kda_ratio = ((kills + assists) / max(deaths, 1))
                                kda_color = "#10b981" if kda_ratio >= 3 else "#eab308" if kda_ratio >= 2 else "#ef4444"
                                
                                st.markdown(f"""
                                <div style="display: flex; align-items: center; gap: 1rem; 
                                            background: rgba(30, 30, 40, 0.4); 
                                            border-radius: 8px; 
                                            padding: 0.75rem; 
                                            margin-bottom: 0.5rem;
                                            border-left: 3px solid {role_color};">
                                    {'<img src="https://ddragon.leagueoflegends.com/cdn/' + ddragon_version + '/img/champion/' + champ_key + '.png" width="40" style="border-radius: 6px;">' if champ_key else '<div style="width: 40px; height: 40px; background: #3f3f46; border-radius: 6px; display: flex; align-items: center; justify-content: center;"><span style="color: white;">?</span></div>'}
                                    <div style="flex: 1;">
                                        <div style="font-weight: 600; color: #f8fafc;">{champion}</div>
                                        <div style="color: {role_color}; font-size: 0.8rem;">{player} ({role})</div>
                                    </div>
                                    <div style="display: flex; gap: 0.8rem; align-items: center;">
                                        <div style="text-align: center;">
                                            <div style="color: {kda_color}; font-weight: 600; font-size: 0.9rem;">
                                                {kills}/{deaths}/{assists}
                                            </div>
                                            <div style="color: #a1a1aa; font-size: 0.7rem;">KDA</div>
                                        </div>
                                        <div style="text-align: center;">
                                            <div style="color: #a78bfa; font-weight: 600; font-size: 0.9rem;">
                                                {cs}
                                            </div>
                                            <div style="color: #a1a1aa; font-size: 0.7rem;">CS</div>
                                        </div>
                                        <div style="text-align: center;">
                                            <div style="color: #a78bfa; font-weight: 600; font-size: 0.9rem;">
                                                {kp:.0f}%
                                            </div>
                                            <div style="color: #a1a1aa; font-size: 0.7rem;">KP</div>
                                        </div>
                                        <div style="text-align: center;">
                                            <div style="color: #ef4444; font-weight: 600; font-size: 0.9rem;">
                                                {damage_percent:.0f}%
                                            </div>
                                            <div style="color: #a1a1aa; font-size: 0.7rem;">DMG</div>
                                        </div>
                                        <div style="text-align: center;">
                                            <div style="color: #f59e0b; font-weight: 600; font-size: 0.9rem;">
                                                {gold_percent:.0f}%
                                            </div>
                                            <div style="color: #a1a1aa; font-size: 0.7rem;">GOLD</div>
                                        </div>
                                    </div>
                                </div>
                                """, unsafe_allow_html=True)
                        
                        with col_sep:
                            st.markdown(f"""
                            <div style="text-align: center; margin-top: 3rem;">
                                <div style="font-size: 2rem; color: {result_color};">
                                    {"⚔️" if game["result"] == "WIN" else "💀"}
                                </div>
                                <div style="color: #a1a1aa; font-size: 0.8rem; margin-top: 0.5rem;">
                                    VS
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        with col2:
                            st.markdown(f"""
                            <h5 style="color: #ef4444; margin-bottom: 0.5rem; text-align: center;">
                                Enemy ({game["enemy_side"]} Side)
                            </h5>
                            """, unsafe_allow_html=True)
                            
                            # Enemy team objectives display
                            enemy_objectives = game.get("enemy_objectives", {})
                            st.markdown(f"""
                            <div style="display: flex; justify-content: center; gap: 1rem; margin-bottom: 1rem;">
                                <div style="text-align: center; background: rgba(239, 68, 68, 0.1); border-radius: 6px; padding: 0.5rem;">
                                    <div style="color: #ef4444; font-size: 1.2rem; font-weight: bold;">{enemy_objectives.get("dragons", 0)}</div>
                                    <div style="color: #a1a1aa; font-size: 0.7rem;">🐉 Dragons</div>
                                </div>
                                <div style="text-align: center; background: rgba(239, 68, 68, 0.1); border-radius: 6px; padding: 0.5rem;">
                                    <div style="color: #ef4444; font-size: 1.2rem; font-weight: bold;">{enemy_objectives.get("grubs", 0)}</div>
                                    <div style="color: #a1a1aa; font-size: 0.7rem;">🐛 Grubs</div>
                                </div>
                                <div style="text-align: center; background: rgba(239, 68, 68, 0.1); border-radius: 6px; padding: 0.5rem;">
                                    <div style="color: #ef4444; font-size: 1.2rem; font-weight: bold;">{enemy_objectives.get("heralds", 0)}</div>
                                    <div style="color: #a1a1aa; font-size: 0.7rem;">👁️ Heralds</div>
                                </div>
                                <div style="text-align: center; background: rgba(239, 68, 68, 0.1); border-radius: 6px; padding: 0.5rem;">
                                    <div style="color: #ef4444; font-size: 1.2rem; font-weight: bold;">{enemy_objectives.get("barons", 0)}</div>
                                    <div style="color: #a1a1aa; font-size: 0.7rem;">👑 Barons</div>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Enemy team champions
                            for player_data in game["enemy_team"]:
                                champion = player_data["champion"]
                                player = player_data["player"]
                                kills = player_data.get("kills", 0)
                                deaths = player_data.get("deaths", 0)
                                assists = player_data.get("assists", 0)
                                cs = player_data.get("cs", 0)
                                kp = player_data.get("kp", 0)
                                damage_percent = player_data.get("damage_percent", 0)
                                gold_percent = player_data.get("gold_percent", 0)
                                champ_key = find_champion_key(champion, champion_data, champ_mapping)
                                
                                # Calculate KDA ratio
                                kda_ratio = ((kills + assists) / max(deaths, 1))
                                kda_color = "#10b981" if kda_ratio >= 3 else "#eab308" if kda_ratio >= 2 else "#ef4444"
                                
                                st.markdown(f"""
                                <div style="display: flex; align-items: center; gap: 1rem; 
                                            background: rgba(30, 30, 40, 0.4); 
                                            border-radius: 8px; 
                                            padding: 0.75rem; 
                                            margin-bottom: 0.5rem;
                                            border-left: 3px solid #ef4444;">
                                    {'<img src="https://ddragon.leagueoflegends.com/cdn/' + ddragon_version + '/img/champion/' 
                                    + champ_key + '.png" width="40" style="border-radius: 6px;">' 
                                    if champ_key 
                                    else '<div style="width: 40px; height: 40px; background: #3f3f46; border-radius: 6px; display: flex; align-items: center; justify-content: center;"><span style="color: white;">?</span></div>'}
                                    <div style="flex: 1;">
                                        <div style="font-weight: 600; color: #f8fafc;">{champion}</div>
                                        <div style="color: #ef4444; font-size: 0.8rem;">{player}</div>
                                    </div>
                                    <div style="display: flex; gap: 0.8rem; align-items: center;">
                                        <div style="text-align: center;">
                                            <div style="color: {kda_color}; font-weight: 600; font-size: 0.9rem;">
                                                {kills}/{deaths}/{assists}
                                            </div>
                                            <div style="color: #a1a1aa; font-size: 0.7rem;">KDA</div>
                                        </div>
                                        <div style="text-align: center;">
                                            <div style="color: #a78bfa; font-weight: 600; font-size: 0.9rem;">
                                                {cs}
                                            </div>
                                            <div style="color: #a1a1aa; font-size: 0.7rem;">CS</div>
                                        </div>
                                        <div style="text-align: center;">
                                            <div style="color: #a78bfa; font-weight: 600; font-size: 0.9rem;">
                                                {kp:.0f}%
                                            </div>
                                            <div style="color: #a1a1aa; font-size: 0.7rem;">KP</div>
                                        </div>
                                        <div style="text-align: center;">
                                            <div style="color: #ef4444; font-weight: 600; font-size: 0.9rem;">
                                                {damage_percent:.0f}%
                                            </div>
                                            <div style="color: #a1a1aa; font-size: 0.7rem;">DMG</div>
                                        </div>
                                        <div style="text-align: center;">
                                            <div style="color: #f59e0b; font-weight: 600; font-size: 0.9rem;">
                                                {gold_percent:.0f}%
                                            </div>
                                            <div style="color: #a1a1aa; font-size: 0.7rem;">GOLD</div>
                                        </div>
                                    </div>
                                </div>
                                """, unsafe_allow_html=True)

# Logout button at the end of the application
st.markdown("---")
st.markdown('<div style="text-align: center; padding: 2rem 0;">', unsafe_allow_html=True)
if st.button("🔓 Logout", key="logout_button"):
    st.session_state.authenticated = False
    st.rerun()
st.markdown('</div>', unsafe_allow_html=True)