---
layout: default
title: "Knight Lab"
permalink: /people/omar-din/
background: /assets/images/gurolBanner.jpg
toc: false
comments: false
---

<div class="pi-profile container" style="max-width: 1100px; padding: 2rem 1rem;">

  <div class="d-flex flex-wrap align-items-center justify-content-center mb-5">

    <div class="flex-shrink-0 me-4 text-center">
      <img src="/assets/images/headshots/Omar_din_headshot.png"
           alt="Dr. Omar Din"
           style="width: 220px; border-radius: 8px;">
    </div>

    <div style="min-width: 300px; max-width: 600px;">

      <h1 class="mb-2">Dr. Omar Din</h1>

      <p class="mb-2">
        <strong>Postdoctoral Fellow Omar Din</strong><br>
        Department of Pediatrics<br>
        University of California San Diego
      </p>

      <ul class="list-inline mt-3">

        <li class="list-inline-item me-3">
          <a href="https://omardin.name/" target="_blank" title="Lab Website">
            <i class="fa-solid fa-globe me-1"></i> Lab Website
          </a>
        </li>

        <li class="list-inline-item me-3">
          <a href="https://scholar.google.com/citations?user=-zgyXN8AAAAJ&hl=en&oi=ao" target="_blank" title="Google Scholar">
            <i class="fa-brands fa-google-scholar me-1"></i> Google Scholar
          </a>
        </li>

        <li class="list-inline-item">
          <a href="mailto:odin@health.ucsd.edu" title="Email">
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
      My research focuses on understanding how microbial communities evolve and function in different environments, and on using that knowledge to design engineered microbes and quantitative tools that can improve human health. As a Ph.D. student in Dr. Jeff Hasty’s lab at UC San Diego, I developed the synchronized lysis circuit (SLC) and related synthetic microbial ecosystems for therapeutic delivery, leading to publications in Nature, Nature Microbiology, Science, and Science Advances.

        More recently, in the Knight Lab, I have been developing long-read metagenomics approaches that resolve microbiomes down to individual strains and alleles and enable quantitative measurements from sequencing data over time. I apply these methods to various questions in human health and environmental microbial surveillance.

        I also gained translational experience with GenCirq, Inc., a biotechnology start-up that commercializes engineered bacterial therapeutics based on synthetic gene circuits originally developed during my graduate work.
    </p>
  </div>

  <hr class="my-5">

  <div class="row justify-content-center">

    <div class="col-md-10 mb-4">
      <h3>Recent News</h3>

      {% assign pi_name = "Omar Din" %}
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
