// Parse the raw AI analysis text and create structured sections
const rawElement = document.getElementById("ai-raw")
const container = document.getElementById("ai-analysis");

if (rawElement && container){
    const raw = rawElement.textContent.trim();
    raw.split(/(?=^\s*(?:\d+[.)]\s*)?(?:Strengths|Weaknesses|Missing Skills|Suggestions for Improvement)\s*:?\s*$)/im)
        .forEach(section => {
            if (!section.trim()) return;

        const [heading, ...content] = section.trim().split("\n");
        const title = heading.replace(/^\d+[.)]\s*/, "").replace(/:$/, "").trim();

        const card = document.createElement("div");
        card.className = "ai-section " + title.toLowerCase().replaceAll(" ", "-");

        const h3 = document.createElement("h3");
        h3.textContent = title;

        const p = document.createElement("p");
        p.textContent = content.join("\n").trim();

        card.append(h3, p);
        container.appendChild(card);
    });
}

// Handle form submission
const form = document.getElementById("analyze-form");
const scanningScreen = document.getElementById("scanning-screen");

if (form) {
    form.addEventListener("submit", async function (event) {
        event.preventDefault();

        // Hide welcome screen
        const welcome = document.querySelector(".welcome-card");

        if (welcome) {
            welcome.style.display = "none";
        }

        // Show scanning screen
        if (scanningScreen) {
            scanningScreen.style.display = "flex";
        }

        try {
            // Keep the uploaded PDF in FormData
            const formData = new FormData(form);

            // Send the form using fetch
            const response = await fetch(form.action || window.location.href, {
                method: "POST",
                body: formData,
                credentials: "same-origin"
            });

            // Get the result page
            const html = await response.text();

            // Replace current page with the result
            document.open();
            document.write(html);
            document.close();

        } catch (error) {
            console.error("Upload error:", error);

            if (scanningScreen) {
                scanningScreen.style.display = "none";
            }

            alert("Something went wrong while uploading the resume. Please try again.");
        }
    });
}