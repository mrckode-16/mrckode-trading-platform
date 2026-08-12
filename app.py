import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from streamlit_autorefresh import st_autorefresh
from datetime import datetime
from bot_engine import TradingBot
from styles import get_custom_css
from config import *

# ===================================================
# PAGE CONFIGURATION
# ===================================================
st.set_page_config(
    page_title=APP_NAME,
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom styling
st.markdown(get_custom_css(), unsafe_allow_html=True)

# Auto-refresh every 30 seconds
st_autorefresh(interval=30000, key="auto_refresh")

# Initialize bot in session
if 'bot' not in st.session_state:
    st.session_state.bot = TradingBot()

bot = st.session_state.bot

# ===================================================
# FETCH LIVE DATA
# ===================================================
try:
    df = bot.get_market_data()
    signals = bot.check_signals(df)
    
    if df is None or signals is None:
        st.error("⚠️ Unable to fetch market data. Please check your internet connection.")
        st.stop()
    
    current_price = signals['price']
    
    # Run trading cycle if bot is active
    if bot.state['bot_running']:
        bot.run_cycle()
        bot.state = bot.load_state()
        signals = bot.check_signals(df)
    
    # Calculate portfolio metrics
    total_value = bot.state['usdt_balance'] + (bot.state['btc_holding'] * current_price)
    total_profit = total_value - STARTING_BALANCE
    profit_pct = (total_profit / STARTING_BALANCE) * 100
    
    # 24h price change
    if len(df) >= 96:
        price_change_24h = ((current_price - df['close'].iloc[-96]) / df['close'].iloc[-96]) * 100
    else:
        price_change_24h = ((current_price - df['close'].iloc[0]) / df['close'].iloc[0]) * 100

except Exception as e:
    st.error(f"⚠️ Connection Error: {e}")
    st.stop()

# ===================================================
# TOP NAVIGATION BAR
# ===================================================
status_html = (
    '<span class="status-pill status-live"><span class="pulse-dot"></span>LIVE</span>'
    if bot.state['bot_running']
    else '<span class="status-pill status-paused"><span class="pulse-dot-red"></span>PAUSED</span>'
)

price_color = "metric-positive" if price_change_24h >= 0 else "metric-negative"
price_arrow = "▲" if price_change_24h >= 0 else "▼"

st.markdown(f"""
<div class="top-nav">
    <div class="nav-brand">
        <div class="nav-logo">⚡ MrCKode</div>
        <div class="nav-badge">PRO</div>
    </div>
    <div class="nav-right">
        <div class="nav-symbol">{bot.settings['symbol']}</div>
        <div class="nav-price">${current_price:,.2f}</div>
        <div class="{price_color}" style="font-size: 15px; font-weight: 700;">
            {price_arrow} {abs(price_change_24h):.2f}%
        </div>
        {status_html}
    </div>
</div>
""", unsafe_allow_html=True)

# ===================================================
# SIDEBAR - CONTROLS & SETTINGS
# ===================================================
with st.sidebar:
    # Logo
    st.markdown("""
    <div class="sidebar-header">
        <div class="sidebar-logo">⚡ MrCKode</div>
        <div class="sidebar-tagline">TRADING TERMINAL</div>
    </div>
    """, unsafe_allow_html=True)
    
    # ===== BOT CONTROLS =====
    st.markdown('<div class="section-title">Bot Control</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("▶ START", use_container_width=True, key="start_btn"):
            bot.state['bot_running'] = True
            bot.state['last_action'] = 'Bot started'
            bot.save_state()
            st.rerun()
    
    with col2:
        if st.button("■ STOP", use_container_width=True, key="stop_btn"):
            bot.state['bot_running'] = False
            bot.state['last_action'] = 'Bot stopped'
            bot.save_state()
            st.rerun()
    
    if st.button("↻ RESET BOT", use_container_width=True, key="reset_btn"):
        bot.reset_bot()
        st.rerun()
    
    # ===== TRADING PAIR SELECTOR =====
    st.markdown('<div class="section-title">Trading Pair</div>', unsafe_allow_html=True)
    
    new_symbol = st.selectbox(
        "Select Coin",
        AVAILABLE_SYMBOLS,
        index=AVAILABLE_SYMBOLS.index(bot.settings['symbol']),
        label_visibility="collapsed"
    )
    if new_symbol != bot.settings['symbol']:
        bot.update_setting('symbol', new_symbol)
        st.rerun()
    
    new_timeframe = st.selectbox(
        "Timeframe",
        AVAILABLE_TIMEFRAMES,
        index=AVAILABLE_TIMEFRAMES.index(bot.settings['timeframe']),
        label_visibility="collapsed"
    )
    if new_timeframe != bot.settings['timeframe']:
        bot.update_setting('timeframe', new_timeframe)
        st.rerun()
    
    # ===== STRATEGY SETTINGS =====
    st.markdown('<div class="section-title">Strategy</div>', unsafe_allow_html=True)
    
    new_tp = st.number_input(
        "Take Profit (%)",
        min_value=0.5,
        max_value=10.0,
        value=bot.settings['take_profit'] * 100,
        step=0.1,
        key="tp_input"
    )
    if new_tp / 100 != bot.settings['take_profit']:
        bot.update_setting('take_profit', new_tp / 100)
    
    new_sl = st.number_input(
        "Stop Loss (%)",
        min_value=0.5,
        max_value=10.0,
        value=bot.settings['stop_loss'] * 100,
        step=0.1,
        key="sl_input"
    )
    if new_sl / 100 != bot.settings['stop_loss']:
        bot.update_setting('stop_loss', new_sl / 100)
    
    new_pos = st.number_input(
        "Position Size (%)",
        min_value=5.0,
        max_value=100.0,
        value=bot.settings['position_size'] * 100,
        step=5.0,
        key="pos_input"
    )
    if new_pos / 100 != bot.settings['position_size']:
        bot.update_setting('position_size', new_pos / 100)
    
    new_rsi = st.number_input(
        "RSI Overbought Level",
        min_value=50,
        max_value=90,
        value=int(bot.settings['rsi_overbought']),
        step=1,
        key="rsi_input"
    )
    if new_rsi != bot.settings['rsi_overbought']:
        bot.update_setting('rsi_overbought', new_rsi)
    
    # ===== LAST ACTION =====
    st.markdown('<div class="section-title">Last Action</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="info-box">{bot.state["last_action"]}</div>', unsafe_allow_html=True)

# ===================================================
# MAIN METRICS ROW
# ===================================================
col1, col2, col3, col4 = st.columns(4)

with col1:
    change_class = "metric-positive" if total_profit >= 0 else "metric-negative"
    change_arrow = "▲" if total_profit >= 0 else "▼"
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-icon">💼</div>
        <div class="metric-label">Portfolio Value</div>
        <div class="metric-value">${total_value:,.2f}</div>
        <div class="metric-sub {change_class}">
            {change_arrow} ${abs(total_profit):.2f} ({profit_pct:+.2f}%)
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    rsi_val = signals['rsi']
    if rsi_val > 70:
        rsi_class = "metric-negative"
        rsi_status = "OVERBOUGHT"
    elif rsi_val < 30:
        rsi_class = "metric-positive"
        rsi_status = "OVERSOLD"
    else:
        rsi_class = "metric-neutral"
        rsi_status = "NEUTRAL"
    
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-icon">📊</div>
        <div class="metric-label">RSI Indicator</div>
        <div class="metric-value">{rsi_val:.1f}</div>
        <div class="metric-sub {rsi_class}">● {rsi_status}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    stats = bot.get_stats()
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-icon">🎯</div>
        <div class="metric-label">Win Rate</div>
        <div class="metric-value">{stats['win_rate']:.1f}%</div>
        <div class="metric-sub metric-neutral">
            ✓ {stats['wins']} Wins · ✗ {stats['losses']} Losses
        </div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    trend_class = "metric-positive" if signals['trend_up'] else "metric-negative"
    trend_icon = "📈" if signals['trend_up'] else "📉"
    trend_text = "BULLISH" if signals['trend_up'] else "BEARISH"
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-icon">{trend_icon}</div>
        <div class="metric-label">Market Trend</div>
        <div class="metric-value" style="font-size:22px;">{trend_text}</div>
        <div class="metric-sub {trend_class}">
            {stats['total_trades']} Total Trades
        </div>
    </div>
    """, unsafe_allow_html=True)

# ===================================================
# ACTIVE POSITION SECTION
# ===================================================
st.markdown('<div class="section-title">Active Position</div>', unsafe_allow_html=True)

if bot.state['in_position']:
    unrealized_pnl = (current_price - bot.state['entry_price']) / bot.state['entry_price'] * 100
    pnl_dollars = (current_price - bot.state['entry_price']) * bot.state['btc_holding']
    pnl_class = "metric-positive" if unrealized_pnl >= 0 else "metric-negative"
    pnl_arrow = "▲" if unrealized_pnl >= 0 else "▼"
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Entry Price</div>
            <div class="metric-value" style="font-size:20px;">${bot.state['entry_price']:,.2f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Current Price</div>
            <div class="metric-value" style="font-size:20px;">${current_price:,.2f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Coin Amount</div>
            <div class="metric-value" style="font-size:20px;">{bot.state['btc_holding']:.6f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Position Value</div>
            <div class="metric-value" style="font-size:20px;">${bot.state['position_size_usdt']:.2f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Unrealized P/L</div>
            <div class="metric-value {pnl_class}" style="font-size:20px;">{pnl_arrow} {abs(unrealized_pnl):.2f}%</div>
            <div class="metric-sub {pnl_class}">${pnl_dollars:+.2f}</div>
        </div>
        """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="position-empty">
        <div class="position-empty-icon">🔍</div>
        <div style="font-size:18px; font-weight:700; color:#9CA3AF;">Scanning Market</div>
        <div style="font-size:13px; margin-top:8px;">Bot is analyzing conditions for the next entry signal</div>
    </div>
    """, unsafe_allow_html=True)

# ===================================================
# LIVE CHART
# ===================================================
st.markdown('<div class="section-title">Live Market Chart</div>', unsafe_allow_html=True)

fig = make_subplots(
    rows=2, cols=1,
    shared_xaxes=True,
    vertical_spacing=0.03,
    row_heights=[0.75, 0.25]
)

# Candlesticks
fig.add_trace(go.Candlestick(
    x=df['timestamp'],
    open=df['open'],
    high=df['high'],
    low=df['low'],
    close=df['close'],
    name=bot.settings['symbol'],
    increasing_line_color='#10B981',
    decreasing_line_color='#EF4444',
    increasing_fillcolor='#10B981',
    decreasing_fillcolor='#EF4444'
), row=1, col=1)

# Moving Averages
fig.add_trace(go.Scatter(
    x=df['timestamp'], y=df['ma_20'],
    name='MA 20',
    line=dict(color='#3B82F6', width=2)
), row=1, col=1)

fig.add_trace(go.Scatter(
    x=df['timestamp'], y=df['ma_50'],
    name='MA 50',
    line=dict(color='#A855F7', width=2)
), row=1, col=1)

# Entry price line if in position
if bot.state['in_position']:
    fig.add_hline(
        y=bot.state['entry_price'],
        line_dash="dot",
        line_color="#F59E0B",
        line_width=2,
        annotation_text=f"Entry: ${bot.state['entry_price']:,.2f}",
        annotation_position="right",
        row=1, col=1
    )

# RSI
fig.add_trace(go.Scatter(
    x=df['timestamp'], y=df['rsi'],
    name='RSI',
    line=dict(color='#F59E0B', width=2),
    fill='tozeroy',
    fillcolor='rgba(245, 158, 11, 0.1)'
), row=2, col=1)

# RSI reference lines
fig.add_hline(y=70, line_dash="dash", line_color="#EF4444", line_width=1, row=2, col=1)
fig.add_hline(y=30, line_dash="dash", line_color="#10B981", line_width=1, row=2, col=1)
fig.add_hline(y=50, line_dash="dot", line_color="#6B7280", line_width=1, row=2, col=1)

fig.update_layout(
    template='plotly_dark',
    paper_bgcolor='rgba(19, 23, 34, 0.6)',
    plot_bgcolor='rgba(5, 8, 16, 0.8)',
    height=650,
    showlegend=True,
    xaxis_rangeslider_visible=False,
    font=dict(family="Inter", color="#F9FAFB", size=11),
    margin=dict(l=10, r=10, t=30, b=10),
    legend=dict(
        orientation="h",
        yanchor="bottom", y=1.02,
        xanchor="right", x=1,
        bgcolor='rgba(0,0,0,0)'
    )
)

fig.update_xaxes(gridcolor='rgba(255,255,255,0.05)', zerolinecolor='rgba(255,255,255,0.05)')
fig.update_yaxes(gridcolor='rgba(255,255,255,0.05)', zerolinecolor='rgba(255,255,255,0.05)')

st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

# ===================================================
# TRADE HISTORY
# ===================================================
st.markdown('<div class="section-title">Trade History</div>', unsafe_allow_html=True)

trades_df = bot.get_trades_history()
if not trades_df.empty:
    st.dataframe(
        trades_df.tail(20).iloc[::-1],
        use_container_width=True,
        hide_index=True,
        height=300
    )
else:
    st.markdown("""
    <div class="position-empty">
        <div class="position-empty-icon">📋</div>
        <div style="font-size:18px; font-weight:700; color:#9CA3AF;">No Trades Yet</div>
        <div style="font-size:13px; margin-top:8px;">Trade history will appear here once your bot executes trades</div>
    </div>
    """, unsafe_allow_html=True)

# ===================================================
# FOOTER
# ===================================================
st.markdown(f"""
<div class="footer">
    ⚡ {APP_NAME} v{APP_VERSION} · Last Sync: {datetime.now().strftime("%H:%M:%S")}
</div>
""", unsafe_allow_html=True)