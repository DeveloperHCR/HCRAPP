# DeveloperHCR

<p align="center">
  <img src=".backend/Main/data.png" alt="DeveloperHCR logo" width="180">
</p>

**Independent software development and technology**

[![GitHub stars](https://img.shields.io/github/stars/DeveloperHCR/HCRAPP?style=for-the-badge&logo=github&label=GitHub%20stars)](https://github.com/DeveloperHCR/HCRAPP/stargazers)

DeveloperHCR creates digital experiences across web, Android, AI-assisted tools, and developer-focused software. This repository contains the DeveloperHCR static website, its visual assets, and supporting project documentation.

## About

DeveloperHCR is focused on practical, accessible software and modern digital experiences. Current areas of interest include:

- AI-assisted applications and developer workflows
- Android software and virtual desktop experiences
- Web design and responsive user interfaces
- Productivity tools and software experimentation

## Website

The site is a static HTML and JavaScript project. Its styles are embedded in each HTML page so they work consistently on GitHub Pages. It includes a brand homepage, project information, contact details, and supporting informational pages.

- Responsive layout and mobile navigation
- English, Hindi, and Hinglish interface language selection
- Shared logo and artwork assets
- Lightweight JavaScript for navigation, language selection, and the copyright year
- GitHub Pages deployment through [`.github/workflows/static.yml`](.github/workflows/static.yml)

The contact form is currently a front-end demonstration and does not send or store submissions.

## Project links

- **Repository:** [github.com/DeveloperHCR/HCRAPP](https://github.com/DeveloperHCR/HCRAPP)
- **Live website demo:** [developerhcr.github.io/HCRAPP](https://developerhcr.github.io/HCRAPP/)
- **YouTube:** [DeveloperHCR](https://youtube.com/@developerhcr)
- **Email:** [developerhcr@gmail.com](mailto:developerhcr@gmail.com)
- **Stable DevX OS APK:** [Download](<https://github.com/DeveloperHCR/HCRAPP/releases/download/DevXOS-3.0(stable)/DevXOS3.0.apk>)

## Run the website locally

No package installation is required. From the repository root, run:

```bash
python3 -m http.server 8000
```

Then open [http://localhost:8000](http://localhost:8000).

## Repository structure

```text
.
├── .backend/Main/       # Supplied logo image and legacy setup note
├── .github/workflows/   # GitHub Pages deployment workflow
├── assets/images/       # Website logo and artwork
├── data/web/            # Nested static backend-status page
├── js/                  # Site navigation and small UI behaviors
├── pages/               # Site pages; index.html remains at the root
├── About.md             # Legacy DevX OS setup guide
└── index.html           # Website homepage
```

## Deployment

The GitHub Actions workflow publishes the repository to GitHub Pages when changes are pushed to the `main` branch. Enable GitHub Pages for the repository and select **GitHub Actions** as the build and deployment source.

## License

This project is released under the [Unlicense](LICENSE).
