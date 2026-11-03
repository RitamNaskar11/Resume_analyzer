
let currentStep = 1;

const steps = document.querySelectorAll(".wizard-step");
const progressSteps = document.querySelectorAll(".progress-step");
const progressLines = document.querySelectorAll(".progress-line");

function showStep(step) {
    currentStep = step;

    steps.forEach((item) => {
        item.classList.toggle(
            "active",
            Number(item.dataset.page) === step
        );
    });

    progressSteps.forEach((item) => {
        const number = Number(item.dataset.step);
        item.classList.toggle("active", number === step);
        item.classList.toggle("completed", number < step);
    });

    progressLines.forEach((line, index) => {
        line.style.background = index < step - 1 ? "#813ff0" : "#e8e2f2";
    });

    window.scrollTo({ top: 0, behavior: "smooth" });
}

document.querySelectorAll(".next-btn").forEach((button) => {
    button.addEventListener("click", () => {
        if (currentStep === 1) {
            const file = document.getElementById("resume").files[0];

            if (!file) {
                alert("Please upload your PDF resume.");
                return;
            }

            if (!file.name.toLowerCase().endsWith(".pdf")) {
                alert("Please select a PDF file.");
                return;
            }

            document.getElementById("review-file").textContent = file.name;
        }

        if (currentStep === 2) {
            const job = document.getElementById("job-description").value.trim();

            if (!job) {
                alert("Please enter a job description.");
                return;
            }

            document.getElementById("review-job").textContent = job;
        }

        if (currentStep < 3) showStep(currentStep + 1);
    });
});

document.querySelectorAll(".back-btn").forEach((button) => {
    button.addEventListener("click", () => {
        if (currentStep > 1) showStep(currentStep - 1);
    });
});

document.getElementById("resume").addEventListener("change", function () {
    const file = this.files[0];
    document.getElementById("file-name").textContent =
        file ? "✓ Selected: " + file.name : "";
});

const jobInput = document.getElementById("job-description");

jobInput.addEventListener("input", function () {
    document.getElementById("char-count").textContent = this.value.length;
});

document.querySelectorAll("[data-sample]").forEach((button) => {
    button.addEventListener("click", () => {
        jobInput.value = button.dataset.sample;
        jobInput.dispatchEvent(new Event("input"));
    });
});

document.getElementById("wizard-form").addEventListener("submit", function () {
    document.querySelector(".wizard-progress").style.display = "none";
    document.querySelectorAll(".wizard-step").forEach((step) => {
        step.style.display = "none";
    });
    document.getElementById("wizard-loading").classList.add("show");
});

showStep(1);
