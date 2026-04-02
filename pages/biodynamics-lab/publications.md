---
title: Publications
description: circuits that oscillate and populations that cooperate
navigation: biodynamics-navigation
permalink: /biodynamics/publications/
background: /assets/images/microfluidics-scaled.jpg
---

# Publications

<div id="publications-container"></div>

<div id="pagination" style="margin-top: 2rem;"></div>

<!-- Modal -->
<div id="pdf-modal" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.6); z-index:1000;">
  <div style="background:white; max-width:400px; margin:10% auto; padding:1.5rem; border-radius:8px; position:relative;">
    <h3 style="margin-top:0;">Request PDF</h3>
    
    <input id="user-name" type="text" placeholder="Your Name" style="width:100%; margin-bottom:0.5rem;" />
    <input id="user-email" type="email" placeholder="Your Email" style="width:100%; margin-bottom:1rem;" />

    <div style="display:flex; justify-content:space-between;">
      <button onclick="submitPDFRequest()">Request</button>
      <button onclick="closeModal()">Cancel</button>
    </div>

    <div id="modal-status" style="margin-top:0.8rem; font-size:0.9rem;"></div>
  </div>
</div>

<script>
const publicationsData = {{ site.data.biodynamics-lab.publications | jsonify }};
const perPage = 20;

let currentPubID = null;

function getQueryParam(param) {
  const urlParams = new URLSearchParams(window.location.search);
  return urlParams.get(param);
}

function updateURL(page) {
  const params = new URLSearchParams();
  if (page > 1) params.set("page", page);
  const newUrl = window.location.pathname + (params.toString() ? "?" + params.toString() : "");
  window.history.pushState({}, "", newUrl);
}

function openModal(pubID) {
  currentPubID = pubID;
  document.getElementById("pdf-modal").style.display = "block";
  document.getElementById("modal-status").textContent = "";
}

function closeModal() {
  document.getElementById("pdf-modal").style.display = "none";
}

async function submitPDFRequest() {
  const name = document.getElementById("user-name").value;
  const email = document.getElementById("user-email").value;
  const status = document.getElementById("modal-status");

  if (!name || !email) {
    status.textContent = "Please fill out both fields.";
    return;
  }

  status.textContent = "Requesting...";

  try {
    const response = await fetch("https://coop.tail17b308.ts.net/request-pdf", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        name: name,
        email: email,
        paper_id: currentPubID
      })
    });

    if (response.ok) {
      status.textContent = "Request sent. Check your email.";
    } else {
      status.textContent = "Request failed.";
    }
  } catch (err) {
    status.textContent = "Network error.";
  }
}

function render() {
  const container = document.getElementById("publications-container");
  const pagination = document.getElementById("pagination");

  const currentPage = parseInt(getQueryParam("page")) || 1;

  let publications = [...publicationsData];

  publications.sort((a, b) => {
    const dateA = new Date(a.publication_date || a.year);
    const dateB = new Date(b.publication_date || b.year);
    return dateB - dateA;
  });

  const totalPages = Math.ceil(publications.length / perPage);
  const safePage = Math.min(Math.max(currentPage, 1), totalPages || 1);
  const start = (safePage - 1) * perPage;
  const pageItems = publications.slice(start, start + perPage);

  container.innerHTML = "";

  if (pageItems.length === 0) {
    container.innerHTML = "<p>No publications found.</p>";
  } else {
    let currentYear = null;

    pageItems.forEach(pub => {
      const pubYear = pub.year || new Date(pub.publication_date).getFullYear();

      if (pubYear !== currentYear) {
        currentYear = pubYear;
        const yearHeader = document.createElement("h2");
        yearHeader.style.marginTop = "2rem";
        yearHeader.textContent = currentYear;
        container.appendChild(yearHeader);
      }

      const div = document.createElement("div");
      div.style.marginBottom = "1.8rem";

      const buttonHTML = pub.pubID
        ? `<button style="margin-top:0.4rem;" onclick="openModal('${pub.pubID}')">Request PDF</button>`
        : "";

      div.innerHTML = `
        <div style="margin-bottom:0.2rem;">
          <strong>
            <a href="${pub.link}" target="_blank" rel="noopener">
              ${pub.title}
            </a>
          </strong>
        </div>
        <div>${pub.authors.join(", ")}</div>
        <div><em>${pub.journal || ""}</em></div>
        <div style="font-size:0.9rem; opacity:0.7;">
          ${pub.publication_date ? new Date(pub.publication_date).toLocaleDateString() : ""}
        </div>
        ${buttonHTML}
      `;

      container.appendChild(div);
    });
  }

  pagination.innerHTML = "";

  if (totalPages > 1) {
    if (safePage > 1) {
      const prev = document.createElement("a");
      prev.href = "#";
      prev.textContent = "← Newer";
      prev.onclick = function(e) {
        e.preventDefault();
        updateURL(safePage - 1);
        render();
      };
      pagination.appendChild(prev);
    }

    if (safePage < totalPages) {
      if (safePage > 1) {
        const sep = document.createTextNode(" | ");
        pagination.appendChild(sep);
      }

      const next = document.createElement("a");
      next.href = "#";
      next.textContent = "Older →";
      next.onclick = function(e) {
        e.preventDefault();
        updateURL(safePage + 1);
        render();
      };
      pagination.appendChild(next);
    }
  }
}

render();
</script>