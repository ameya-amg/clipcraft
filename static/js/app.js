// ClipCraft AI - Frontend Logic

  // Backend API URL management
  function getApiBaseUrl() {
    if (window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1") {
      return localStorage.getItem("clipcraft_api_url") || "";
    }
    return localStorage.getItem("clipcraft_api_url") || "http://localhost:8000";
  }

  function apiUrl(path) {
    const base = getApiBaseUrl().replace(/\/+$/, "");
    return base ? `${base}${path}` : path;
  }

  // Server Config Modal Elements
  const serverConfigBtn = document.getElementById("serverConfigBtn");
  const serverModal = document.getElementById("serverModal");
  const closeModalBtn = document.getElementById("closeModalBtn");
  const backendUrlInput = document.getElementById("backendUrlInput");
  const testConnectionBtn = document.getElementById("testConnectionBtn");
  const saveBackendUrlBtn = document.getElementById("saveBackendUrlBtn");
  const connectionStatusMsg = document.getElementById("connectionStatusMsg");
  const serverStatusDot = document.getElementById("serverStatusDot");
  const serverStatusText = document.getElementById("serverStatusText");

  async function checkServerConnection() {
    try {
      const res = await fetch(apiUrl("/api/presets"), { method: "GET" });
      if (res.ok) {
        if (serverStatusDot) serverStatusDot.style.color = "#22c55e";
        if (serverStatusText) serverStatusText.textContent = "AI Engine: Connected";
        return true;
      }
    } catch (e) {
      // offline
    }
    if (serverStatusDot) serverStatusDot.style.color = "#f59e0b";
    if (serverStatusText) serverStatusText.textContent = "AI Engine: Connect";
    return false;
  }

  if (serverConfigBtn && serverModal) {
    serverConfigBtn.addEventListener("click", () => {
      backendUrlInput.value = localStorage.getItem("clipcraft_api_url") || (window.location.hostname === "localhost" ? "" : "http://localhost:8000");
      connectionStatusMsg.style.display = "none";
      serverModal.classList.remove("hidden");
    });

    closeModalBtn.addEventListener("click", () => {
      serverModal.classList.add("hidden");
    });

    serverModal.addEventListener("click", (e) => {
      if (e.target === serverModal) serverModal.classList.add("hidden");
    });

    testConnectionBtn.addEventListener("click", async () => {
      const url = backendUrlInput.value.trim().replace(/\/+$/, "");
      testConnectionBtn.disabled = true;
      testConnectionBtn.textContent = "Testing...";
      try {
        const testEndpoint = url ? `${url}/api/presets` : "/api/presets";
        const res = await fetch(testEndpoint);
        if (res.ok) {
          connectionStatusMsg.style.display = "block";
          connectionStatusMsg.style.color = "#22c55e";
          connectionStatusMsg.textContent = "✓ Connected successfully to ClipCraft AI engine!";
        } else {
          throw new Error("HTTP " + res.status);
        }
      } catch (err) {
        connectionStatusMsg.style.display = "block";
        connectionStatusMsg.style.color = "#ef4444";
        connectionStatusMsg.textContent = "✗ Could not reach backend: " + err.message;
      } finally {
        testConnectionBtn.disabled = false;
        testConnectionBtn.textContent = "Test Connection";
      }
    });

    saveBackendUrlBtn.addEventListener("click", () => {
      const url = backendUrlInput.value.trim().replace(/\/+$/, "");
      if (url) {
        localStorage.setItem("clipcraft_api_url", url);
      } else {
        localStorage.removeItem("clipcraft_api_url");
      }
      serverModal.classList.add("hidden");
      checkServerConnection();
    });
  }

  // Initial connection check
  checkServerConnection();

  // Elements
  const youtubeUrlInput = document.getElementById("youtubeUrl");
  const fetchBtn = document.getElementById("fetchBtn");
  const videoInfoCard = document.getElementById("videoInfoCard");
  const videoThumb = document.getElementById("videoThumb");
  const videoTitle = document.getElementById("videoTitle");
  const videoChannel = document.getElementById("videoChannel");
  const videoDuration = document.getElementById("videoDuration");
  const startTimeInput = document.getElementById("startTime");
  const endTimeInput = document.getElementById("endTime");
  const clipDurationDisplay = document.getElementById("clipDurationDisplay");

  // Styling inputs
  const presetButtons = document.querySelectorAll(".preset-btn");
  const fontFamilySelect = document.getElementById("fontFamily");
  const fontSizeInput = document.getElementById("fontSize");
  const fontSizeNum = document.getElementById("fontSizeNum");
  const fontSizeVal = document.getElementById("fontSizeVal");
  const sizeChips = document.querySelectorAll(".btn-size-chip");
  const primaryColorInput = document.getElementById("primaryColor");
  const primaryColorHex = document.getElementById("primaryColorHex");
  const highlightColorInput = document.getElementById("highlightColor");
  const highlightColorHex = document.getElementById("highlightColorHex");
  const outlineColorInput = document.getElementById("outlineColor");
  const outlineColorHex = document.getElementById("outlineColorHex");
  const outlineWidthInput = document.getElementById("outlineWidth");
  const outlineWidthVal = document.getElementById("outlineWidthVal");
  const positionYInput = document.getElementById("positionY");
  const positionYVal = document.getElementById("positionYVal");
  const wordsPerLineSelect = document.getElementById("wordsPerLine");
  const allCapsCheckbox = document.getElementById("allCaps");
  const languageSelect = document.getElementById("languageSelect");
  const punchZoomCheckbox = document.getElementById("punchZoom");
  const enableSfxCheckbox = document.getElementById("enableSfx");

  // Preview elements
  const liveSubContainer = document.getElementById("liveSubContainer");
  const liveSubtitleBox = document.getElementById("liveSubtitleBox");
  const toggleAnimBtn = document.getElementById("toggleAnimBtn");

  // Generation & Progress
  const generateBtn = document.getElementById("generateBtn");
  const progressCard = document.getElementById("progressCard");
  const progressTitle = document.getElementById("progressTitle");
  const progressPercent = document.getElementById("progressPercent");
  const progressBar = document.getElementById("progressBar");
  const progressMessage = document.getElementById("progressMessage");
  const resultCard = document.getElementById("resultCard");
  const outputVideoPlayer = document.getElementById("outputVideoPlayer");
  const downloadBtn = document.getElementById("downloadBtn");
  const createAnotherBtn = document.getElementById("createAnotherBtn");

  // Preset definitions
  const PRESET_CONFIGS = {
    hormozi: {
      font: "Montserrat",
      size: 60,
      primary: "#FFFFFF",
      highlight: "#FFEA00",
      outline: "#000000",
      outlineWidth: 6,
      allCaps: true,
      position: 62,
      words: 3
    },
    beast: {
      font: "Anton",
      size: 64,
      primary: "#FFFFFF",
      highlight: "#39FF14",
      outline: "#000000",
      outlineWidth: 7,
      allCaps: true,
      position: 60,
      words: 2
    },
    vice_neon: {
      font: "Impact",
      size: 62,
      primary: "#00FFFF",
      highlight: "#FF1493",
      outline: "#0D0B18",
      outlineWidth: 6,
      allCaps: true,
      position: 63,
      words: 3
    },
    fire_gold: {
      font: "Arial Black",
      size: 58,
      primary: "#FFFFFF",
      highlight: "#FF7700",
      outline: "#000000",
      outlineWidth: 6,
      allCaps: true,
      position: 62,
      words: 3
    },
    minimal_clean: {
      font: "Helvetica",
      size: 50,
      primary: "#F0F0F0",
      highlight: "#FFFFFF",
      outline: "#1A1A1A",
      outlineWidth: 4,
      allCaps: false,
      position: 65,
      words: 4
    }
  };

  // Helper: Format seconds to MM:SS
  function formatTime(seconds) {
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs < 10 ? "0" : ""}${secs}`;
  }

  // Update duration display
  function updateClipDuration() {
    const start = parseFloat(startTimeInput.value) || 0;
    const end = parseFloat(endTimeInput.value) || 0;
    const diff = Math.max(0, end - start);
    clipDurationDisplay.textContent = `${diff}s`;
  }

  startTimeInput.addEventListener("input", updateClipDuration);
  endTimeInput.addEventListener("input", updateClipDuration);

  // Fetch YouTube Info
  fetchBtn.addEventListener("click", async () => {
    const url = youtubeUrlInput.value.trim();
    if (!url) {
      alert("Please enter a valid YouTube URL.");
      return;
    }

    fetchBtn.disabled = true;
    fetchBtn.innerHTML = "<span>Fetching...</span>";

    try {
      const res = await fetch(apiUrl("/api/video-info"), {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url })
      });
      const data = await res.json();

      if (data.success && data.info) {
        const info = data.info;
        videoThumb.src = info.thumbnail;
        videoTitle.textContent = info.title;
        videoChannel.textContent = info.channel;
        videoDuration.textContent = formatTime(info.duration);
        
        startTimeInput.value = 0;
        endTimeInput.value = Math.min(30, info.duration || 30);
        endTimeInput.max = info.duration || 300;
        updateClipDuration();

        videoInfoCard.classList.remove("hidden");
      } else {
        alert(data.error || "Failed to load video info.");
      }
    } catch (err) {
      alert("Error contacting server: " + err.message);
    } finally {
      fetchBtn.disabled = false;
      fetchBtn.innerHTML = "<span>Load Video</span>";
    }
  });

  // Apply Preset
  presetButtons.forEach(btn => {
    btn.addEventListener("click", () => {
      presetButtons.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");

      const key = btn.dataset.preset;
      const conf = PRESET_CONFIGS[key];
      if (conf) {
        fontFamilySelect.value = conf.font;
        fontSizeInput.value = conf.size;
        if (fontSizeNum) fontSizeNum.value = conf.size;
        fontSizeVal.textContent = conf.size;
        syncSizeChips(conf.size);
        primaryColorInput.value = conf.primary;
        primaryColorHex.textContent = conf.primary;
        highlightColorInput.value = conf.highlight;
        highlightColorHex.textContent = conf.highlight;
        outlineColorInput.value = conf.outline;
        outlineColorHex.textContent = conf.outline;
        outlineWidthInput.value = conf.outlineWidth;
        outlineWidthVal.textContent = conf.outlineWidth;
        positionYInput.value = conf.position;
        positionYVal.textContent = conf.position;
        allCapsCheckbox.checked = conf.allCaps;
        wordsPerLineSelect.value = conf.words;
        updateLivePreview();
      }
    });
  });

  // Size Sync and Quick Chips
  function syncSizeChips(currentVal) {
    if (!sizeChips) return;
    sizeChips.forEach(c => {
      if (parseInt(c.dataset.size, 10) === parseInt(currentVal, 10)) {
        c.classList.add("active");
      } else {
        c.classList.remove("active");
      }
    });
  }

  if (fontSizeInput && fontSizeNum) {
    fontSizeInput.addEventListener("input", (e) => {
      fontSizeNum.value = e.target.value;
      syncSizeChips(e.target.value);
      updateLivePreview();
    });

    fontSizeNum.addEventListener("input", (e) => {
      fontSizeInput.value = e.target.value;
      syncSizeChips(e.target.value);
      updateLivePreview();
    });
  }

  if (sizeChips) {
    sizeChips.forEach(chip => {
      chip.addEventListener("click", () => {
        const sz = chip.dataset.size;
        fontSizeInput.value = sz;
        if (fontSizeNum) fontSizeNum.value = sz;
        syncSizeChips(sz);
        updateLivePreview();
      });
    });
  }

  // Live preview styling updates
  function updateLivePreview() {
    const font = fontFamilySelect.value;
    const size = fontSizeInput.value;
    const primary = primaryColorInput.value;
    const highlight = highlightColorInput.value;
    const outline = outlineColorInput.value;
    const strokeWidth = outlineWidthInput.value;
    const positionY = positionYInput.value;
    const isAllCaps = allCapsCheckbox.checked;

    // Display values
    fontSizeVal.textContent = size;
    primaryColorHex.textContent = primary.toUpperCase();
    highlightColorHex.textContent = highlight.toUpperCase();
    outlineColorHex.textContent = outline.toUpperCase();
    outlineWidthVal.textContent = strokeWidth;
    positionYVal.textContent = positionY;

    // Position container
    liveSubContainer.style.top = `${positionY}%`;

    // Font styling
    liveSubtitleBox.style.fontFamily = `"${font}", sans-serif`;
    liveSubtitleBox.style.fontSize = `${Math.round(size * 0.45)}px`; // Scaled for phone mockup
    liveSubtitleBox.style.textTransform = isAllCaps ? "uppercase" : "none";

    // Text stroke / shadow
    const strokeCss = `${strokeWidth * 0.4}px ${outline}`;

    const words = liveSubtitleBox.querySelectorAll(".sub-word");
    words.forEach(w => {
      if (w.classList.contains("highlighted")) {
        w.style.color = highlight;
      } else {
        w.style.color = primary;
      }
      w.style.webkitTextStroke = strokeCss;
      w.style.textShadow = `0px 2px 4px rgba(0,0,0,0.8)`;
    });
  }

  // Bind input listeners
  [
    fontFamilySelect, fontSizeInput, primaryColorInput, highlightColorInput,
    outlineColorInput, outlineWidthInput, positionYInput, allCapsCheckbox, wordsPerLineSelect
  ].forEach(el => {
    el.addEventListener("input", updateLivePreview);
    el.addEventListener("change", updateLivePreview);
  });

  // Layout radio buttons styling & preview adaptation
  document.querySelectorAll('input[name="layoutMode"]').forEach(radio => {
    radio.addEventListener("change", (e) => {
      document.querySelectorAll(".layout-option").forEach(lo => lo.classList.remove("active"));
      e.target.closest(".layout-option").classList.add("active");

      const mode = e.target.value;
      const previewScreen = document.getElementById("previewScreen");
      const simulatedBg = document.getElementById("simulatedBg");

      if (mode === "center_crop") {
        if (simulatedBg) simulatedBg.style.transform = "scale(1.35)";
        // If font size was small, bump it to 85px for full screen center crop
        if (parseInt(fontSizeInput.value, 10) < 70) {
          fontSizeInput.value = 85;
          if (fontSizeNum) fontSizeNum.value = 85;
          syncSizeChips(85);
        }
      } else {
        if (simulatedBg) simulatedBg.style.transform = "scale(1.0)";
      }
      updateLivePreview();
    });
  });

  // Word Animation Test
  let animTimer = null;
  let activeWordIndex = 0;
  const sampleWords = ["BHAI", "YEH", "KABHI", "DEKHA", "HAI?!"];

  function startAnimation() {
    if (animTimer) {
      clearInterval(animTimer);
      animTimer = null;
      toggleAnimBtn.textContent = "▶ Test Word Highlight Animation";
      updateLivePreview();
      return;
    }

    toggleAnimBtn.textContent = "⏹ Stop Animation";
    animTimer = setInterval(() => {
      activeWordIndex = (activeWordIndex + 1) % sampleWords.length;
      const spans = liveSubtitleBox.querySelectorAll(".sub-word");
      spans.forEach((span, idx) => {
        if (idx === activeWordIndex) {
          span.classList.add("highlighted");
        } else {
          span.classList.remove("highlighted");
        }
      });
      updateLivePreview();
    }, 400);
  }

  toggleAnimBtn.addEventListener("click", startAnimation);

  // Generate 9:16 Short
  generateBtn.addEventListener("click", async () => {
    const url = youtubeUrlInput.value.trim();
    if (!url) {
      alert("Please provide a YouTube video URL first.");
      youtubeUrlInput.focus();
      return;
    }

    const start = parseFloat(startTimeInput.value) || 0;
    const end = parseFloat(endTimeInput.value) || 30;
    if (end <= start) {
      alert("End time must be greater than start time.");
      return;
    }

    const layout = document.querySelector('input[name="layoutMode"]:checked').value;
    const activePresetBtn = document.querySelector(".preset-btn.active");
    const preset = activePresetBtn ? activePresetBtn.dataset.preset : null;

    const payload = {
      url: url,
      start_time: start,
      end_time: end,
      layout_mode: layout,
      preset: preset,
      font_family: fontFamilySelect.value,
      font_size: parseInt(fontSizeInput.value, 10),
      primary_color: primaryColorInput.value,
      highlight_color: highlightColorInput.value,
      outline_color: outlineColorInput.value,
      outline_width: parseInt(outlineWidthInput.value, 10),
      all_caps: allCapsCheckbox.checked,
      position_y: parseInt(positionYInput.value, 10),
      max_words_per_segment: parseInt(wordsPerLineSelect.value, 10),
      language: languageSelect ? languageSelect.value : "hinglish",
      punch_zoom: punchZoomCheckbox ? punchZoomCheckbox.checked : true,
      enable_sfx: enableSfxCheckbox ? enableSfxCheckbox.checked : true,
      model_size: "small"
    };

    // UI state
    generateBtn.disabled = true;
    generateBtn.innerHTML = "<span>Generating Clip...</span>";
    resultCard.classList.add("hidden");
    progressCard.classList.remove("hidden");
    progressBar.style.width = "5%";
    progressPercent.textContent = "5%";
    progressMessage.textContent = "Submitting clip request...";

    // Reset step badges
    ["step-dl", "step-ai", "step-sub", "step-render"].forEach(id => {
      const el = document.getElementById(id);
      el.className = "mini-step";
    });

    try {
      const res = await fetch(apiUrl("/api/create-clip"), {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });
      const data = await res.json();

      if (!data.success) {
        throw new Error(data.error || "Failed to start processing.");
      }

      const jobId = data.job_id;
      pollJobStatus(jobId);
    } catch (err) {
      alert("Error: " + err.message);
      generateBtn.disabled = false;
      generateBtn.innerHTML = '<span class="btn-icon">⚡</span><span>Generate 9:16 Short with Captions</span>';
      progressCard.classList.add("hidden");
    }
  });

  // Polling Job Status
  async function pollJobStatus(jobId) {
    const pollInterval = setInterval(async () => {
      try {
        const res = await fetch(apiUrl(`/api/job-status/${jobId}`));
        if (!res.ok) return;

        const data = await res.json();
        progressBar.style.width = `${data.progress}%`;
        progressPercent.textContent = `${data.progress}%`;
        progressMessage.textContent = data.message || "Working...";

        // Update step badges
        if (data.status === "downloading") {
          document.getElementById("step-dl").className = "mini-step active";
        } else if (data.status === "transcribing") {
          document.getElementById("step-dl").className = "mini-step done";
          document.getElementById("step-ai").className = "mini-step active";
        } else if (data.status === "generating_subtitles") {
          document.getElementById("step-dl").className = "mini-step done";
          document.getElementById("step-ai").className = "mini-step done";
          document.getElementById("step-sub").className = "mini-step active";
        } else if (data.status === "rendering") {
          document.getElementById("step-dl").className = "mini-step done";
          document.getElementById("step-ai").className = "mini-step done";
          document.getElementById("step-sub").className = "mini-step done";
          document.getElementById("step-render").className = "mini-step active";
        } else if (data.status === "completed") {
          clearInterval(pollInterval);
          ["step-dl", "step-ai", "step-sub", "step-render"].forEach(id => {
            document.getElementById(id).className = "mini-step done";
          });

          // Show Result
          progressCard.classList.add("hidden");
          resultCard.classList.remove("hidden");
          const finalVideoUrl = apiUrl(data.output_url);
          outputVideoPlayer.src = finalVideoUrl;
          downloadBtn.href = finalVideoUrl;
          outputVideoPlayer.play().catch(() => {});

          generateBtn.disabled = false;
          generateBtn.innerHTML = '<span class="btn-icon">⚡</span><span>Generate 9:16 Short with Captions</span>';
        } else if (data.status === "failed") {
          clearInterval(pollInterval);
          progressMessage.textContent = data.message || "Failed.";
          alert("Generation failed: " + data.message);
          generateBtn.disabled = false;
          generateBtn.innerHTML = '<span class="btn-icon">⚡</span><span>Generate 9:16 Short with Captions</span>';
        }
      } catch (err) {
        console.error("Poll error:", err);
      }
    }, 1500);
  }

  // Create another clip
  createAnotherBtn.addEventListener("click", () => {
    resultCard.classList.add("hidden");
    window.scrollTo({ top: 0, behavior: "smooth" });
  });

  // Initial render of preview
  updateLivePreview();
});
