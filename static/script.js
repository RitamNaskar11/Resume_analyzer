document.addEventListener("DOMContentLoaded", () => {
  const modal = document.getElementById("upload-modal");
  const closeButton = document.getElementById("modal-close");
  const openButtons = document.querySelectorAll("[data-open-modal]");
  const form = document.getElementById("analyze-form");
  const fileInput = document.getElementById("resume-file");
  const fileLabel = document.getElementById("file-label");
  const fileHint = document.getElementById("file-hint");
  const dropZone = document.getElementById("drop-zone");
  const errorBox = document.getElementById("form-error");
  const submitButton = document.getElementById("submit-button");
  const scanning = document.getElementById("scanning-screen");
  const menuToggle = document.getElementById("menu-toggle");
  const sidebar = document.getElementById("sidebar");

  // Open and close upload modal
  const openModal = () => {
    modal?.classList.remove("is-hidden");
    modal?.setAttribute("aria-hidden", "false");
    document.body.classList.add("modal-open");
  };

  const closeModal = () => {
    modal?.classList.add("is-hidden");
    modal?.setAttribute("aria-hidden", "true");
    document.body.classList.remove("modal-open");
  };

  openButtons.forEach(button => {
    button.addEventListener("click", openModal);
  });

  closeButton?.addEventListener("click", closeModal);

  modal?.addEventListener("click", event => {
    if (event.target === modal) {
      closeModal();
    }
  });

  document.addEventListener("keydown", event => {
    if (
      event.key === "Escape" &&
      modal &&
      !modal.classList.contains("is-hidden")
    ) {
      closeModal();
    }
  });

  // Mobile sidebar
  menuToggle?.addEventListener("click", () => {
    sidebar?.classList.toggle("open");
  });

  document.addEventListener("click", event => {
    if (
      window.innerWidth <= 760 &&
      sidebar?.classList.contains("open") &&
      !sidebar.contains(event.target) &&
      !menuToggle?.contains(event.target)
    ) {
      sidebar.classList.remove("open");
    }
  });

  // Show selected PDF filename
  const showFileName = file => {
    if (!file) return;

    fileLabel.textContent = file.name;
    fileHint.textContent = "Your resume is selected and ready.";

    dropZone?.classList.add("dragover");
  };

  // Validate uploaded PDF
  fileInput?.addEventListener("change", () => {
    errorBox.textContent = "";

    const file = fileInput.files?.[0];

    if (!file) return;

    if (!file.name.toLowerCase().endsWith(".pdf")) {
      fileInput.value = "";
      fileLabel.textContent = "Choose a PDF resume";
      fileHint.textContent = "Only PDF files are supported.";
      errorBox.textContent = "Please select a PDF file.";
      return;
    }

    if (file.size > 5 * 1024 * 1024) {
      fileInput.value = "";
      fileLabel.textContent = "Choose a PDF resume";
      fileHint.textContent = "Maximum file size is 5 MB.";
      errorBox.textContent =
        "Your file is larger than 5 MB. Please choose a smaller PDF.";
      return;
    }

    showFileName(file);
  });

  // Drag and drop functionality
  ["dragenter", "dragover"].forEach(type => {
    dropZone?.addEventListener(type, event => {
      event.preventDefault();
      dropZone.classList.add("dragover");
    });
  });

  ["dragleave", "drop"].forEach(type => {
    dropZone?.addEventListener(type, event => {
      event.preventDefault();

      if (type === "dragleave") {
        dropZone.classList.remove("dragover");
      }
    });
  });

  dropZone?.addEventListener("drop", event => {
    const file = event.dataTransfer?.files?.[0];

    if (!file) return;

    const transfer = new DataTransfer();
    transfer.items.add(file);

    fileInput.files = transfer.files;

    fileInput.dispatchEvent(
      new Event("change", { bubbles: true })
    );
  });

  // Form submission
  form?.addEventListener("submit", event => {
    errorBox.textContent = "";

    const file = fileInput?.files?.[0];

    const jobDescription = document
      .getElementById("job-description")
      ?.value.trim();

    if (!file) {
      event.preventDefault();
      errorBox.textContent = "Please choose your PDF resume first.";
      return;
    }

    if (
      !file.name.toLowerCase().endsWith(".pdf") ||
      file.size > 5 * 1024 * 1024
    ) {
      event.preventDefault();
      errorBox.textContent = "Choose a PDF file up to 5 MB.";
      return;
    }

    if (!jobDescription) {
      event.preventDefault();
      errorBox.textContent = "Please paste the job description.";
      return;
    }

    // Show scanning screen and allow normal Flask form submission
    submitButton.disabled = true;
    submitButton.innerHTML = "Analyzing…";
    submitButton.style.opacity = ".7";

    scanning?.classList.add("visible");
  });

  // Parse existing AI analysis into feedback cards
  const rawElement = document.getElementById("ai-raw");
  const aiContainer = document.getElementById("ai-analysis");

  if (rawElement && aiContainer) {
    const raw = rawElement.textContent.trim();

    const headingPattern =
      /^\s*(?:\d+[.)]\s*)?(Strengths|Weaknesses|Missing Skills|Suggestions for Improvement)\s*:?\s*$/im;

    const sections = raw.split(
      /(?=^\s*(?:\d+[.)]\s*)?(?:Strengths|Weaknesses|Missing Skills|Suggestions for Improvement)\s*:?\s*$)/im
    );

    sections.forEach(section => {
      const clean = section.trim();

      if (!clean) return;

      const lines = clean.split("\n");

      const heading = lines
        .shift()
        .replace(/^\d+[.)]\s*/, "")
        .replace(/:$/, "")
        .trim();

      if (!headingPattern.test(heading + ":")) return;

      const card = document.createElement("article");

      card.className =
        "ai-section " +
        heading.toLowerCase().replaceAll(" ", "-");

      const title = document.createElement("h3");
      title.textContent = heading;

      const body = document.createElement("p");

      body.textContent =
        lines.join("\n").trim() || clean;

      card.append(title, body);

      aiContainer.appendChild(card);
    });

    // Fallback if AI response has no recognized headings
    if (!aiContainer.querySelector(".ai-section") && raw) {
      const fallback = document.createElement("article");

      fallback.className = "ai-section";

      const title = document.createElement("h3");
      title.textContent = "Analysis feedback";

      const body = document.createElement("p");
      body.textContent = raw;

      fallback.append(title, body);

      aiContainer.appendChild(fallback);
    }
  }
});