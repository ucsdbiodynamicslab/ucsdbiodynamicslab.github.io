# UCSD Synthetic Biology Institute & Biodynamics Lab Website

This is the combined website of the UCSD Synthetic Biology Institute and the UCSD Biodynamics Lab.

The site is designed to present the institute and lab clearly to prospective students, collaborators, and funding agencies while remaining simple for lab members to maintain. It is built using **Jekyll** and hosted through **GitHub Pages**, which allows the entire website to live in a version-controlled repository. All content is written in Markdown or simple HTML and compiled into a static site, making it fast, reliable, and easy to update.

The repository contains two closely related but structurally distinct components. The **Synthetic Biology Institute** pages form the top-level site, while the **Biodynamics Lab** website is nested within it. This arrangement allows both entities to share styling, navigation, and infrastructure while maintaining their own content and sections.

## Design Philosophy

The design philosophy of this site prioritizes:

- **Clarity for visitors** — especially prospective students, collaborators, and funding agencies  
- **Low maintenance for lab members** — most pages are simple Markdown files that can be edited directly  
- **Transparency and version control** — all changes occur through Git commits  
- **Speed and reliability** — the site compiles to static files and requires no database or backend server  

Where possible, routine tasks such as publication updates and document handling are partially automated through scripts and lightweight services connected to the repository.

## Purpose of This README

This README is intended to help future lab members understand:

- the structure of the site  
- how to safely edit content  
- how the underlying infrastructure works  

Even if you have never worked with Jekyll before, most common tasks (editing text, adding people, updating publications, etc.) should take only a few minutes once you understand the layout of the repository.

# Dependencies Needed to Edit

Editing the website requires only a small number of standard tools. In most cases you will only need **Git**, **Ruby**, and **Jekyll**. Once these are installed, you can run a local development server to preview changes before committing them.

## 1. Git

The website is stored in a Git repository and hosted through GitHub Pages. You will need Git to clone the repository, pull updates, and push changes.

Check if Git is installed:

```git --version```

If it is not installed, install it through your system package manager.

## 2. Ruby

Jekyll is written in Ruby and requires a working Ruby installation. Check your Ruby version:

```ruby --version```

## 3. Bundler

Bundler manages the Ruby packages required by the website. Install it with:

```gem install bundler```

## 4. Jekyll and Site Dependencies

All required Ruby packages are listed in the Gemfile. After cloning the repository, install them with

```bundle install```

This initiates **Jekyll** and any additional plugins required to build the site. 

## 5. Running the Local Development Server

Once the dependencies are installed, you can preview the website locally:

```bundle exec jekyll serve```

This will start a local server, typically available at:

```http://localhost:4000```

Any changes you make to files in the repository will automatically rebuild the site so you can preview them in your browser.

# Big Picture of How the Site Works

This website is a **static site generated with Jekyll** and hosted on **GitHub Pages**. Instead of running a database or backend server, the entire site is built from Markdown, HTML templates, and configuration files stored in this repository. Jekyll compiles these files into a set of static HTML pages that are served directly to visitors.

At a high level, the workflow looks like this:

1. **Content is written in Markdown or HTML**  
   Most pages on the site are simple Markdown files. These contain the text content along with a small block of metadata at the top called **front matter**.

2. **Layouts define the page structure**  
   Layout files (located in `_layouts/`) define the common structure of pages such as headers, navigation bars, and footers. Individual pages reference a layout in their front matter.

3. **Includes provide reusable components**  
   Small reusable pieces of the site (navigation menus, footers, profile elements, etc.) are stored in `_includes/`. Layouts and pages can insert these components where needed.

4. **Data files automatically populate many pages**  
   Much of the site's structured content is stored in **YAML files inside the `_data/` directory**. These files act like a lightweight database. Jekyll templates read these `.yml` files and automatically generate page content such as lists of people, publications, or other structured information.

   For example, a single YAML entry describing a lab member or publication can automatically populate multiple parts of the site. This avoids duplicating information and makes updates much easier. In many cases, adding or modifying one entry in a `_data/*.yml` file is all that is needed to update several pages at once.

5. **Assets store images, styles, and scripts**  
   Static files such as images, CSS, and JavaScript live in the `assets/` directory and are served directly by the site.

6. **Jekyll builds the site**  
   When the site is built (either locally with `jekyll serve` or automatically by GitHub Pages), Jekyll processes all pages, layouts, templates, and data files to produce a final static website.

7. **GitHub Pages hosts the result**  
   When changes are pushed to the repository, GitHub automatically rebuilds the site and publishes the updated version.

In practice, most edits only require modifying a Markdown page or adding an entry to one of the YAML files in `_data/`. The templates handle the formatting and page generation automatically.

# Basics of Petridish

The **Jekyll** template that the site is built on is called Petridish. Making changes to basic site elements like the navigation bar or adding new pages is well explained on the [Petridish Site](https://peterdesmet.com/petridish/).

# Adding People to the Institute

The institute members on synbio.ucsd.edu/mems/ are automatically populated from /_data/team.yml. To add a member, add an entry to team.yml using this format:

```- name: Jeff Hasty
  role: Director
  image: assets/images/headshots/jhasty_headshot.jpg
  description: >
    Genetic Circuits • Biophysics • Engineered Ecologies
  googlescholar: 5rjhaooAAAAJ&hl=en&oi=ao
  email: jhasty@ucsd.edu```

Notice that you will need to add a headshot of the new member PI in assets/images/headshots. The googlescholar: field needs to be set to the part of the PIs Google Scholar page following "https://scholar.google.com/citations?user=". Do not include anything but the final alphanumeric string, or the link will break. 

# Adding People to the Biodynamics Lab

When a new member joins that Biodynamics Lab, they must be added to synbio.ucsd.edu/biodynamics/people/. This page is automatically populated from _data/biodynamics-lab/people.yml. To add a lab member, add an entry in this format: 


```- name: Jeff Hasty
  photo: /assets/images/biodynamics/portraits/jeff.jpeg
  alt_photo: /assets/images/biodynamics/portraits/jeffFun.jpeg
  interests:
    - Bioengineering
    - Physics
    - Biology
  scholar: https://scholar.google.com/citations?user=5rjhaooAAAAJ&hl=en&oi=ao
  scholar_new_tab: true
  role: Faculty
  ```

For each new member, you will need to place a serious photo ('photo') and a fun photo ('alt_photo') of the new member in /assets/images/biodynamics/portraits/. An alt_photo is optional, but should only ever be excluded for Collaborators. Undergraduates do not get photos. Note that, unlike the synbio members page, here scholar: must map to the individual's full google scholar url. This entry can also be used to link a personal website or personal page on synbio.ucsd.edu. The only allowed values for the 'role:' entry are Faculty, Postdoctoral Fellow, PhD Student, Master's Student, Undergraduate Student, Staff, and Collaborator. 'scholar_new_tab:' should be set to true unless the individual has an internal synbio.ucsd.edu page. 

# Newsbot

The lab website includes an automated **newsbot** that periodically searches for media coverage related to lab PIs and adds new articles to the site.

## How It Works

1. **PI list**  
   The script reads `_data/pis.yml`, which contains the names of all PIs whose news coverage should be tracked.

2. **Google News queries**  
   For each PI, the script queries the Google News RSS API using a search string of the form:

   ''' <PI Name> Synthetic Biology UCSD '''


This helps bias results toward relevant scientific news coverage.

3. **Article parsing**  
Each RSS entry is parsed to extract:
- title
- url
- source
- publication date
- summary (if available)

4. **Tag generation**  
Each article receives:
- the PI name
- the tag `UCSD Synthetic Biology`
- additional keywords automatically extracted from capitalized phrases in the title and summary

5. **Deduplication**  
Articles are deduplicated by URL.  
If the same article appears in searches for multiple PIs, the existing entry is updated so **all relevant PI names are kept as tags**.

6. **Storage**  
All news items are stored in `_data/news.yml`.  
The script sorts entries by date before saving.

7. **Rendering on the site**  
The website reads `_data/news.yml` and renders articles dynamically using JavaScript. Pages can filter articles by tags (for example, a subsite can show only articles related to specific PIs).

## Running the Newsbot

The script lives at:

``` assets/python/fetch_news.py ```


To run it manually:

``` python3 assets/python/fetch_news.py ```

New articles will be appended to _data/news.yml if they are not already present. 

## Maintenance Notes

- Add or remove PIs in _data/pis.yml to change whose news coverage is tracked
- The site does **not** scrape articles directly. It only reads from _data/news.yml
- If the news feed ever behaves unexpectedly, deleting _data/news.yml and rerunning the script (or GitHub Action) will regenerate the dataset from fresh searches

# Publications Bot

## Publications Bot

The Biodynamics Lab publications page is automatically populated using a Python script that fetches papers from the Semantic Scholar API and writes them to a YAML data file used by the website.

### Overview

The publications system has three components:

1. **Publication Fetch Script**
2. **Structured Data File**
3. **GitHub Actions Automation**

Together these ensure the publications page stays up to date without manual editing.

---

## 1. Publication Fetch Script

Location:

``` assets/python/fetch_publications.py ```


This script queries the Semantic Scholar API for publications associated with Jeff Hasty. Because Semantic Scholar created multiple author profiles for Jeff, the script explicitly checks multiple author IDs.

Current author IDs queried: 2916647, 2245535793, 2367545890


The script performs the following tasks:

- Fetches publications from all three author profiles
- Respects Semantic Scholar API rate limits
- Deduplicates publications across author IDs
- Extracts key metadata:
  - title
  - authors
  - journal
  - publication date
  - year
  - paper link (DOI preferred)
- Sorts publications by publication date
- Writes the results to the site data directory

Output file:

```_data/biodynamics-lab/publications.yml ```


This file is then used by the website to render the publications page.

---

## 2. Publications Data File

Location:

```_data/biodynamics-lab/publications.yml ```


This YAML file contains structured publication entries. Example entry:

```
- title: Rational engineering of combinatorial bacterial therapies for cancer
  journal: Genome Biology
  authors:
    - Paige Steppe
    - Katherine O’Connor
    - J. Hasty
  publication_date: "2026-01-28"
  year: 2026
  link: https://doi.org/10.1186/s13059-026-03951-0 ```

The publications page loads this file at build time and uses JavaScript to:

- sort publications by date
- group them by year
- dispaly titles with links to the papers
- paginate results (20 pubs per page)

---

## 3. GitHub Actions Automation
WIP




# The Publications File Server

# Handling DNS Stuff