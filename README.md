# DeveloperHCR

<p align="center">
  <img src=".backend/Main/data.png" alt="DeveloperHCR logo" width="180">
</p>

**Independent software development and technology**

[![GitHub stars](https://img.shields.io/github/stars/DeveloperHCR/HCRAPP?style=for-the-badge&logo=github&label=GitHub%20stars)](https://github.com/DeveloperHCR/HCRAPP/stargazers)
[![README views](https://visitor-badge.laobi.icu/badge?page_id=DeveloperHCR.HCRAPP-README&left_text=README%20views&logo=github&right_color=0891b2)](https://visitor-badge.laobi.icu/)

DeveloperHCR designs premium digital experiences across web, Android, AI-assisted tools, and developer-first software. This repository contains the official static website, DevX OS release information, visual assets, and supporting documentation for the project ecosystem.

## About

DeveloperHCR focuses on practical software and accessible digital experiences with a polished, product-first style. Core areas include:

- AI-assisted applications and developer workflows
- Android software and virtual desktop experiences
- Premium responsive web design and product storytelling
- Productivity tools and software experimentation

The website includes thoughtfully layered visual enhancements, subtle motion effects, and a hidden stealth-mode cue for a more premium feel without compromising clarity or accessibility.

## Website

The site is a static HTML and JavaScript project. Styles are embedded in the HTML pages so GitHub Pages can serve the site without a build step or external CSS files. The landing page has a more refined visual treatment with gradient depth, glassmorphism panels, hover motion, and selective interactive polish.

| Page | What it contains |
| --- | --- |
| Home | DeveloperHCR introduction, featured projects, GitHub stars, and demo links |
| Projects | HCRAPP, DevX OS, and DevX Billing summaries, tags, release links, a DevX OS browser preview, and a sandboxed DevX Billing preview |
| Contact | Email, public location, Google Map, and a message form that opens a prefilled email in the visitor's email app |
| Downloads | Link to the official DevX OS 3.0 stable APK release |
| About, Services, AI & API, Documentation, Gallery | Company and product information |
| Privacy, Terms | Website privacy and usage information |

The site supports English, Hindi, and Hinglish. Navigation, language selection, page-view badge display, and copyright year use lightweight JavaScript.

The contact form uses a `mailto:` link to open the visitor's configured email app with the message addressed to `developerhcr@gmail.com`. The visitor must review and send the email; the website itself does not transmit or store form submissions.

### DevX OS browser demo

The DevX OS browser demo is an interactive website simulation of the desktop interface, with Files, Notes, Settings, an unlocked Admin Panel, Calculator, Calendar, a local-only sample Browser, a simulated safe Terminal, a sample System Monitor, and About apps. The Admin Panel needs no login and only changes in-memory sample data. The demo is not the Android application or a real operating system; nothing is persisted or sent, and system resources are not accessed. The Android release remains available from the [DevX OS stable release](https://github.com/DeveloperHCR/HCRAPP/releases/tag/DevXOS-3.0(stable)).

### DevX Billing demo safety

The embedded demo is served from the separate [DevX_Billing repository](https://github.com/DeveloperHCR/DevX_Billing). The embedded preview is sandboxed and does not persist data. The standalone app stores business records and configured AI credentials in browser local storage. Both projects use the `developerhcr.github.io` origin, so this storage is shared with other pages on that origin. Use sample information only; never enter real customer, invoice, payment, or API-key data.

### Stars and views

The GitHub stars badge is live. Website views count page loads through the visitor-badge service; repeated loads by the same person count separately, and counts may include automated traffic. The README has a separate counter. These are not GitHub repository traffic statistics. GitHub makes repository traffic views available to repository owners in [Insights → Traffic](https://github.com/DeveloperHCR/HCRAPP/graphs/traffic).

## Project links

- **Repository:** [github.com/DeveloperHCR/HCRAPP](https://github.com/DeveloperHCR/HCRAPP)
- **DeveloperHCR website:** [developerhcr.github.io/HCRAPP](https://developerhcr.github.io/HCRAPP/)
- **DevX OS browser demo:** [Try the interactive desktop preview](https://developerhcr.github.io/HCRAPP/pages/devx-os-demo.html)
- **DevX Billing demo:** [Try the live demo](https://developerhcr.github.io/DevX_Billing/)
- **DevX Billing repository:** [github.com/DeveloperHCR/DevX_Billing](https://github.com/DeveloperHCR/DevX_Billing)
- **DevX Billing release:** [DevX_billing_1.3.2](https://github.com/DeveloperHCR/DevX_Billing/releases/tag/DevX_billing_1.3.2)
- **GitHub release/tag:** [DevXOS-3.0(stable)](https://github.com/DeveloperHCR/HCRAPP/releases/tag/DevXOS-3.0(stable))
- **Public location:** Phuljori, Giridih, Jharkhand, India ([Google Maps](https://maps.app.goo.gl/k4rmCBtXUHK1BVem9))
- **YouTube:** [DeveloperHCR](https://youtube.com/@developerhcr)
- **Email:** [developerhcr@gmail.com](mailto:developerhcr@gmail.com)
- **Stable DevX OS APK:** [Download](<https://github.com/DeveloperHCR/HCRAPP/releases/download/DevXOS-3.0(stable)/DevXOS3.0.apk>)

## Run the website locally

No package installation is required. From the repository root, run:

```bash
python3 -m http.server 8000
```

Then open [http://localhost:8000](http://localhost:8000). For a more polished preview, refresh once the page is loaded and explore the page motion and UI details.

## Deployment

The GitHub Actions workflow in [`.github/workflows/static.yml`](.github/workflows/static.yml) deploys the repository to GitHub Pages whenever changes are pushed to `main`. The Pages build source should be set to **GitHub Actions** in the repository settings.

## Repository structure

```text
.
├── .backend/Main/       # Logo image and legacy setup note
├── .github/workflows/   # GitHub Pages deployment workflow
├── assets/images/       # Website logo and artwork
├── data/web/            # Nested static backend-status page
├── js/                  # Site navigation and small UI behaviors
├── pages/               # Site pages; index.html remains at the root
├── About.md             # Legacy DevX OS setup guide
└── index.html           # Website homepage
```

## License

This project is released under the [Unlicense](LICENSE).

> THE WORLD IS BLIND. **(DeveloperHCR)**
