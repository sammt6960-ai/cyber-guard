
const scanForm = document.getElementById("scan-form");
const urlInput = document.getElementById("url-input");
const scanButton = document.getElementById("scan-button");

const loading = document.getElementById("loading");
const errorMessage = document.getElementById("error-message");
const results = document.getElementById("results");

const riskBadge = document.getElementById("risk-badge");
const riskScore = document.getElementById("risk-score");
const scoreBar = document.getElementById("score-bar");
const resultHost = document.getElementById("result-host");
const resultSummary = document.getElementById("result-summary");
const findingsList = document.getElementById("findings-list");
const noFindings = document.getElementById("no-findings");
const disclaimer = document.getElementById("disclaimer");

function showError(message) {
    errorMessage.textContent = message;
    errorMessage.classList.remove("hidden");
}

function resetResults() {
    results.classList.add("hidden");
    errorMessage.classList.add("hidden");
    loading.classList.add("hidden");
}

function displayResults(data) {
    results.classList.remove("hidden");

    resultHost.textContent = "Hostname: " + data.hostname;
    riskScore.textContent = data.score;
    resultSummary.textContent = data.message;
    disclaimer.textContent = data.disclaimer;

    riskBadge.textContent = data.risk + " Risk";
    riskBadge.className = "risk-badge " + data.risk.toLowerCase();

    scoreBar.style.width = data.score + "%";
    scoreBar.className = "score-bar " + data.risk.toLowerCase();

    findingsList.replaceChildren();

    for (const finding of data.findings) {
        const item = document.createElement("li");
        item.textContent = finding;
        findingsList.appendChild(item);
    }

    noFindings.classList.toggle("hidden", data.findings.length !== 0);

    results.scrollIntoView({
        behavior: "smooth",
        block: "nearest"
    });
}

scanForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const url = urlInput.value.trim();

    resetResults();

    if (!url) {
        showError("Please enter a URL to analyze.");
        urlInput.focus();
        return;
    }

    loading.classList.remove("hidden");
    scanButton.disabled = true;
    scanButton.textContent = "Analyzing...";

    try {
        const response = await fetch("/api/check", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ url })
        });

        const data = await response.json();

        if (!response.ok || !data.valid) {
            throw new Error(data.error || "Unable to analyze this URL.");
        }

        displayResults(data);

    } catch (error) {
        showError(
            error.message || "Could not contact the server. Is Flask running?"
        );
    } finally {
        loading.classList.add("hidden");
        scanButton.disabled = false;
        scanButton.textContent = "Analyze URL";
    }
});
