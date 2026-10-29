from flask import Flask, render_template, request
from urllib.parse import urlparse
import re

app = Flask(__name__)


def analyze_url(url):
    score = 0
    warnings = []

    test_url = url

    if not re.match(r"^https?://", test_url, re.IGNORECASE):
        test_url = "http://" + test_url

    try:
        parsed = urlparse(test_url)
        domain = parsed.netloc.lower()

        if not domain:
            return {
                "risk": "INVALID",
                "score": 100,
                "warnings": ["The URL does not appear to be valid."]
            }

        # HTTP instead of HTTPS
        if parsed.scheme == "http":
            score += 15
            warnings.append("The website uses HTTP instead of HTTPS.")

        # IP address instead of domain
        ip_pattern = r"^\d{1,3}(\.\d{1,3}){3}$"

        if re.match(ip_pattern, domain.split(":")[0]):
            score += 25
            warnings.append(
                "The link uses an IP address instead of a normal domain."
            )

        # Suspicious keywords
        suspicious_words = [
            "login",
            "verify",
            "verification",
            "password",
            "account",
            "secure",
            "security",
            "update",
            "confirm",
            "bank",
            "wallet",
            "paypal",
            "free",
            "gift",
            "prize",
            "urgent"
        ]

        found_words = []

        for word in suspicious_words:
            if word in test_url.lower():
                found_words.append(word)

        if found_words:
            score += min(len(found_words) * 5, 25)

            warnings.append(
                "Potentially sensitive or urgent keywords detected: "
                + ", ".join(found_words)
            )

        # Long URL
        if len(url) > 100:
            score += 10
            warnings.append("The URL is unusually long.")

        # @ symbol
        if "@" in url:
            score += 20
            warnings.append(
                "The URL contains '@', which can sometimes be used "
                "to disguise the destination."
            )

        # Many subdomains
        if domain.count(".") >= 3:
            score += 15
            warnings.append(
                "The domain contains an unusually large number of subdomains."
            )

        # Multiple hyphens
        if domain.count("-") >= 2:
            score += 10
            warnings.append(
                "The domain contains multiple hyphens."
            )

        # Risk classification
        if score >= 60:
            risk = "HIGH"
        elif score >= 30:
            risk = "MEDIUM"
        else:
            risk = "LOW"

        if not warnings:
            warnings.append(
                "No obvious suspicious indicators were detected."
            )

        return {
            "risk": risk,
            "score": min(score, 100),
            "warnings": warnings
        }

    except Exception:
        return {
            "risk": "INVALID",
            "score": 100,
            "warnings": ["Unable to analyze this URL."]
        }


@app.route("/", methods=["GET", "POST"])
def home():

    result = None
    submitted_url = ""

    if request.method == "POST":

        submitted_url = request.form.get("url", "").strip()

        if submitted_url:
            result = analyze_url(submitted_url)

        else:
            result = {
                "risk": "INVALID",
                "score": 100,
                "warnings": ["Please enter a URL."]
            }

    return render_template(
        "index.html",
        result=result,
        submitted_url=submitted_url
    )


if __name__ == "__main__":
    app.run(debug=True)