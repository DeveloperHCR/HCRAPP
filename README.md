# DeveloperHCR

<p align="center">
  <img src=".backend/Main/data.png" alt="DeveloperHCR logo" width="180">
</p>

**Independent software development and technology**

[![GitHub stars](https://img.shields.io/github/stars/DeveloperHCR/HCRAPP?style=for-the-badge&logo=github&label=GitHub%20stars)](https://github.com/DeveloperHCR/HCRAPP/stargazers)
[![README views](https://visitor-badge.laobi.icu/badge?page_id=DeveloperHCR.HCRAPP-README&left_text=README%20views&logo=github&right_color=0891b2)](https://visitor-badge.laobi.icu/)

DeveloperHCR builds digital experiences across web, Android, AI-assisted tools, and developer-focused software. This repository contains the official static website, the DevX OS release information, visual assets, and supporting documentation.

## About

DeveloperHCR focuses on practical software and accessible digital experiences. Project areas include:

- AI-assisted applications and developer workflows
- Android software and virtual desktop experiences
- Web design and responsive user interfaces
- Productivity tools and software experimentation

## Website

The site is a static HTML and JavaScript project. Styles are embedded in the HTML pages so GitHub Pages can serve the site without a build step or external CSS files.

| Page | What it contains |
| --- | --- |
| Home | DeveloperHCR introduction, featured projects, GitHub stars, and live-site link |
| Projects | HCRAPP and DevX OS summaries, project tags, release link, and an embedded website preview |
| Contact | Email, public location, Google Map, and contact form demonstration |
| Downloads | Link to the official DevX OS 3.0 stable APK release |
| About, Services, AI & API, Documentation, Gallery | Company and product information |
| Privacy, Terms | Website privacy and usage information |

The site supports English, Hindi, and Hinglish. Navigation, language selection, page-view badge display, and copyright year use lightweight JavaScript.

The contact form is a visual demonstration only; it does not send or store submissions.

### Stars and views

The GitHub stars badge is live. Website views count page loads through the visitor-badge service; repeated loads by the same person count separately, and counts may include automated traffic. The README has a separate counter. These are not GitHub repository traffic statistics. GitHub makes repository traffic views available to repository owners in [Insights → Traffic](https://github.com/DeveloperHCR/HCRAPP/graphs/traffic).

## Project links

- **Repository:** [github.com/DeveloperHCR/HCRAPP](https://github.com/DeveloperHCR/HCRAPP)
- **Live website demo:** [developerhcr.github.io/HCRAPP](https://developerhcr.github.io/HCRAPP/)
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

Then open [http://localhost:8000](http://localhost:8000).

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
