# DeveloperHCR

<p align="center">
  <img src=".backend/Main/data.png" alt="DeveloperHCR logo" width="180">
</p>

**Independent software development and technology**

[![GitHub stars](https://img.shields.io/github/stars/DeveloperHCR/HCRAPP?style=for-the-badge&logo=github&label=GitHub%20stars)](https://github.com/DeveloperHCR/HCRAPP/stargazers)
[![README views](https://visitor-badge.laobi.icu/badge?page_id=DeveloperHCR.HCRAPP-README&left_text=README%20views&logo=github&right_color=0891b2)](https://visitor-badge.laobi.icu/)
[![Commits applied](https://img.shields.io/badge/commits_applied-153-0891b2?style=for-the-badge&logo=git&logoColor=white)](#commits-applied)

DeveloperHCR designs premium digital experiences across web, Android, AI-assisted tools, and developer-first software. This repository contains the official static website, DevX OS release information, visual assets, and supporting documentation for the project ecosystem.

## About

DeveloperHCR focuses on practical software and accessible digital experiences with a polished, product-first style. Core areas include:

- AI-assisted applications and developer workflows
- Android software and virtual desktop experiences
- Premium responsive web design and product storytelling
- Productivity tools and software experimentation

The website includes thoughtfully layered visual enhancements, subtle motion effects, and a hidden stealth-mode cue for a more premium feel without compromising clarity or accessibility.

## Website

The site is a static HTML and JavaScript project. Styles are embedded in the HTML pages so GitHub Pages can serve the site without a build step or external CSS files. The root GitHub Pages URL opens the DeveloperHCR Engine first, with the main home content available from the top navigation.

| Page | What it contains |
| --- | --- |
| Engine (default landing, first page) | DeveloperHCR Engine at `pages/search.html` with **unlimited** web search and full-screen results shown on the website (no other tab), on-device AI limited to **12 searches per browser** (unlimited for admin), multi-style themes, Chrome/Google-style local login/signup (no cloud), profile picture, device/CPU info, cookies/local extensions, top navigation and quick links to all inner and outer websites, and live commit/stats display |
| Home | DeveloperHCR introduction, featured projects, GitHub stars, commits applied, and demo links |
| Projects | HCRAPP, DevX OS, and DevX Billing summaries, tags, release links, a DevX OS browser preview, and a sandboxed DevX Billing preview |
| Contact | Email, public location, Google Map, and a message form that opens a prefilled email in the visitor's email app |
| Downloads | Link to the official DevX OS 3.0 stable APK release |
| About, Services, AI & API, Documentation, Gallery | Company and product information; About includes a browser-local demo status dashboard |
| Privacy, Terms | Website privacy and usage information |

The site supports English, Hindi, and Hinglish. Navigation, language selection, page-view badge display, and copyright year use lightweight JavaScript.

The contact form uses a `mail to:` link to open the visitor's configured email app with the message addressed to `developerhcr@gmail.com`. The visitor must review and send the email; the website itself does not transmit or store form submissions.

The About page's admin dashboard offers an expanded view, checks whether the static status page responds, and provides quick links to published pages. GitHub Pages hosts the site, so a personal PC does not need to stay on; if you run a separate local server on your computer, keep that computer on while serving the local site. The dashboard password is stored only in the current browser and is not server-side authentication; the static site does not provide a backend API or machine-level server monitoring.

The DeveloperHCR Engine (default first page) provides unlimited web search with full-screen results displayed on the website (no other tab) using embedded web result views and on-page result tools. Its on-device AI mode is limited to 12 searches per browser profile (unlimited for the admin account when signed in locally). The engine includes multiple website styles, full-screen search mode, Chrome/Google-style local login/signup (no cloud), local profile picture support, device/CPU/browser information shown on-device, local cookies/extensions, and quick access to inner website pages and outer websites. AI mode, settings, login/signup, profile, and AI search quota are stored locally in the browser (localStorage/cookies) with no cloud account or server-side storage.

### DevX OS browser demo

The DevX OS browser demo is an interactive website simulation of the desktop interface, with Files, Notes, Settings, an unlocked Admin Panel, Calculator, Calendar, a local-only sample Browser, a simulated safe Terminal, a sample System Monitor, and About apps. The Admin Panel needs no login and only changes in-memory sample data. The demo is not the Android application or a real operating system; nothing is persisted or sent, and system resources are not accessed. The Android release remains available from the [DevX OS stable release](https://github.com/DeveloperHCR/HCRAPP/releases/tag/DevXOS-3.0(stable)).

### DevX Billing demo safety

The embedded demo is served from the separate [DevX_Billing repository](https://github.com/DeveloperHCR/DevX_Billing). The embedded preview is sandboxed and does not persist data. The standalone app stores business records and configured AI credentials in browser local storage. Both projects use the `developerhcr.github.io` origin, so this storage is shared with other pages on that origin. Use sample information only; never enter real customer, invoice, payment, or API-key data.

### Stars, views, and commits

The GitHub stars badge is live. Website views count page loads through the visitor-badge service; repeated loads by the same person count separately, and counts may include automated traffic. The README has a separate counter. Commits applied shows the all-time total commits in this repository and is also surfaced on the GitHub Pages site. These are not GitHub repository traffic statistics. GitHub makes repository traffic views available to repository owners in [Insights → Traffic](https://github.com/DeveloperHCR/HCRAPP/graphs/traffic).

## Project links

- **Repository:** [github.com/DeveloperHCR/HCRAPP](https://github.com/DeveloperHCR/HCRAPP)
- **DeveloperHCR website:** [developerhcr.github.io/HCRAPP](https://developerhcr.github.io/HCRAPP/)
- **DevX OS browser demo:** [Try the interactive desktop preview](https://developerhcr.github.io/HCRAPP/pages/devx-os-demo.html)
- **DevX Billing demo:** [Try the live demo](https://developerhcr.github.io/DevX_Billing/)
- **DevX Billing repository:** [github.com/DeveloperHCR/DevX_Billing](https://github.com/DeveloperHCR/DevX_Billing)
- **DevX Billing release:** [DevX_billing_1.3.2](https://github.com/DeveloperHCR/DevX_Billing/releases/tag/DevX_billing_1.3.2)
- **GitHub release/tag:** [DevXOS-3.0(stable)](https://github.com/DeveloperHCR/HCRAPP/releases/tag/DevXOS-3.0(stable))
- **Public location:** Phuljori, Giridih, Jharkhand, India ([Google Maps](https://maps.app.goo.gl/qQdrrygNBAHfPKD16))
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
├── About.md             # About DeveloperHCR and project overview (served at /HCRAPP/About.md)
└── index.html           # Website homepage
```


## Commits applied

**Total commits applied (all time): 153** — tracked alongside GitHub stars and README/website views.

<details>
<summary>All commits applied over time (chronological, includes 76 listed entries)</summary>

- `9edfc87` (2026-10-07) — Initial commit
- `5a06690` (2026-10-07) — Create README.md
- `4b27865` (2026-10-07) — /data/
- `55415c6` (2026-10-07) — Create About.md
- `bc08e37` (2026-10-07) — Update README.md
- `fd4fb67` (2026-10-07) — Update README.md
- `ed290c0` (2026-10-07) — Update README.md
- `5c2375c` (2026-10-08) — Update README.md
- `e5011b9` (2026-10-08) — Update README.md
- `c76ce46` (2026-10-08) — Update README.md
- `b95c3a6` (2026-10-08) — Update README.md
- `4858149` (2026-10-08) — Update README.md
- `922293a` (2026-10-08) — Update README.md
- `661aa39` (2026-10-12) — Unzip
- `ae86c14` (2026-10-16) — Add files via upload
- `2ab5773` (2026-10-16) — Merge pull request #2 from DeveloperHCR/DevHCR
- `8c46d7a` (2026-10-16) — Create static.yml
- `1ecb7bf` (2026-10-16) — Delete DevX OS.apk
- `4137bf7` (2026-10-16) — Delete DevX-OS-2.0.1-BETA-FIXED.zip
- `063e6ff` (2026-10-16) — Delete DevX-OS-V3.5-RELEASE-FULL-FIX-1.zip
- `06bc987` (2026-10-16) — Delete HCRAPP-main.zip
- `47c9ed9` (2026-10-16) — Add files via upload
- `7742a51` (2026-10-16) — Delete .github/workflows directory
- `118cf6e` (2026-10-16) — Create static.yml
- `e03ec2c` (2026-10-16) — Update index.html
- `16421ca` (2026-10-16) — Create Backend.html
- `4867600` (2026-10-16) — Update index.html
- `e9b9dcc` (2026-10-16) — Update index.html
- `9553358` (2026-10-16) — Update index.html
- `e66b85d` (2026-10-16) — Update index.html
- `20a7270` (2026-10-16) — Update index.html
- `84ce43f` (2026-10-16) — Update index.html
- `2c2a018` (2026-10-17) — Update index.html
- `49d3b59` (2026-10-17) — Add files via upload
- `fe75347` (2026-10-17) — Delete index.html
- `435c994` (2026-10-17) — Rename hcrapp-portal-v3.html to Index.html
- `0fac556` (2026-10-17) — Rename Index.html to index.html
- `9893a0e` (2026-10-18) — Delete index.html
- `1ff4bc8` (2026-10-18) — Delete .github/workflows directory
- `192a651` (2026-10-18) — Create static.yml
- `7b26fac` (2026-10-18) — Create index.html
- `483d953` (2026-10-18) — Create index.html
- `b7d7f94` (2026-10-18) — Delete index.html
- `ffd669d` (2026-10-18) — Create index.html
- `11aeb8a` (2026-10-19) — Update index.html
- `42b5f59` (2026-10-19) — Update index.html
- `720142d` (2026-10-19) — Update index.html
- `3d97f1a` (2026-10-19) — Update index.html
- `8135e76` (2026-10-19) — Create backend.html
- `7196636` (2026-10-20) — Create data.png
- `4992260` (2026-10-20) — Delete .backend /main /data.png
- `66b9fd1` (2026-10-20) — Create Setup.md
- `2820f5b` (2026-10-20) — Add files via upload
- `3afad8d` (2026-10-20) — Update README.md
- `362ff2b` (2026-11-12) — Update index.html
- `2045586` (2026-11-15) — Prepare DeveloperHCR site for GitHub Pages
- `de3c3bc` (2026-11-15) — Initial commit
- `d253bbc` (2026-11-15) — Initial commit
- `c665ee1` (2026-11-15) — Improve GitHub Pages metrics and documentation
- `f7dece4` (2026-11-15) — Separate website and README view counts
- `c3593a0` (2026-11-15) — Update README.md
- `eb1f58a` (2026-11-15) — Feature DevX Billing project demo
- `65bde92` (2026-11-15) — Initial commit
- `cfe255d` (2026-11-15) — Add unlocked DevX OS admin demo
- `cbb5cf1` (2026-11-15) — Enhance website experience and contact email flow
- `31bc2a2` (2026-11-15) — Make advanced mode and email options visible
- `192e5e6` (2026-11-16) — Create SECURITY.md for security policy
- `78e6c95` (2026-11-16) — Create dependabot.yml
- `ca9370d` (2026-11-15) — Update README attribution
- `a2e04ce` (2026-11-16) — Refresh GitHub Pages content and status dashboard
- `5ebdf6e` (2026-11-16) — Improve homepage layout and add theme switch
- `8a7456e` (2026-11-16) — Refresh shared script cache version
- `59b26f7` (2026-11-16) — Update public map location
- `f50d09e` (2026-11-16) — Expand About admin dashboard
- `7196735` (2026-11-16) — Center admin server status
- `bf5d270` (2026-11-16) — Add DeveloperHCR search engine page

</details>

## License

This project is released under the [Unlicense](LICENSE).

> THE WORLD IS BLIND. **(DeveloperHCR - Abhimanyu Verma)**
