---
title: News
description: stories of genes, ciruits, and the people who design them
#background: /assets/images/banner_background_image.jpg
permalink: /news/
background: /assets/images/cropped-Q1190217rgb2.jpg
toc: false
comments: false # See posts
published: true # See posts
---

# News

<div style="margin-bottom: 2rem;">
  <label for="tagSelect"><strong>Filter by topic:</strong></label>
  <select id="tagSelect" style="margin-left: 0.5rem;"></select>
</div>

<div id="news-container"></div>

<div id="pagination" style="margin-top: 2rem;"></div>

<script>
const newsData = {{ site.data.news | jsonify }};
const perPage = 10;

function getQueryParam(param) {
  const urlParams = new URLSearchParams(window.location.search);
  return urlParams.get(param);
}

function updateURL(page, tag) {
  const params = new URLSearchParams();
  if (page > 1) params.set("page", page);
  if (tag) params.set("tag", tag);
  const newUrl = window.location.pathname + (params.toString() ? "?" + params.toString() : "");
  window.history.pushState({}, "", newUrl);
}

function renderDropdown(allNews, activeTag) {
  const select = document.getElementById("tagSelect");
  const tags = new Set();

  allNews.forEach(item => {
    if (item.tags) item.tags.forEach(tag => tags.add(tag));
  });

  select.innerHTML = "";

  const allOption = document.createElement("option");
  allOption.value = "";
  allOption.textContent = "All";
  if (!activeTag) allOption.selected = true;
  select.appendChild(allOption);

  Array.from(tags).sort().forEach(tag => {
    const option = document.createElement("option");
    option.value = tag;
    option.textContent = tag;
    if (tag === activeTag) option.selected = true;
    select.appendChild(option);
  });

  select.onchange = function() {
    updateURL(1, this.value || null);
    render();
  };
}

function render() {
  const container = document.getElementById("news-container");
  const pagination = document.getElementById("pagination");

  const currentPage = parseInt(getQueryParam("page")) || 1;
  const activeTag = getQueryParam("tag");

  let filtered = [...newsData];

  filtered.sort((a, b) => new Date(b.date) - new Date(a.date));

  if (activeTag) {
    filtered = filtered.filter(item =>
      item.tags && item.tags.includes(activeTag)
    );
  }

  const totalPages = Math.ceil(filtered.length / perPage);
  const safePage = Math.min(Math.max(currentPage, 1), totalPages || 1);
  const start = (safePage - 1) * perPage;
  const pageItems = filtered.slice(start, start + perPage);

  container.innerHTML = "";

  if (pageItems.length === 0) {
    container.innerHTML = "<p>No news items found.</p>";
  } else {
    pageItems.forEach(item => {
      const div = document.createElement("div");
      div.style.marginBottom = "2rem";

      div.innerHTML = `
        <h3 style="margin-bottom:0.3rem;">
          <a href="${item.url}" target="_blank" rel="noopener">
            ${item.title}
          </a>
        </h3>
        <p style="margin:0; font-size:0.9rem; opacity:0.7;">
          ${item.source} · ${new Date(item.date).toLocaleDateString()}
        </p>
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
        updateURL(safePage - 1, activeTag);
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
        updateURL(safePage + 1, activeTag);
        render();
      };
      pagination.appendChild(next);
    }
  }

  renderDropdown(newsData, activeTag);
}

render();
</script>