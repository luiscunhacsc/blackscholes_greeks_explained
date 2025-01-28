import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# Black-Scholes function with Greeks calculation
def black_scholes_greeks(S, K, T, r, sigma, option_type='call'):
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    if option_type == 'call':
        price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
        delta = norm.cdf(d1)
        rho = K * T * np.exp(-r * T) * norm.cdf(d2)
    else:
        price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
        delta = norm.cdf(d1) - 1
        rho = -K * T * np.exp(-r * T) * norm.cdf(-d2)
    
    # Greeks common to both calls and puts
    gamma = norm.pdf(d1) / (S * sigma * np.sqrt(T))
    vega = S * norm.pdf(d1) * np.sqrt(T)
    theta = (- (S * norm.pdf(d1) * sigma) / (2 * np.sqrt(T)) 
             - r * K * np.exp(-r * T) * norm.cdf(d2 if option_type == 'call' else -d2))
    
    return price, delta, gamma, theta, vega, rho

# Configure the Streamlit app
st.set_page_config(layout="wide")
st.title("📊 Understanding Greeks in the Black-Scholes Model")
st.markdown("Analyze how different parameters affect option price sensitivities (Delta, Gamma, Theta, Vega, Rho).")

# Sidebar for input parameters
with st.sidebar:
    st.header("⚙️ Parameters")
    
    # Add reset button at top
    if st.button('↺ Reset Parameters'):
        st.session_state.S_slider = 100.0
        st.session_state.K_slider = 105.0
        st.session_state.T_slider = 1.0
        st.session_state.r_slider = 0.05
        st.session_state.sigma_slider = 0.2
        st.session_state.option_type_radio = 'call'
    
    S = st.slider("Current Stock Price (S)", 50.0, 150.0, 100.0, key='S_slider')
    K = st.slider("Strike Price (K)", 50.0, 150.0, 105.0, key='K_slider')
    T = st.slider("Time to Maturity (years)", 0.1, 5.0, 1.0, key='T_slider')
    r = st.slider("Risk-Free Interest Rate (r)", 0.0, 0.2, 0.05, key='r_slider')
    sigma = st.slider("Volatility (σ)", 0.1, 1.0, 0.2, key='sigma_slider')
    option_type = st.radio("Option Type", ["call", "put"], key='option_type_radio')

    # Disclaimer and license
    st.markdown("---")
    st.markdown("""
    **⚠️ Disclaimer**  
    *Educational purposes only. No accuracy guarantees.*  
    """)
    
    st.markdown("""
    <div style="margin-top: 20px;">
        <a href="https://creativecommons.org/licenses/by-nc/4.0/deed.en" target="_blank">
            <img src="https://licensebuttons.net/l/by-nc/4.0/88x31.png" alt="CC BY-NC 4.0">
        </a>
        <br>
        <span style="font-size: 0.8em;">By Luís Simões da Cunha</span>
    </div>
    """, unsafe_allow_html=True)

# Create tabs for different sections
tab1, tab2, tab3 = st.tabs(["🎮 Interactive Tool", "📚 Theory Behind the Model", "📖 Comprehensive Tutorial"])

with tab1:
    # Calculate option price and Greeks
    price, delta, gamma, theta, vega, rho = black_scholes_greeks(S, K, T, r, sigma, option_type)

    # Display results in columns
    col1, col2 = st.columns([1, 3])
    with col1:
        st.success(f"### Option Price: **€{price:.2f}**")
        
        # Table of Greeks
        st.markdown("### Sensitivities (Greeks)")
        st.markdown(f"""
        - **Delta (Δ):** `{delta:.3f}`  
          *Call: 0→1, Put: -1→0. Change per €1 stock move.*
        - **Gamma (Γ):** `{gamma:.3f}`  
          *Delta sensitivity. Peaks at ATM (same for calls/puts).*
        - **Theta (Θ):** `{theta/365:.3f}/day`  
          *Daily time decay. Generally negative for all options.*
        - **Vega (ν):** `{vega:.3f}`  
          *Volatility sensitivity. Positive for calls/puts.*
        - **Rho (ρ):** `{rho:.3f}`  
          *Rate sensitivity. Positive for calls, negative for puts.*
        """)

    with col2:
        # Select Greek to visualize
        selected_greek = st.selectbox(
            "Select a Greek to visualize:",
            ["Delta", "Gamma", "Theta", "Vega", "Rho"],
            index=0
        )
        
        # Generate graph for the selected Greek
        fig, ax = plt.subplots(figsize=(10, 5))
        S_range = np.linspace(50, 150, 100)
        
        # Calculate values for the selected Greek across the stock price range
        greek_values = []
        for s in S_range:
            _, d, g, t, v, r_val = black_scholes_greeks(s, K, T, r, sigma, option_type)
            if selected_greek == "Delta":
                greek_values.append(d)
            elif selected_greek == "Gamma":
                greek_values.append(g)
            elif selected_greek == "Theta":
                greek_values.append(t / 365)  # Daily Theta
            elif selected_greek == "Vega":
                greek_values.append(v)
            else:
                greek_values.append(r_val)
        
        ax.plot(S_range, greek_values, color='darkorange', linewidth=2)
        ax.axvline(S, color='red', linestyle='--', label='Current Stock Price (S)')
        ax.set_title(f"{selected_greek} vs Stock Price", fontweight='bold')
        ax.set_xlabel("Stock Price (S)")
        ax.set_ylabel(f"{selected_greek}")
        ax.grid(alpha=0.3)
        ax.legend()
        st.pyplot(fig)

        # Dynamic explanation for the selected Greek
        explanations = {
            "Delta": (
                "**Call/Put Behavior:**\n"
                "- Calls: 0 (far OTM) → 1 (deep ITM)\n"
                "- Puts: -1 (deep ITM) → 0 (far OTM)\n\n"
                "Delta represents the hedge ratio - shares needed to hedge the option."
            ),
            "Gamma": (
                "**Universal Sensitivity:**\n"
                "Gamma is identical for calls and puts at the same strike. "
                "It measures convexity - how Delta changes with stock price moves. "
                "Maximized at-the-money (S=K) when near expiration."
            ),
            "Theta": (
                "**Time Decay Patterns:**\n"
                "- Both calls/puts lose value over time\n"
                "- Accelerates near expiration\n"
                "- ATM options decay fastest\n\n"
                "Theta represents the daily 'cost' of holding the option."
            ),
            "Vega": (
                "**Volatility Exposure:**\n"
                "Vega is positive for all options - both calls and puts benefit from volatility. "
                "Longer-dated options have higher Vega. Peak sensitivity occurs near-the-money."
            ),
            "Rho": (
                "**Interest Rate Effects:**\n"
                "- Calls: Positive Rho (↑ rates → ↑ value)\n"
                "- Puts: Negative Rho (↑ rates → ↓ value)\n\n"
                "Most significant in long-dated options and high rate environments."
            )
        }
        st.info(f"📘 **{selected_greek} Deep Dive**\n{explanations[selected_greek]}")

with tab2:
    st.markdown("""
    ## Black-Scholes Model: Mathematical Foundation
    
    ### Model Overview
    The Black-Scholes model prices European options using these key assumptions:
    1. No arbitrage opportunities
    2. Constant volatility (σ) and risk-free rate (r)
    3. No transaction costs or dividends
    4. Underlying follows geometric Brownian motion
    
    ### Core Equations
    
    **Black-Scholes PDE**:
    $$
    \\frac{\\partial V}{\\partial t} + \\frac{1}{2}\\sigma^2S^2\\frac{\\partial^2 V}{\\partial S^2} + rS\\frac{\\partial V}{\\partial S} - rV = 0
    $$
    
    **Closed-Form Solution** (for European options):
    $$
    C(S,t) = N(d_1)S - N(d_2)Ke^{-r(T-t)}
    $$
    $$
    P(S,t) = N(-d_2)Ke^{-r(T-t)} - N(-d_1)S
    $$
    
    Where:
    $$
    d_1 = \\frac{\\ln(S/K) + (r + \\sigma^2/2)(T-t)}{\\sigma\\sqrt{T-t}}
    $$
    $$
    d_2 = d_1 - \\sigma\\sqrt{T-t}
    $$
    
    ### Greeks in Mathematical Form
    
    | Greek  | Call Option Formula                      | Put Option Formula                       |
    |--------|------------------------------------------|------------------------------------------|
    | Delta  | $N(d_1)$                                 | $N(d_1) - 1$                             |
    | Gamma  | $\\frac{N'(d_1)}{S\\sigma\\sqrt{T-t}}$   | Same as Call                             |
    | Theta  | $-\\frac{S N'(d_1)\\sigma}{2\\sqrt{T-t}} - rKe^{-r(T-t)}N(d_2)$ | $-\\frac{S N'(d_1)\\sigma}{2\\sqrt{T-t}} + rKe^{-r(T-t)}N(-d_2)$ |
    | Vega   | $S N'(d_1)\\sqrt{T-t}$                   | Same as Call                             |
    | Rho    | $K(T-t)e^{-r(T-t)}N(d_2)$                | $-K(T-t)e^{-r(T-t)}N(-d_2)$              |

    ### Connecting Theory to Practice
    
    1. **See Equations in Action**:
       - Use the interactive tool to observe how changing:
         - $S$ affects $d_1$ and Delta
         - $\\sigma$ modifies the probability distribution (Vega)
         - $T$ impacts time decay patterns (Theta)
    
    2. **Model Limitations**:
       - Assumes constant volatility (vs real-world stochastic vol)
       - No early exercise (American options)
       - Log-normal distribution may not match market returns
    
    3. **Empirical Testing**:
       - Try extreme parameters (σ=100%, T=0.01 years) to see model boundaries
       - Compare ITM/OTM Greeks to understand probability weightings
    """)
    
    # Practical exercise section
    with st.expander("🔍 Hands-On Theoretical Exercise"):
        st.markdown("""
        **Observe Delta as Probability**:
        1. Set S=100, K=100 (ATM)
        2. Set σ=20%, r=5%, T=1 year
        3. Calculate $d_1$: (ln(1) + (0.05+0.2²/2)*1)/(0.2*1) ≈ 0.325
        4. $N(d_1)$ ≈ 0.627 → Call Delta
        5. In the tool, verify Delta ≈ 0.627
        6. Repeat with different moneyness states
        
        **This shows**: Delta approximates risk-neutral probability of finishing ITM!
        """)

with tab3:
    st.markdown("""
    ## Welcome to the Black-Scholes Learning Tool!
    
    **What this tool does:**  
    This interactive calculator helps you visualize how option prices and their sensitivities (Greeks) change with market parameters. Perfect for understanding the Black-Scholes model dynamics!
    
    ### Quick Start Guide
    
    1. **Adjust Parameters** (Left Sidebar):
       - Move sliders to set stock price, strike price, etc.
       - Switch between call/put options
    
    2. **View Results** (Main Panel):
       - Real-time option price calculation
       - Greeks displayed with explanations
       - Interactive chart showing Greek behavior
    
    3. **Try These Examples**:
       - 🎚️ Drag volatility to 80% - see Vega spike (both calls/puts)
       - ⏳ Reduce time to expiration - watch Theta accelerate
       - 💹 Move stock price across strike price - observe Delta/Gamma changes
       - 🎯 Set S=K (ATM) - Notice Gamma peak (same for calls/puts)
       - 💰 Deep ITM Call (S=150, K=105): Delta ~1 → Switch to Put: Delta ~0
       - 📈 Long-term Options (T=5, r=0.15): See Rho's call/put difference
       - ⚖️ Compare Theta: T=0.1 (fast decay) vs T=1.0 (slow decay)
    
    ### Key Features to Explore
    - **Call/Put Comparisons**: Switch option type to see Greek sign changes
    - **Greek Visualizations**: See relationships through interactive charts
    - **Real-World Scenarios**: Test market conditions like rate changes
    
    **Pro Tip:** Use the reset button ↺ to quickly return to default values!
    """)