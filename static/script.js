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

// Handle form submission to show scanning screen
const form = document.getElementById("analyze-form");
const scanningScreen = document.getElementById("scanning-screen");

form.addEventListener("submit", function (event) {
// stop the form from submitting immediately
    event.preventDefault(); 

    // Hide welcome
    const welcome = document.querySelector(".welcome-card");

    if (welcome) {
        welcome.style.display = "none";
    }

    // Show scanning
    scanningScreen.style.display = "flex";

setTimeout(function(){
    form.submit();

},2500);

});