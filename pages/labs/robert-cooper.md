---
layout: default
title: "Coopabacter labyi"
permalink: /people/rob-cooper/
background: /assets/images/gurolBanner.jpg
toc: false
comments: false
---

<div class="pi-profile container" style="max-width: 1100px; padding: 2rem 1rem;">

  <div class="d-flex flex-wrap align-items-center justify-content-center mb-5">

    <div class="flex-shrink-0 me-4 text-center">
      <img src="/assets/images/headshots/rcooper_headshot.jpeg"
           alt="Dr. Robert Cooper"
           style="width: 220px; border-radius: 8px;">
    </div>

    <div style="min-width: 300px; max-width: 600px;">

      <h1 class="mb-2">Dr. Robert Cooper</h1>

      <p class="mb-2">
        <strong>Research Scientist Robert Cooper</strong><br>
        Department Bioengineering<br>
        University of California San Diego
      </p>

      <ul class="list-inline mt-3">

        <li class="list-inline-item me-3">
          <a href="https://coopabacter.ucsd.edu/home" target="_blank" title="Lab Website">
            <i class="fa-solid fa-globe me-1"></i> Lab Website
          </a>
        </li>

        <li class="list-inline-item me-3">
          <a href="https://scholar.google.com/citations?hl=en&user=UWjM5p4AAAAJ" target="_blank" title="Google Scholar">
            <i class="fa-brands fa-google-scholar me-1"></i> Google Scholar
          </a>
        </li>

        <li class="list-inline-item">
          <a href="mailto:rcooper@ucsd.edu" title="Email">
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
      We combine theoretical and quantitative analysis (equations and modeling) with on-the-ground wet lab work. We like to understand how things (mainly bacteria) work, but we also like to apply that knowledge to program cells to do useful things, like biosensors. We're mainly working with the bacterium Acinetobacter baylyi, a fascinating character for what it can teach us about spreading antibiotic resistance, and its potential for powering low-cost, user-friendly DNA biosensors. We also work on various other interesting and/or useful things that are within, or adjacent to, our skill set. 
    </p>
  </div>

  <hr class="my-5">

  <div class="row justify-content-center">

    <div class="col-md-10 mb-4">
      <h3>Recent News</h3>

      {% assign pi_name = "Robert Cooper" %}
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
