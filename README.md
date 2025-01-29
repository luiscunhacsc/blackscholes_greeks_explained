
# Black-Scholes Greeks Explained

## 1. What Is This?

The **Black-Scholes model** is a mathematical model used for pricing options. The "Greeks" (Delta, Gamma, Theta, Vega, Rho) are metrics that measure how the price of an option changes with various factors (like the price of the underlying asset, the time to expiration, volatility, etc.).

This project includes a small interactive application where you can:
- Input option parameters (strike price, underlying price, volatility, risk-free rate, time to expiration).
- Visualize how each Greek changes as you alter these parameters.

## How to run the application: 

Please try clicking this link. It should work. If not, you will have to download it to your computer and run it locally. The steps for that are bellow. 🙏😊

[![Open in Streamlit](https://img.shields.io/badge/Streamlit-Run_App-brightgreen.svg)](https://blackscholesgreeksexplained-frzywp64wynitx7vzm7ptt.streamlit.app/)



## 2. Prerequisites (to change the code and play around with it)

1. **A computer** (Windows, macOS, or Linux).
2. **Python 3.9 or higher** (Python 3.12 preferred, but anything 3.9+ should be fine).
   - If you do not have Python installed:
     - Go to [python.org/downloads](https://www.python.org/downloads/) and download/install the latest version for your operating system.
3. **Git** (optional, but recommended to clone the repository directly).
   - If you do not have Git:
     - Go to [git-scm.com/downloads](https://git-scm.com/downloads) and download/install Git for your operating system.

*(If you are completely new to GitHub, you can skip installing Git and just download the project as a ZIP file. See details in [Section 3.2](#32-download-as-zip-file).)*

## 3. Downloading the Project

There are two main ways to get the files from GitHub onto your computer.

### 3.1 Cloning via Git (Recommended)

1. Open the **Terminal** (on macOS or Linux) or the **Command Prompt** / **PowerShell** (on Windows).
2. Navigate to the folder where you want to download the project. For example:
   ```bash
   cd Documents
   ```
3. Run this command to clone the repository:
   ```bash
   git clone https://github.com/luiscunhacsc/blackscholes_greeks_explained.git
   ```
4. After downloading, go into the project folder:
   ```bash
   cd blackscholes_greeks_explained
   ```

### 3.2 Download as ZIP File

1. Go to the repository page in your web browser:  
   [https://github.com/luiscunhacsc/blackscholes_greeks_explained](https://github.com/luiscunhacsc/blackscholes_greeks_explained)
2. Click on the green **Code** button.
3. Select **Download ZIP**.
4. Locate the downloaded ZIP file on your computer (usually in your *Downloads* folder).
5. **Unzip** (extract) the file into a folder (for example, `C:\Users\YourName\Documents\blackscholes_greeks_explained` on Windows).

## 4. Installing Dependencies

The project includes a file named `requirements.txt` that lists all the packages you need. This makes installing the dependencies straightforward.

1. Open your **Terminal** (macOS/Linux) or **Command Prompt** / **PowerShell** (Windows).
2. Navigate to the folder where you have the files. For instance, if you extracted the ZIP to `C:\Users\YourName\Documents\blackscholes_greeks_explained`, then:
   ```bash
   cd "C:\Users\YourName\Documents\blackscholes_greeks_explained"
   ```
   *(On macOS or Linux, change the path accordingly.)*
3. Make sure you have **pip** (the Python package manager) updated. You can upgrade pip with:
   ```bash
   python -m pip install --upgrade pip
   ```
   *(On some systems, you might use `python3` instead of `python`.)*

4. Install the required packages using the `requirements.txt` file:
   ```bash
   pip install -r requirements.txt
   ```
   This will install:
   - streamlit
   - numpy
   - scipy
   - matplotlib
   - setuptools

   *(If you see any warnings or prompts, just follow the instructions.)*

## 5. Running the Application

Once you have installed the dependencies, you can launch the Streamlit application.

1. Still in the **Terminal** / **Command Prompt**, ensure you are in the project folder.  
2. Run the command:
   ```bash
   streamlit run blacksmodels.py
   ```
   or:
   ```bash
   streamlit run v1.py
   ```
   *(Choose the file your application code is actually in; check the repository for the exact filename. Often `v1.py` or `blacksmodels.py` might be the main file.)*

3. A new tab or window will open in your **default web browser** showing the interactive application. If it does not open automatically, look at the Terminal output—Streamlit will give you a local URL such as `http://localhost:8501`. You can copy and paste that URL into your browser’s address bar to open the app.

### 5.1 Troubleshooting

- **Streamlit not found**:  
  Make sure you installed the dependencies correctly:
  ```bash
  pip install -r requirements.txt
  ```
- **Permission errors**:  
  On Windows, try running your command prompt or PowerShell as Administrator (right-click, “Run as administrator”). On macOS/Linux, you might need to use `sudo` if there are permission issues (though normally not recommended, it’s an option if you are stuck).
- **Python not found**:  
  Ensure Python is added to your system’s PATH. Re-install Python and select the option “Add Python to PATH” (on Windows) if needed.
- **Browser not opening**:  
  Copy the URL from the terminal (something like `http://localhost:8501`) and paste it into your browser manually.

## 6. Using the Application

After the application opens in your web browser, you’ll see various input fields and graphs. A typical workflow is:

1. **Enter option parameters** like:
   - **Underlying Price** (current stock price)
   - **Strike Price** (the option’s strike)
   - **Volatility** (σ)
   - **Risk-Free Rate** (annual)
   - **Time to Expiration** (in years)
2. **Adjust the sliders or text inputs** to see how each Greek (Delta, Gamma, Theta, Vega, Rho) changes.
3. The plots or numerical outputs will **update in real-time**, letting you explore the Black-Scholes Greeks.

## 7. Editing the Code (Optional)

If you want to make changes:

1. Open the `.py` files in a text editor or IDE (like Visual Studio Code, PyCharm, or JupyterLab).
2. Modify the code (e.g., add new parameters, change the layout).
3. Save your changes.
4. Restart the Streamlit app by closing it (Ctrl + C in the terminal) and re-running:
   ```bash
   streamlit run v1.py
   ```

## 8. Additional Resources

- **Streamlit Documentation**: [docs.streamlit.io](https://docs.streamlit.io)  
  Learn more about how Streamlit works to build interactive data apps quickly.
- **Black-Scholes Model**:  
  - [Wikipedia](https://en.wikipedia.org/wiki/Black%E2%80%93Scholes_model)
  - [Investopedia Guide](https://www.investopedia.com/terms/b/blackscholes.asp)

## 9. Support

If you have any questions, issues, or suggestions, feel free to:

- [Open an Issue](https://github.com/luiscunhacsc/blackscholes_greeks_explained/issues) in this repository.
- Contact the repository owner (check the GitHub profile or email if listed).

---

*Happy exploring the Black-Scholes Greeks!*