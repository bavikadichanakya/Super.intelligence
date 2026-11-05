// SUPER.INTELLIGENCEEE - Dashboard Controller

document.addEventListener("DOMContentLoaded", () => {
  initTabs();
  startTelemetryPoll();
});

// -------------------------------------------------------------
// 1. Navigation & Tabs
// -------------------------------------------------------------
function initTabs() {
  const links = document.querySelectorAll(".nav-link");
  links.forEach(link => {
    link.addEventListener("click", (e) => {
      e.preventDefault();
      const targetId = link.getAttribute("data-tab");
      switchTab(targetId);
    });
  });
}

function switchTab(tabId) {
  document.querySelectorAll(".nav-link").forEach(l => {
    l.classList.toggle("active", l.getAttribute("data-tab") === tabId);
  });
  document.querySelectorAll(".tab-panel").forEach(p => {
    p.classList.toggle("active", p.id === tabId);
  });
}

// -------------------------------------------------------------
// 2. Task & Telemetry Polling
// -------------------------------------------------------------
let activeTaskId = null;

function startTelemetryPoll() {
  setInterval(async () => {
    try {
      const res = await fetch("/api/telemetry");
      if (!res.ok) return;
      const data = await res.json();
      
      // Update sidebar telemetry
      if (data.resources) {
        const r = data.resources;
        const ramEl = document.getElementById("telemetry-ram");
        const cpuEl = document.getElementById("telemetry-cpu");
        if (ramEl) ramEl.textContent = `${r.ram_process_mb} MB (${r.ram_system_percent}%)`;
        if (cpuEl) cpuEl.textContent = `${r.cpu_percent}%`;
      }

      // Check active tasks
      if (data.active_tasks) {
        const runningTask = Object.values(data.active_tasks).find(t => t.status === "RUNNING");
        const monitor = document.getElementById("task-monitor");
        if (runningTask) {
          activeTaskId = runningTask.task_id;
          if (monitor) monitor.style.display = "block";
          document.getElementById("task-name").textContent = runningTask.name;
          document.getElementById("task-msg").textContent = runningTask.message;
          document.getElementById("task-pct").textContent = `${runningTask.progress}%`;
          document.getElementById("task-fill").style.width = `${runningTask.progress}%`;
        } else if (activeTaskId) {
          // Task just finished
          if (monitor) monitor.style.display = "none";
          activeTaskId = null;
          // Reload page to refresh tables
          setTimeout(() => window.location.reload(), 1000);
        } else {
          if (monitor) monitor.style.display = "none";
        }
      }
    } catch (e) {
      console.warn("Telemetry fetch error:", e);
    }
  }, 2500);
}

// -------------------------------------------------------------
// 3. Research Actions
// -------------------------------------------------------------
async function triggerDiscover() {
  try {
    const res = await fetch("/api/research/discover", { method: "POST" });
    const data = await res.json();
    alert(data.message || "Discovery started!");
  } catch (e) {
    alert("Discovery failed: " + e.message);
  }
}

async function updateArticleStatus(articleId, status, notes = "") {
  try {
    const res = await fetch("/api/research/status", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ article_id: articleId, status, notes })
    });
    const data = await res.json();
    if (data.success) {
      window.location.reload();
    } else {
      alert("Status update blocked: " + (data.error || "Unknown error"));
    }
  } catch (e) {
    alert("Failed to update status: " + e.message);
  }
}

async function generateScript(articleId) {
  try {
    const btn = event.target;
    btn.textContent = "Generating...";
    btn.disabled = true;

    const res = await fetch("/api/scripts/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ article_id: articleId })
    });
    const data = await res.json();
    if (data.success) {
      alert("Script generated successfully! Switching to Scripts tab.");
      window.location.reload();
    } else {
      alert("Script generation failed: " + (data.error || "Unknown error"));
      btn.textContent = "Generate Script";
      btn.disabled = false;
    }
  } catch (e) {
    alert("Script request failed: " + e.message);
  }
}

// -------------------------------------------------------------
// 4. Production & Rendering Actions
// -------------------------------------------------------------
async function renderSingleReel(scriptId) {
  try {
    const res = await fetch("/api/render/single", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ script_id: scriptId })
    });
    const data = await res.json();
    if (res.ok) {
      alert("Render job queued! You can monitor progress at the top of the dashboard.");
      switchTab("tab-production");
    } else {
      alert("Render cannot start: " + (data.error || "Conflict"));
    }
  } catch (e) {
    alert("Render request failed: " + e.message);
  }
}

async function renderBatchReels() {
  if (!confirm("Start sequential batch render for the 5 weekly Reels? Rendering will process 1-by-1 sequentially to strictly respect the 8 GB RAM environment.")) {
    return;
  }
  try {
    const res = await fetch("/api/render/batch", { method: "POST" });
    const data = await res.json();
    if (res.ok) {
      alert(data.message);
      switchTab("tab-production");
    } else {
      alert("Batch render error: " + (data.error || "Unknown error"));
    }
  } catch (e) {
    alert("Batch render failed: " + e.message);
  }
}

// -------------------------------------------------------------
// 5. Publishing & Export Actions
// -------------------------------------------------------------
async function assignWeeklySlots() {
  try {
    const res = await fetch("/api/publishing/assign-weekly", { method: "POST" });
    const data = await res.json();
    if (data.success) {
      alert(`Successfully scheduled ${data.scheduled_count} Reels across Mon-Fri time slots.`);
      window.location.reload();
    }
  } catch (e) {
    alert("Failed to schedule: " + e.message);
  }
}

async function exportPublishPackage(itemId) {
  try {
    const res = await fetch("/api/publishing/export-package", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ item_id: itemId })
    });
    const data = await res.json();
    if (data.success) {
      alert("Publishing package generated at:\n" + data.package.package_dir);
      window.location.reload();
    } else {
      alert("Export failed: " + (data.error || "Unknown"));
    }
  } catch (e) {
    alert("Export request failed: " + e.message);
  }
}

async function markAsPublished(itemId) {
  if (!confirm("Confirm this Reel has been published on Instagram?")) return;
  try {
    const res = await fetch("/api/publishing/status", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ item_id: itemId, status: "PUBLISHED" })
    });
    const data = await res.json();
    if (data.success) {
      window.location.reload();
    }
  } catch (e) {
    alert("Update failed: " + e.message);
  }
}

async function publishToInstagramDirect(itemId, title) {
  if (!confirm("CONFIRM HUMAN EDITORIAL APPROVAL:\n\nPublish Reel #" + itemId + " ('" + title + "') directly to Instagram via official Meta API?\n\nPer editorial policy, publishing strictly requires this explicit human confirmation.")) return;
  try {
    const res = await fetch(`/api/instagram/publish/${itemId}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ explicit_approval: true })
    });
    const data = await res.json();
    if (res.ok && (data.ok || data.success)) {
      alert("Reel successfully published to Instagram!\n\nMedia ID: " + (data.result?.ig_media_id || "OK"));
      window.location.reload();
    } else {
      alert("Publish failed: " + (data.detail || data.error || JSON.stringify(data)));
    }
  } catch (e) {
    alert("Publish request failed: " + e.message);
  }
}

// -------------------------------------------------------------
// 6. Analytics & Reports
// -------------------------------------------------------------
async function generateWeeklyReport() {
  try {
    const res = await fetch("/api/reports/generate", { method: "POST" });
    const data = await res.json();
    if (data.success) {
      alert("Weekly report generated!\nSaved at: " + data.report.report_file);
      window.location.reload();
    }
  } catch (e) {
    alert("Report generation failed: " + e.message);
  }
}

// -------------------------------------------------------------
// 7. Modals
// -------------------------------------------------------------
function openModal(id) {
  const el = document.getElementById(id);
  if (el) el.style.display = "flex";
}

function closeModal(id) {
  const el = document.getElementById(id);
  if (el) el.style.display = "none";
}

// Custom Article Form Submit
async function submitCustomArticle(event) {
  event.preventDefault();
  const title = document.getElementById("art-title").value;
  const url = document.getElementById("art-url").value;
  const publisher = document.getElementById("art-publisher").value;
  const category = document.getElementById("art-category").value;
  const summary = document.getElementById("art-summary").value;

  try {
    const res = await fetch("/api/research/add", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title, url, publisher, category, summary })
    });
    const data = await res.json();
    if (data.success) {
      closeModal("modal-add-article");
      window.location.reload();
    } else {
      alert("Failed: " + data.error);
    }
  } catch (e) {
    alert("Error submitting article: " + e.message);
  }
}

