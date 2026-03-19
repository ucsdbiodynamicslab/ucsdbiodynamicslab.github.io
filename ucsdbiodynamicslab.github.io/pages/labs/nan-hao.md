---
layout: default
title: "Hao Lab"
permalink: /people/nan-hao/
background: /assets/images/gurolBanner.jpg
toc: false
comments: false
---

<div class="pi-profile container" style="max-width: 1100px; padding: 2rem 1rem;">

  <div class="d-flex flex-wrap align-items-center justify-content-center mb-5">

    <div class="flex-shrink-0 me-4 text-center">
      <img src="/assets/images/headshots/nhao_headshot.jpg"
           alt="Dr. Nan Hao"
           style="width: 220px; border-radius: 8px;">
    </div>

    <div style="min-width: 300px; max-width: 600px;">

      <h1 class="mb-2">Dr. Nan Hao</h1>

      <p class="mb-2">
        <strong>Professor Nan Hao</strong><br>
        Department of Molecular Biology<br>
        University of California San Diego
      </p>

      <ul class="list-inline mt-3">

        <li class="list-inline-item me-3">
          <a href="https://haolab.ucsd.edu/" target="_blank" title="Lab Website">
            <i class="fa-solid fa-globe me-1"></i> Lab Website
          </a>
        </li>

        <li class="list-inline-item me-3">
          <a href="https://scholar.google.com/citations?user=4TlPy6MAAAAJ&hl=en" target="_blank" title="Google Scholar">
            <i class="fa-brands fa-google-scholar me-1"></i> Google Scholar
          </a>
        </li>

        <li class="list-inline-item">
          <a href="mailto:nhao@ucsd.edu" title="Email">
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
      In recent years, genomic sequencing and systematic analysis have revealed many molecular components that control gene expression at multiple levels, and detailed the myriad of interactions among and between these regulatory modules. However, it remains unclear how these molecular networks operate in time and space to carry out diverse cellular functions. The goal of our lab is to understand how network architecture governs the dynamics and function of regulatory responses in the context of stresses, aging, or diseases.
    
    Our lab uses multidisciplinary approaches, integrating biology, engineering and computer science, in our studies. We develop and use novel microfluidics and imaging technologies to quantitatively track the dynamics of molecular processes in single living cells and construct computational models to describe and predict cellular behaviors.
    </p>
  </div>

  <hr class="my-5">

  <div class="row justify-content-center">

    <div class="col-md-10 mb-4">
      <h3>Recent News</h3>

      {% assign pi_name = "Nan Hao" %}
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
