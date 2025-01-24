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
    S = st.slider("Current Stock Price (S)", 50.0, 150.0, 100.0)
    K = st.slider("Strike Price (K)", 50.0, 150.0, 105.0)
    T = st.slider("Time to Maturity (years)", 0.1, 5.0, 1.0)
    r = st.slider("Risk-Free Interest Rate (r)", 0.0, 0.2, 0.05)
    sigma = st.slider("Volatility (σ)", 0.1, 1.0, 0.2)
    option_type = st.radio("Option Type", ["call", "put"])

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
      *Change in option price for a €1 change in the stock price.*
    - **Gamma (Γ):** `{gamma:.3f}`  
      *Change in Delta for a €1 change in the stock price.*
    - **Theta (Θ):** `{theta:.3f}/day`  
      *Daily loss in value due to time decay.*
    - **Vega (ν):** `{vega:.3f}`  
      *Impact of a 1% increase in volatility.*
    - **Rho (ρ):** `{rho:.3f}`  
      *Impact of a 1% increase in interest rates.*
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
        "Delta": "Delta measures the sensitivity of the option price to changes in the underlying stock price. Higher Delta means the option closely tracks the stock price.",
        "Gamma": "Gamma reflects the rate of change in Delta. High Gamma indicates greater sensitivity of Delta to stock price changes.",
        "Theta": "Theta measures the rate of time decay in the option's value. As expiration approaches, Theta increases in magnitude.",
        "Vega": "Vega measures the sensitivity of the option price to changes in volatility. Higher Vega means the option is more affected by volatility changes.",
        "Rho": "Rho measures the sensitivity of the option price to changes in interest rates. It is more significant for options with longer expirations."
    }
    st.info(f"📘 **{selected_greek}:** {explanations[selected_greek]}")
