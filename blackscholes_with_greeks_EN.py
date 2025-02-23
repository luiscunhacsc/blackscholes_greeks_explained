import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

#######################################
# 1) Define two callback functions:
#    - One to reset defaults
#    - One to set Lab 1 parameters
#######################################
def reset_parameters():
    st.session_state["S_slider"] = 100.0
    st.session_state["K_slider"] = 105.0
    st.session_state["T_slider"] = 1.0
    st.session_state["r_slider"] = 0.05
    st.session_state["sigma_slider"] = 0.2
    st.session_state["option_type_radio"] = 'call'

def set_lab1_parameters():
    st.session_state["S_slider"] = 100.0
    st.session_state["K_slider"] = 100.0
    st.session_state["T_slider"] = 0.08  # ~1 month
    st.session_state["r_slider"] = 0.02
    st.session_state["sigma_slider"] = 0.4
    st.session_state["option_type_radio"] = 'call'
#######################################

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
    
    gamma = norm.pdf(d1) / (S * sigma * np.sqrt(T))
    vega = S * norm.pdf(d1) * np.sqrt(T)
    theta = (
        - (S * norm.pdf(d1) * sigma) / (2 * np.sqrt(T))
        - r * K * np.exp(-r * T) * norm.cdf(d2 if option_type == 'call' else -d2)
    )
    
    return price, delta, gamma, theta, vega, rho

# Configure the Streamlit app
st.set_page_config(layout="wide")
st.title("📊 Understanding Greeks in the Black-Scholes Model")
st.markdown("Analyze how different parameters affect option price sensitivities (Delta, Gamma, Theta, Vega, Rho).")

# Sidebar for input parameters
with st.sidebar:
    st.header("⚙️ Parameters")
    
    #######################################
    # 2) Use callbacks on both buttons
    #######################################
    st.button("↺ Reset Parameters", on_click=reset_parameters)

    S = st.slider("Current Stock Price (S)", 50.0, 150.0, 100.0, key='S_slider')
    K = st.slider("Strike Price (K)", 50.0, 150.0, 105.0, key='K_slider')
    T = st.slider("Time to Maturity (years)", 0.1, 5.0, 1.0, key='T_slider')
    r = st.slider("Risk-Free Interest Rate (r)", 0.0, 0.2, 0.05, key='r_slider')
    sigma = st.slider("Volatility (σ)", 0.1, 1.0, 0.2, key='sigma_slider')
    option_type = st.radio("Option Type", ["call", "put"], key='option_type_radio')

    # Disclaimer and license
    st.markdown("---")
    st.markdown(
    """
    **⚠️ Disclaimer**  
    *Educational purposes only. No accuracy guarantees. Do not use options as an investment tool if you are not a qualified professional investor.*  
    
    <small>
    The author does not engage in option trading and does not endorse it for non-professional investors. 
    All information provided is for educational purposes only and should not be construed as financial or 
    investment advice. Option trading involves significant risks and may not be suitable for all investors. 
    Always consult a qualified financial professional before making any investment decisions.
    </small>
    """,
    unsafe_allow_html=True
    )

    
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
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🎮 Interactive Tool", 
    "📚 Theory Behind the Model", 
    "📖 Comprehensive Tutorial", 
    "🛠️ Practical Labs",
    "🧠 The Very Basics of Options"
])

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
        for s_val in S_range:
            _, d, g, t_, v_, r_val_ = black_scholes_greeks(s_val, K, T, r, sigma, option_type)
            if selected_greek == "Delta":
                greek_values.append(d)
            elif selected_greek == "Gamma":
                greek_values.append(g)
            elif selected_greek == "Theta":
                greek_values.append(t_ / 365)  # Daily Theta
            elif selected_greek == "Vega":
                greek_values.append(v_)
            else:  # Rho
                greek_values.append(r_val_)
        
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

########################################
# Define parameter-setting callbacks
########################################
def set_lab1_parameters():
    st.session_state["S_slider"] = 100.0
    st.session_state["K_slider"] = 100.0
    st.session_state["T_slider"] = 0.08  # ~1 month
    st.session_state["r_slider"] = 0.02
    st.session_state["sigma_slider"] = 0.4
    st.session_state["option_type_radio"] = 'call'

def set_lab2_parameters():
    st.session_state["S_slider"] = 100.0
    st.session_state["K_slider"] = 100.0
    st.session_state["T_slider"] = 0.5   # 6 months
    st.session_state["r_slider"] = 0.02
    st.session_state["sigma_slider"] = 0.4
    st.session_state["option_type_radio"] = 'call'

def set_lab3_parameters():
    st.session_state["S_slider"] = 100.0
    st.session_state["K_slider"] = 100.0
    st.session_state["T_slider"] = 0.02  # ~1 week
    st.session_state["r_slider"] = 0.01
    st.session_state["sigma_slider"] = 0.2
    st.session_state["option_type_radio"] = 'call'

def set_lab4_parameters():
    st.session_state["S_slider"] = 100.0
    st.session_state["K_slider"] = 100.0
    st.session_state["T_slider"] = 0.1   # ~1.2 months
    st.session_state["r_slider"] = 0.02
    st.session_state["sigma_slider"] = 0.2
    st.session_state["option_type_radio"] = 'call'

def set_lab5_parameters():
    st.session_state["S_slider"] = 100.0
    st.session_state["K_slider"] = 100.0
    st.session_state["T_slider"] = 2.0   # 2 years
    st.session_state["r_slider"] = 0.05
    st.session_state["sigma_slider"] = 0.2
    st.session_state["option_type_radio"] = 'call'


########################################
# Tab 4: Practical Labs (Accordion style via Radio)
########################################
with tab4:
    st.header("🔬 Practical Option Labs")
    st.markdown("""
    Welcome to the **Practical Option Labs** section! Each lab provides a real-world scenario or demonstration 
    to help you apply the Black-Scholes formula and the Greeks in a hands-on way.
    
    Use the **"Set Lab Parameters"** buttons to jump directly to recommended settings for each scenario.
    Experiment, take notes, and enjoy exploring how options behave under different market conditions!
    """)

    # --- Additional Disclaimer ---
    st.warning("""
    **Disclaimer**:  
    The author does *not* use options or option trading as an investment strategy, 
    nor does he recommend that any retail investor should. 
    This material is purely for educational and illustrative purposes.
    """)

    # A radio to choose one of the labs
    lab_choice = st.radio(
        "Select a lab to view:",
        ("Lab 1: Delta Hedging",
         "Lab 2: Gamma Scalping",
         "Lab 3: Time Decay",
         "Lab 4: Volatility Shocks",
         "Lab 5: Interest Rates & Rho"),
        index=0
    )

    # ---------------- Lab 1 ----------------
    if lab_choice == "Lab 1: Delta Hedging":
        st.subheader("🏦 Lab 1: Delta Hedging in a Volatile Market")
        st.markdown("""
        **Real-World Scenario:**  
        You're a portfolio manager holding **100 call options** during earnings season. The stock is **highly volatile**.  
        Your goal is to **stay delta-neutral**, meaning that the overall portfolio (options + shares) has a net Delta near zero. 
        This helps you avoid large directional gains or losses if the stock moves suddenly.

        ---
        **Beginner Explanation of What's Happening:**

        - **Call Options**: Owning a call gives you positive Delta (usually between 0 and 1 per contract). 
          For example, if one call has Δ=0.50, holding 100 calls gives a total Delta of 50 (0.50 × 100).

        - **Owning vs. Shorting Shares**: 
          - If your net Delta is +50, you can **short 50 shares** to bring total Delta to zero. 
          - If the stock price rises, your short shares lose money but the calls gain value—ideally canceling out.

        - **Why Hedge?**  
          - Delta-hedging removes immediate exposure to price moves, letting you potentially profit from other factors 
            (like time decay or changes in volatility).  
          - As the stock price changes, Delta changes too, so you must **rebalance** your share position periodically 
            (dynamic hedging).

        **Learning Objective:**  
        - Understand how **Delta** acts as a hedge ratio.
        - Practice adjusting your share position to keep the overall Delta near zero.

        ---
        **Suggested Steps**:
        1. Click "**Set Lab 1 Parameters**" to use S=100, K=100, T=1 month, σ=40%, r=2%.
        2. Look at the **Delta** displayed in the main tool tab.  
           Holding 100 calls → net Delta = 100 × (option's Δ).  
        3. If the stock jumps to S=105, see how Δ changes.  
        4. Recalculate how many shares to short:  
           `Shares Needed = - (New Delta) × (Number of Contracts)`.
        5. Repeat as the stock moves around and observe how often you might rebalance.

        **💡 Reflection Questions:**  
        - Why do ATM calls typically have Δ around 0.5?  
        - How does a higher σ (volatility) affect how quickly Δ changes (i.e., Gamma)?  
        - What happens to Δ and Gamma as expiration approaches?
        """)

        # Button to set recommended Lab 1 parameters
        st.button("⚡ Set Lab 1 Parameters", on_click=set_lab1_parameters, key="lab1_setup")

    # ---------------- Lab 2 ----------------
    elif lab_choice == "Lab 2: Gamma Scalping":
        st.subheader("💥 Lab 2: Gamma Scalping & The 'Convexity' Effect")
        st.markdown("""
        **Real-World Scenario:**  
        You hold a position that is **long Gamma** (e.g., a long call + short put at the same strike, or any 
        net-positive Gamma strategy). When the stock makes big moves (up or down), your Delta shifts in a way 
        that can be **profitable** if you rebalance your share position frequently. This is known as 
        **Gamma scalping** or **Gamma trading**.

        **Learning Objective:**  
        - Observe how **Gamma** is the rate of change of Delta with respect to the underlying price.
        - Understand why having large Gamma can help you profit from volatility if you actively manage your Delta.

        ---
        **Suggested Steps**:
        1. Click "**Set Lab 2 Parameters**" to pick an ATM strike, T=6 months, σ=40%.
        2. Go to the main tool tab and note the **Gamma**. 
        3. Move the **Stock Price (S)** slider around 90–110. Watch how Delta changes.
        4. Think about how you'd buy low and sell high in the underlying shares each time 
           Delta changes to lock in small gains.

        **Key Insight**:  
        - **High Gamma** → Delta changes quickly with small price moves → more frequent rebalancing opportunities 
          → potential to "scalp" the market if realized volatility is high enough.

        **💡 Reflection Questions:**  
        - How does Gamma behave as your option goes deeper ITM or OTM?  
        - Why is Gamma typically **highest near-the-money** and **near expiration**?
        """)
        st.button("⚡ Set Lab 2 Parameters", on_click=set_lab2_parameters, key="lab2_setup")

    # ---------------- Lab 3 ----------------
    elif lab_choice == "Lab 3: Time Decay":
        st.subheader("⏳ Lab 3: Time Decay (Theta) in Short-Dated Options")
        st.markdown("""
        **Real-World Scenario:**  
        You've **sold** a short-term (1-week) **ATM call**. Each day that passes, the option loses **time value** 
        (Theta), which benefits you if you're short. However, if the stock moves quickly, you could face losses.

        **Learning Objective:**  
        - Investigate how **Theta** (daily time decay) behaves for near-expiration options.
        - Compare it against the risk of big adverse moves (Gamma risk).

        ---
        **Suggested Steps**:
        1. Click "**Set Lab 3 Parameters**" to automatically pick S=100, K=100, T=0.02 yrs (≈1 week).
        2. Check **Theta** in the main results panel (shown in per-day terms).
        3. Move the stock price around or adjust the strike to see how Theta changes. 
        4. Increase T to 1 year. Notice how daily Theta is smaller for a longer-dated option.

        **Why This Matters**:  
        - Short-term, near-the-money options have **significant** daily time decay. 
        - Option sellers can profit from this, but face a high Gamma risk if the stock swings around.

        **💡 Reflection Questions:**  
        - Why do deeply ITM or far OTM options have relatively smaller Theta near expiration?  
        - How does high volatility interact with Theta?
        """)
        st.button("⚡ Set Lab 3 Parameters", on_click=set_lab3_parameters, key="lab3_setup")

    # ---------------- Lab 4 ----------------
    elif lab_choice == "Lab 4: Volatility Shocks":
        st.subheader("🌩️ Lab 4: Volatility Shocks (Vega) and Market Repricing")
        st.markdown("""
        **Real-World Scenario:**  
        You own a **long straddle** (long call + long put) on a stock about to announce earnings. 
        A jump in implied volatility (IV) can significantly increase the option’s price, 
        even if the stock doesn’t move much initially. This is a **long Vega** position.

        **Learning Objective:**  
        - Understand how **Vega** measures sensitivity to changes in implied volatility σ.
        - See why a volatility "crush" after earnings could harm long Vega traders, or help short Vega traders.

        ---
        **Suggested Steps**:
        1. Click "**Set Lab 4 Parameters**": S=100, K=100, T=0.1 yrs, σ=20%.
        2. Look at **Vega** in the main results panel. 
        3. Increase σ to 40% or 50%. Notice the jump in option price. 
        4. If you had a long straddle, you'd profit from a rise in IV. 
           Conversely, if IV plummets, those options lose extrinsic value quickly.

        **Takeaway**:  
        - **Long Vega** = Gains from rising IV, loses from falling IV.  
        - **Short Vega** = Gains from IV drops but suffers if IV spikes.

        **💡 Reflection Questions:**  
        - Would you prefer to be long or short Vega ahead of a known volatility event (e.g., earnings)?  
        - Does Vega’s magnitude depend on time to expiration (T) and strike moneyness?
        """)
        st.button("⚡ Set Lab 4 Parameters", on_click=set_lab4_parameters, key="lab4_setup")

    # ---------------- Lab 5 ----------------
    else:  # lab_choice == "Lab 5: Interest Rates & Rho"
        st.subheader("💹 Lab 5: Interest Rates & Rho — Impact on Calls vs. Puts")
        st.markdown("""
        **Real-World Scenario:**  
        In a rising interest rate environment (e.g., rates going from 2% to 5–10%), 
        how do **calls** vs. **puts** react? Rho is often neglected at low rates but becomes significant at higher levels. 
        For longer-dated options, a rate hike can substantially affect pricing.

        **Learning Objective:**  
        - Examine **Rho**, which measures the option price’s sensitivity to interest rates (r).
        - Compare how call Rho (positive) vs. put Rho (negative) changes the option value.

        ---
        **Suggested Steps**:
        1. Click "**Set Lab 5 Parameters**": T=2 years, r=5%, S=100, K=100, σ=20%.
        2. Compare Rho for a call vs. a put in the main tool. 
        3. Increase r to 0.15 (15%) and see how the call’s value jumps while the put’s value drops.

        **Use Case**:  
        - In a **high-rate** environment, calls become relatively more expensive (positive Rho), 
          while puts can lose value (negative Rho).

        **💡 Reflection Questions:**  
        - Why do higher rates boost call prices and lower put prices?  
        - Does Rho matter much for short-dated options?  
        - How might you hedge interest rate exposure on long-dated options?
        """)
        st.button("⚡ Set Lab 5 Parameters", on_click=set_lab5_parameters, key="lab5_setup")


with tab5:
    st.header("🧠 The Very Basics of Options")

    # Modern UI-style disclaimer (Bootstrap-like "alert-danger")
    st.markdown("""
<div style="
    background-color: #f8d7da; 
    color: #721c24; 
    padding: 20px; 
    border-radius: 8px; 
    margin-bottom: 20px;
">
  <h4 style="margin-top: 0;">
    <strong>IMPORTANT DISCLAIMER</strong>
  </h4>
  <ul style="list-style-type: disc; padding-left: 1.5em;">
    <li>Options are a <em>powerful, complex tool</em> widely used by professional investors who typically have 
      <strong>many years of formal education and intensive training</strong>.</li>
    <li>Even these professionals often <strong>fail to outperform</strong> a simple buy-and-hold strategy 
      in a diversified index, as <strong>Warren Buffett</strong> and numerous 
      <strong>Nobel Prize-winning economists</strong> have demonstrated.</li>
    <li>The reality is that <strong>markets are smarter</strong> than any individual, making consistent 
      outperformance extremely difficult.</li>
    <li>If you’d like more insight into how challenging it is to "beat the market," watch 
      <a href="https://www.youtube.com/watch?v=SwkjqGd8NC4" 
         style="color: #721c24; text-decoration: underline;">How to Win the Loser's Game: Full Version</a>, 
      and explore the 
      <a href="https://rationalreminder.ca/podcast" 
         style="color: #721c24; text-decoration: underline;">Rational Reminder podcast</a>.</li>
    <li>The author’s main interest here is <strong>intellectual curiosity</strong> about the science and tools of finance, 
      not promoting active option trading.</li>
    <li>This material is <strong>purely educational</strong>. The author does <strong>not</strong> recommend any retail investor 
      engage in options trading.</li>
  </ul>
</div>
""", unsafe_allow_html=True)

    st.markdown("""
    ### 1. What Are Options?

    **Options** are **contracts** that let you "lock in" a price to **buy** or **sell** a stock, 
    without forcing you to actually do it. Think of them like a **reservation**:
    - A **Call Option** is a reservation to **buy** a stock at a certain *strike price* before the option expires.
    - A **Put Option** is a reservation to **sell** a stock at a certain *strike price* before the option expires.

    If it ends up being a good deal (e.g., the stock price goes above your call's strike), 
    you can use your option ("exercise" it). If not, you can simply let it expire. 
    You **never** have to use your reservation.

    ---

    ### 2. Why Do People Use Options?

    1. **To Potentially Profit If the Market Moves**  
       - If you think a stock will go **up**, you might **buy a call**. 
         When the stock does rise above your strike, your option can become **very valuable**.
       - If you think it'll go **down**, you might **buy a put**. 
         If the stock price falls below your put's strike, you can sell at that higher fixed price.

    2. **To Protect Existing Stocks (Hedging)**  
       - If you **already own** shares and worry about a drop in price, 
         you can buy a **put** as insurance. If the stock falls a lot, 
         your put can offset some of the losses.

    3. **To Earn Income**  
       - Some people **sell** options (like selling insurance). 
         They collect money upfront (the premium), but if the market moves 
         strongly in the buyer's favor, the seller has significant risk.

    ---

    ### 3. A Simple Example

    - **Buying a Call** on a stock at €100 (strike) for a €2 premium:
      - If the stock price goes to €110, you can buy it at €100 using your call 
        and potentially sell it at €110 in the market. That could yield a profit 
        (minus the €2 you paid).
      - If the stock never goes above €100, you won't use your call. 
        You just lose the €2 you paid.

    This is similar to paying for a ticket that might be valuable later if conditions are right.

    ---

    ### 4. How People Trade Options on a Broker Platform

    1. **Pick a Stock** (e.g., Apple).
    2. **Select an Expiration Date** (maybe 1 month or 6 months from now).
    3. **Choose a Strike Price** (the price you're locking in).
    4. **Choose Call or Put** (buy or sell):
       - **Buy a Call**: You pay the premium to have the right to buy the stock.
       - **Buy a Put**: You pay the premium to have the right to sell the stock.
       - **Sell a Call/Put**: You collect the premium but take on the obligation 
         if the buyer exercises their right.

    Once you confirm, your broker shows your option position in your account. 
    The value of that position changes day by day, based on:
    - The stock’s price changing,
    - Time passing (options lose value as they get closer to expiration, all else equal),
    - Changes in market volatility (bigger expected swings often make options more expensive).

    ---

    ### 5. What Is the Black-Scholes Model?

    This is a **mathematical formula** to figure out a "fair" price for an option, 
    assuming you know:
    - How volatile the stock is (σ),
    - How much time remains (T),
    - What the stock price (S) and strike (K) are,
    - The risk-free interest rate (r).

    Professionals use this model to **estimate** how much an option should cost 
    and to see how sensitive it is to changes in the stock price or volatility.

    ---

    ### 6. Understanding "Delta Hedging" (An Advanced, But Important Idea)

    - **Delta** is just a number that tells you **how much** an option's price might 
      change if the stock moves by €1.
    - For example, if a call has a Delta of 0.50, that means if the stock price goes up by €1, 
      the call might increase by about €0.50.

    **Delta hedging** means:
    1. You figure out your total Delta. 
       - For instance, if you own 2 call options (each covering 100 shares) 
         and each has Delta = 0.50, your total Delta is 0.50 × 200 = 100. 
         (It's as if you own 100 shares.)
    2. If you **don’t** want to be exposed to big stock moves, you can **short 100 shares** 
       (i.e., borrow shares and sell them). 
       - This way, if the stock price goes up, you **lose** on the short shares but **gain** on the calls, 
         roughly canceling out.
    3. If the stock price goes down, your calls lose some value, but the short shares gain.
    4. Because Delta changes as the stock price moves (Gamma effect), professionals keep **rebalancing**. 
       This is **dynamic hedging**—they’re constantly adjusting how many shares they hold short (or long).

    **Why do it?**  
    - Professionals often want to earn money from **time decay** or changes in volatility, 
      rather than guessing whether a stock goes up or down. By hedging Delta, 
      they remove the "directional" risk.

    ---

    ### 7. What Professional Investors Do

    1. **Hedging a Portfolio**: 
       If a big fund owns many stocks, it might buy puts for protection, 
       or it might use Delta hedging to keep overall risk manageable.
    2. **Speculating (Directional Bets)**: 
       If they strongly believe a stock will rise, 
       they might buy calls to amplify potential gains with less initial cash outlay.
    3. **Collecting Premiums (Selling Options)**: 
       Some funds or traders sell options regularly, aiming to profit from the "time decay" 
       if prices don’t move dramatically.

    ---

    ### 8. Key Takeaways (No Jargon)

    - **Options** let you fix a buy or sell price in the future, but you only exercise if it benefits you.
    - **Call** = right to buy; **Put** = right to sell.
    - **Black-Scholes** is a famous formula to help price options and understand their risk.
    - **Delta Hedging** is when you buy or sell shares to **balance out** (hedge) the effect of price moves on your option position.
    - **Even professionals** find it difficult to beat a diversified index fund consistently.
    - **Professional Investors** often combine options with shares to manage risk or speculate, 
      adjusting positions (sometimes daily) to keep their profits and losses more predictable.
    """)
