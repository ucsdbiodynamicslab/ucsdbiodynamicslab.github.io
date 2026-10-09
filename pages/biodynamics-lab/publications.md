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

<script>
const publicationsData = {{ site.data.biodynamics-lab.publications | jsonify }};
const perPage = 20;

// PDFs live in /assets/pdfs/biodynamics/, named <pubID>.pdf
const pdfPaths = new Set([
{%- for file in site.static_files -%}
  {%- if file.path contains "/assets/pdfs/biodynamics/" and file.extname == ".pdf" -%}
    {{ file.path | relative_url | jsonify }},
  {%- endif -%}
{%- endfor -%}
]);

function pdfURL(pub) {
  if (!pub.pubID) return null;
  const path = "{{ '/assets/pdfs/biodynamics/' | relative_url }}" + pub.pubID + ".pdf";
  return pdfPaths.has(path) ? path : null;
}

// "YYYY-MM-DD" as a local date (new Date("YYYY-MM-DD") is UTC midnight, which shows as
// the previous day in US time zones)
function parseLocalDate(str) {
  const [y, m, d] = String(str).split("-").map(Number);
  return new Date(y, (m || 1) - 1, d || 1);
}

// Date used for sorting and year headers: publication date, else Jan 1 of the year, else null
function pubDate(pub) {
  if (pub.publication_date) return parseLocalDate(pub.publication_date);
  if (pub.year) return new Date(pub.year, 0, 1);
  return null;
}

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

function render() {
  const container = document.getElementById("publications-container");
  const pagination = document.getElementById("pagination");

  const currentPage = parseInt(getQueryParam("page")) || 1;

  let publications = [...publicationsData];

  // Newest first; publications with no date or year go last
  publications.sort((a, b) => {
    const dateA = pubDate(a);
    const dateB = pubDate(b);
    if (!dateA || !dateB) return (dateA ? -1 : 0) + (dateB ? 1 : 0);
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
      const date = pubDate(pub);
      const pubYear = date ? date.getFullYear() : "Other";

      if (pubYear !== currentYear) {
        currentYear = pubYear;
        const yearHeader = document.createElement("h2");
        yearHeader.style.marginTop = "2rem";
        yearHeader.textContent = currentYear;
        container.appendChild(yearHeader);
      }

      const div = document.createElement("div");
      div.style.marginBottom = "1.8rem";

      const pdf = pdfURL(pub);
      const titleHTML = pdf
        ? `<a href="${pdf}" target="_blank" rel="noopener">${pub.title}</a>`
        : pub.title;

      const buttonHTML = pub.link
        ? `<a class="btn btn-sm btn-outline-dark mt-2" href="${pub.link}" target="_blank" rel="noopener">Journal Version</a>`
        : "";

      div.innerHTML = `
        <div style="margin-bottom:0.2rem;">
          <strong>${titleHTML}</strong>
        </div>
        <div>${pub.authors.join(", ")}</div>
        <div><em>${pub.journal || ""}</em></div>
        <div style="font-size:0.9rem; opacity:0.7;">
          ${pub.publication_date ? parseLocalDate(pub.publication_date).toLocaleDateString() : ""}
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