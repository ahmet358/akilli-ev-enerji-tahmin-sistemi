(() => {
    "use strict";

    const forms = document.querySelectorAll(".needs-validation");
    forms.forEach((form) => {
        form.addEventListener("submit", (event) => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add("was-validated");
        });
    });

    const plotlyConfig = { responsive: true, displayModeBar: false };
    const chartLayout = (title) => ({
        title: { text: title, font: { size: 15 } },
        margin: { l: 48, r: 18, t: 48, b: 54 },
        paper_bgcolor: "rgba(0,0,0,0)",
        plot_bgcolor: "rgba(0,0,0,0)",
        font: { family: "Inter, system-ui, sans-serif", color: "#17202a" },
    });

    window.akilliEnerjiDashboardHazirla = () => {
        const veri = window.akilliEnerjiGrafikleri || { tahminler: [], modeller: [] };
        const predictionElement = document.getElementById("predictionChart");
        const modelElement = document.getElementById("modelChart");

        if (predictionElement) {
            const x = veri.tahminler.map((item) => item.etiket);
            const y = veri.tahminler.map((item) => item.deger);
            Plotly.newPlot(
                predictionElement,
                [{ x, y, type: "scatter", mode: "lines+markers", line: { color: "#0f766e", width: 3 }, marker: { size: 8 } }],
                chartLayout("Son tahminler"),
                plotlyConfig
            );
        }

        if (modelElement) {
            Plotly.newPlot(
                modelElement,
                [{
                    x: veri.modeller.map((item) => item.model),
                    y: veri.modeller.map((item) => item.rmse),
                    type: "bar",
                    marker: { color: "#f97316" },
                }],
                chartLayout("RMSE değerleri"),
                plotlyConfig
            );
        }
    };

    window.akilliEnerjiPerformansHazirla = () => {
        const veri = window.akilliEnerjiPerformansVerisi || [];
        const performanceElement = document.getElementById("performanceChart");
        const r2Element = document.getElementById("r2Chart");

        if (performanceElement) {
            Plotly.newPlot(
                performanceElement,
                [{
                    x: veri.map((item) => item.model),
                    y: veri.map((item) => item.rmse),
                    type: "bar",
                    marker: { color: "#0f766e" },
                }],
                chartLayout("Düşük RMSE daha iyidir"),
                plotlyConfig
            );
        }

        if (r2Element) {
            Plotly.newPlot(
                r2Element,
                [{
                    x: veri.map((item) => item.model),
                    y: veri.map((item) => item.r2),
                    type: "bar",
                    marker: { color: "#2563eb" },
                }],
                chartLayout("Yüksek R2 Score daha iyidir"),
                plotlyConfig
            );
        }
    };
})();

