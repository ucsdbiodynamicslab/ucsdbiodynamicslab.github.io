---
layout: default
title: "Knight Lab"
permalink: /people/rob-knight/
background: /assets/images/gurolBanner.jpg
toc: false
comments: false
---

<div class="pi-profile container" style="max-width: 1100px; padding: 2rem 1rem;">

  <div class="d-flex flex-wrap align-items-center justify-content-center mb-5">

    <div class="flex-shrink-0 me-4 text-center">
      <img src="/assets/images/headshots/rob_knight_headshot.jpeg"
           alt="Dr. Rob Knight"
           style="width: 220px; border-radius: 8px;">
    </div>

    <div style="min-width: 300px; max-width: 600px;">

      <h1 class="mb-2">Dr. Rob Knight</h1>

      <p class="mb-2">
        <strong>Wolfe Family Endowed Chair in Microbiome Research, Professor Rob Knight</strong><br>
        Departments of Bioengineering and Computer Science & Engineering<br>
        University of California San Diego
      </p>

      <ul class="list-inline mt-3">

        <li class="list-inline-item me-3">
          <a href="https://knightlab.ucsd.edu/" target="_blank" title="Lab Website">
            <i class="fa-solid fa-globe me-1"></i> Lab Website
          </a>
        </li>

        <li class="list-inline-item me-3">
          <a href="https://scholar.google.com/citations?user=_e3QL94AAAAJ&hl=en&oi=ao" target="_blank" title="Google Scholar">
            <i class="fa-brands fa-google-scholar me-1"></i> Google Scholar
          </a>
        </li>

        <li class="list-inline-item">
          <a href="mailto:rknight@ucsd.edu" title="Email">
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
      The Knight Lab uses and develops state-of-the-art computational and experimental techniques to ask fundamental questions about the evolution of the composition of biomolecules, genomes, and communities in different ecosystems, including the complex microbial ecosystems of the human body. We subscribe to an open-access scientific model, providing free, open-source software tools and making all protocols and data publicly available in order to increase general interest in and understanding of microbial ecology, and to further public involvement in scientific endeavors more generally.
    </p>
  </div>

  <hr class="my-5">

  <div class="row justify-content-center">

    <div class="col-md-10 mb-4">
      <h3>Recent News</h3>

      {% assign pi_name = "Rob Knight" %}
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
