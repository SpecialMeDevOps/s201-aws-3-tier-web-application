const apiBase = window.API_BASE_URL || "/api";
const form = document.querySelector("#job-form");
const input = document.querySelector("#target-url");
const message = document.querySelector("#message");
const jobs = document.querySelector("#jobs");

function renderJobs(items) {
  if (!items.length) {
    jobs.textContent = "No jobs yet.";
    return;
  }
  jobs.innerHTML = items
    .map(
      (job) =>
        `<article class="job"><strong>#${job.id}</strong> <span>${job.status}</span>` +
        `<div>${job.target_url}</div><small>${new Date(job.created_at).toLocaleString()}</small></article>`,
    )
    .join("");
}

async function loadJobs() {
  jobs.textContent = "Loading...";
  try {
    const response = await fetch(`${apiBase}/jobs`);
    if (!response.ok) throw new Error(`Request failed (${response.status})`);
    renderJobs((await response.json()).items);
  } catch (error) {
    jobs.textContent = error.message;
  }
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  message.textContent = "Submitting...";
  try {
    const response = await fetch(`${apiBase}/jobs`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ target_url: input.value }),
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || `Request failed (${response.status})`);
    message.textContent = `Job #${data.id} queued.`;
    input.value = "";
    await loadJobs();
  } catch (error) {
    message.textContent = error.message;
  }
});

document.querySelector("#refresh").addEventListener("click", loadJobs);
loadJobs();
