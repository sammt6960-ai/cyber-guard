
# Cyber Guard 🛡️

Cyber Guard is an educational cybersecurity web application built with
Python, Flask, HTML, CSS, and JavaScript.

## Features

- Suspicious URL analysis using local heuristic rules
- Risk score and Low, Medium, or High indicator
- Explanations of detected URL characteristics
- Responsive dark cybersecurity dashboard
- Cybersecurity awareness tips
- Flask JSON API
- No external API key required

## Technology Stack

- Python
- Flask
- HTML5
- CSS3
- JavaScript

## Installation

1. Install Python 3.11 or newer.
2. Clone this repository or download the project.
3. Open a terminal in the project directory.
4. Create a virtual environment:

   ```bash
   python -m venv .venv
   ```

5. Activate it on Windows:

   ```powershell
   .venv\Scripts\Activate.ps1
   ```

   If you use Command Prompt instead:

   ```bat
   .venv\Scripts\activate.bat
   ```

6. Install dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

7. Start the application:

   ```bash
   python app.py
   ```

8. Open http://127.0.0.1:5000 in your browser.

## API Example

Send a POST request to `/api/check` with JSON:

```json
{
  "url": "https://example.com"
}
```

The response includes the hostname, heuristic score, risk category,
detected indicators, and a disclaimer.

## Limitations

Cyber Guard does not use a live threat-intelligence database, inspect
website content, follow redirects, or prove that a website is safe.

A low score does not guarantee that a URL is legitimate. A high score
does not prove that it is malicious.

This project is intended for learning and demonstration.

## Security Note

Flask debug mode is enabled for local development only. Disable debug
mode and configure a production WSGI server before deploying publicly.

## Author

Cybersecurity student and aspiring cybersecurity professional.
