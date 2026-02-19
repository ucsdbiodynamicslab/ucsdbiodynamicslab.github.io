---
layout: default
title: "Biodynamics Lab"
permalink: /people/lev-tsimring/
background: /assets/images/gurolBanner.jpg
toc: false
comments: false
---

<div class="pi-profile container" style="max-width: 1100px; padding: 2rem 1rem;">

  <div class="d-flex flex-wrap align-items-center justify-content-center mb-5">

    <div class="flex-shrink-0 me-4 text-center">
      <img src="/assets/images/headshots/Lev_Tsimring_headshot.jpg"
           alt="Dr. Lev Tsimring"
           style="width: 220px; border-radius: 8px;">
    </div>

    <div style="min-width: 300px; max-width: 600px;">

      <h1 class="mb-2">Dr. Lev Tsimring</h1>

      <p class="mb-2">
        <strong>Distringuished Research Scientist Lev Tsimring</strong><br>
        Synthetic Biology Institute<br>
        University of California San Diego
      </p>

      <ul class="list-inline mt-3">

        <li class="list-inline-item me-3">
          <a href="https://lab-website-url.edu" target="_blank" title="Lab Website">
            <i class="fa-solid fa-globe me-1"></i> Lab Website
          </a>
        </li>

        <li class="list-inline-item me-3">
          <a href="https://scholar.google.com/citations?user=Muw0HmEAAAAJ&hl=en&oi=ao" target="_blank" title="Google Scholar">
            <i class="fa-brands fa-google-scholar me-1"></i> Google Scholar
          </a>
        </li>

        <li class="list-inline-item">
          <a href="mailto:ltsimring@ucsd.edu" title="Email">
            <i class="fa-regular fa-envelope me-1"></i> Email
          </a>
        </li>

      </ul>

    </div>

  </div>

  <hr class="my-5">

  <div class="text-center" style="max-width: 800px; margin: 0 auto;">
    <h2>Research Overview</h2>
    <p>
      The Biodynamics Laboratory (BDL) seeks to understand the network interactions that mediate gene regulation and cellular signaling. Since behavior arising from these complex interactions is difficult to predict with qualitative reasoning, we employ experimentally validated computational modeling approaches. We design and construct de novo synthetic gene circuits, which provide a natural framework for reducing the complexity of gene regulatory networks. We use tools from physics and engineering to study such simplified systems and to dissect, analyze, and control the modular components that govern the dynamics of gene regulation and cellular signaling.
    </p>
  </div>

  <hr class="my-5">

  <div class="row justify-content-center">

    <div class="col-md-10 mb-4">
      <h3>Recent News</h3>

      {% assign pi_name = "Lev Tsimring" %}
      {% assign filtered_news = site.data.news
          | where_exp: "item", "item.tags contains pi_name"
          | sort: "date"
          | reverse %}

      {% if filtered_news.size > 0 %}
        <ul class="list-unstyled">

          {% for article in filtered_news limit: 5 %}
            <li class="mb-3">
              <a href="{{ article.url }}" target="_blank">
                {{ article.title | strip }}
              </a><br>
              <small class="text-muted">
                {{ article.source }} |
                {{ article.date | date: "%B %d, %Y" }}
              </small>
            </li>
          {% endfor %}

        </ul>
      {% else %}
        <p class="text-muted">No recent news articles.</p>
      {% endif %}

    </div>

  </div>

</div>
