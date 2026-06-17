## 🚀 How to Run the Application

Follow these steps to set up your virtual environment and launch the Streamlit app.

### 1. Activate the Virtual Environment
Choose the command that matches your Operating System and Terminal:

* **Windows (Command Prompt):**
    ```cmd
    .venv\Scripts\activate.bat
    ```
* **Windows (PowerShell):**
    ```powershell
    .venv\Scripts\Activate.ps1
    ```
* **macOS / Linux:**
    ```bash
    source .venv/bin/activate
    ```

### 2. Install Dependencies
Once your virtual environment is active (you should see `(.venv)` at the beginning of your terminal line), install the required packages:

```cmd
pip install -r requirements.txt
```

3. Launch the App
Run the Streamlit server to open the app in your browser:

```cmd
streamlit run app.py
```
💡 Tip: If the browser doesn't open automatically, copy and paste the Local URL (usually http://localhost:8501) from your terminal into your web browser.