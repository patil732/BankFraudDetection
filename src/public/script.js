const historyTable = document.getElementById("history");

function checkFraud() {
    const amount = document.getElementById("amount").value;
    const hour = document.getElementById("hour").value;
    const location = document.getElementById("location").value;
    const device = document.getElementById("device").value;

    // ⚠️ DEMO MODE (replace with API later)
    const probability = Math.min(1, (amount / 10000) + (hour < 6 ? 0.3 : 0));
    const riskScore = Math.round(probability * 100);

    const isFraud = probability > 0.6;

    document.getElementById("prediction").textContent =
        isFraud ? "FRAUD DETECTED" : "SAFE";
    document.getElementById("prediction").className =
        isFraud ? "fraud" : "safe";

    document.getElementById("probability").textContent =
        (probability * 100).toFixed(2) + "%";

    document.getElementById("riskScore").textContent = riskScore + "%";

    const bar = document.getElementById("riskFill");
    bar.style.width = riskScore + "%";
    bar.style.background =
        riskScore > 70 ? "#ef4444" :
        riskScore > 40 ? "#facc15" :
        "#22c55e";

    document.getElementById("riskLabel").textContent =
        riskScore > 70 ? "HIGH RISK" :
        riskScore > 40 ? "MEDIUM RISK" :
        "LOW RISK";

    addHistory(amount, location, isFraud, riskScore);
}

function addHistory(amount, location, isFraud, risk) {
    const row = document.createElement("tr");
    row.innerHTML = `
        <td>${new Date().toLocaleTimeString()}</td>
        <td>₹${amount}</td>
        <td>${location}</td>
        <td class="${isFraud ? "fraud" : "safe"}">
            ${isFraud ? "FRAUD" : "SAFE"}
        </td>
        <td>${risk}%</td>
    `;
    historyTable.prepend(row);
}
