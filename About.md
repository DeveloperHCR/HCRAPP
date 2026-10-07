# 🚀 DevX OS 2.0.1 BETA — Complete Setup & APK Build Guide

DevX OS — Professional Virtual Workspace
Owner: Abhimanyu Verma
Location: Near Utkramit Madhya Vidyalay Phuljori (or Pandayd), Giridih, Jharkhand, India

Version: DevX OS 2.0.1 BETA


## 📌 ABOUT DEVX OS

DevX OS is a custom virtual desktop and workspace application with a modern dark gaming-style interface.

Features include:

🎮 Free Fire-inspired gaming UI
🖥️ Windows-style desktop
🌌 Dark/neon interface
📱 Android touch support
🖱️ Mouse support
⌨️ Keyboard support
🪟 Movable windows
↔️ Resizable windows
➖ Minimize
□ Maximize / Restore
❌ Close
🤖 AI features
💻 Code Assist
🛠️ Developer tools
📦 App management
👤 Admin and Guest modes


## 📱 REQUIREMENTS

Install:

- Android Studio
- Android SDK
- Android SDK Platform
- Android SDK Build-Tools
- Android SDK Platform-Tools
- Compatible JDK
- Required Gradle components


## 📦 OPEN THE PROJECT

Extract:

DevX-OS-2.0.1-BETA-FIXED.zip

Open Android Studio.

Select:

Open

Then select:

dh/

Do NOT open only:

dh/app/

The correct project folder contains files such as:

settings.gradle
build.gradle
app/


## 🔄 GRADLE SYNC

After opening the project, wait for Gradle Sync.

If Android Studio asks to install missing SDK, Gradle or Build Tools components, install them.

Wait until Gradle Sync finishes successfully.


## 🏗️ BUILD DEBUG APK

Android Studio menu:

Build
→ Build Bundle(s) / APK(s)
→ Build APK(s)

After the build finishes, select:

Locate

The APK is normally generated at:

app/build/outputs/apk/debug/app-debug.apk


## 📱 INSTALL APK

Copy app-debug.apk to your Android phone.

Open the APK and install it.

If Android asks for installation permission, allow the required permission.


## 🚀 BOOT SCREEN

DevX OS startup flow:

🚀 DevX OS
↓
🔄 Boot / Loading
↓
👤 Admin Setup or Login
↓
⚙️ Setup Center
↓
🖥️ DevX OS Desktop

The boot screen must remain inside the available screen size.

It should not create unwanted scrolling, overflow or controls outside the screen.


## 👤 CREATE ADMIN

First launch should provide:

👤 Username
🔐 Password
🔐 Confirm Password
🚀 Create Admin

Example:

Username: admin
Password: YourStrongPassword

Never publish your real password on GitHub.


## ⚙️ SETUP CENTER

Setup Center provides access to:

⚙️ Settings
🛠️ Troubleshooting
🩺 App Health
🤖 AI
💻 Environment
🔐 Security
👤 Account
ℹ️ About


## 👤 RUN AS GUEST

DevX OS provides a limited temporary Guest Mode.

Button:

👤 Run as Guest

Default Guest session:

⏱️ 1 minute

Guest users should NOT receive full Admin access.

Selected basic applications may be available:

📝 Notes
🧮 Calculator
🎮 Games
🆘 Help
ℹ️ About
⏱️ Clock
📁 Limited File Manager

Admin-only features remain protected.

When the Guest session expires:

⏱️ Session Expired
↓
🚪 Exit Guest Mode

Temporary Guest data should be cleaned where supported.


## ⚙️ SETTINGS

Settings must open correctly.

Settings should support:

🖱️ Move
↔️ Resize
➖ Minimize
□ Maximize / Restore
❌ Close

Settings must work with Android touch and PC mouse/keyboard where supported.


## 🛠️ TROUBLESHOOTING

Open:

🛠️ Troubleshooting

The Troubleshooting window should support:

🖱️ Move
↔️ Resize
➖ Minimize
□ Maximize
❌ Close

It must not freeze the complete application.


## 🩺 APP HEALTH

Open:

🩺 App Health

The application must safely handle missing system information.

Unavailable CPU/RAM/network data must never crash the complete application.


## ♻️ RESET SYSTEM

Open:

⚙️ Settings
→ ♻️ Reset System

Reset System is intended to reset local DevX OS configuration and data.

A reset may remove:

👤 Local accounts
⚙️ Local settings
🧩 App configuration
👤 Guest session data
🖥️ Desktop preferences

The APK/application itself is not automatically uninstalled by an in-app reset.

After a complete reset, DevX OS may return to:

👤 First Admin Setup

Always back up important data before resetting.


## 🤖 AI FEATURES

DevX OS includes an AI environment.

Possible AI features:

🤖 AI Assistant
💬 AI Chat
🧠 AI Models
🛠️ AI Tools
🎙️ Voice-related features

AI services may require an AI provider or API configuration.

Never publish private API keys on GitHub.


## 💻 CODE ASSIST

DevX OS includes:

💻 Code Assist

Code Assist is the developer-focused coding environment.

Features may include:

📁 Project Explorer
📄 Code Editor
🔍 Code Search
🔎 Find & Replace
📝 Code Editing
▶️ Run / Preview
🛠️ Build
🐞 Debug
💻 Terminal
📋 Clipboard
📦 Project Management
🤖 AI Coding Assistant
🧠 Code Explanation
✨ Code Suggestions
🐛 Error Assistance
🔧 Code Fixing
♻️ Refactoring


## 🧠 CODE ASSIST AI

AI-powered Code Assist may provide:

💡 Generate Code
🤖 Explain Code
🐛 Find Errors
🔧 Fix Errors
♻️ Refactor Code
📝 Generate Comments
📚 Explain Functions
🔍 Analyze Project
✨ Code Suggestions

AI functionality depends on the configured AI provider/model.


## 📁 FILE MANAGER

DevX OS includes:

📁 File Manager

Available file operations depend on Android storage permissions and the current implementation.


## 🌐 BROWSER

DevX OS may provide:

🌐 Browser

Internet access requires a network connection and supported configuration.


## ⌨️ TERMINAL

DevX OS may include:

⌨️ Terminal

Terminal capabilities are limited by Android security and sandbox restrictions.


## 🛠️ DEVELOPER TOOLS

Developer tools may include:

💻 Code Assist
🔍 Debugging
📦 Project Tools
🧪 Testing
📊 System Information
📝 Logs


## 📦 APP STORE

DevX OS may provide:

📦 App Store

for supported applications and features.


## 🎮 GAMES

DevX OS includes a gaming-oriented interface:

🎮 Games

The overall interface uses a gaming-inspired visual style.


## 📝 NOTES

DevX OS includes:

📝 Notes

for basic text and note-taking.


## 🧮 CALCULATOR

DevX OS includes:

🧮 Calculator

for basic calculations.


## 🔐 SECURITY

Admin-only functionality must remain protected from Guest users.

Never publish:

❌ Passwords
❌ API Keys
❌ Access Tokens
❌ Private Keys
❌ Keystore Passwords
❌ Personal Credentials


## 🖥️ DESKTOP WINDOW SYSTEM

DevX OS uses a Windows-style virtual desktop.

Windows should support:

🖱️ Drag
↔️ Resize
➖ Minimize
□ Maximize
↩️ Restore
❌ Close

Touch and mouse controls should work where supported.


## 📱 ANDROID COMPATIBILITY

The UI should be responsive for Android devices.

Avoid:

❌ Horizontal overflow
❌ Broken dialogs
❌ Unreachable buttons
❌ Controls outside the screen
❌ Unwanted page scrolling
❌ Frozen windows


## 🏷️ APP INFORMATION

Application Name:

DevX OS

Version:

2.0.1 BETA

Owner:

Abhimanyu Verma

Location:

Near Utkramit Madhya Vidyalay Phuljori (or Pandayd),
Giridih, Jharkhand, India


## ℹ️ ABOUT SECTION

The About section should show:

🎮 DevX OS

Version: 2.0.1 BETA

👤 Owner:
Abhimanyu Verma

📍 Location:
Near Utkramit Madhya Vidyalay Phuljori
(or Pandayd)
Giridih, Jharkhand, India


## 🏗️ RELEASE APK

For a release APK:

Build
→ Generate Signed App Bundle / APK
→ APK

Select or create a signing key.

Choose:

release

Complete the signing wizard.

Keep the keystore and passwords safe.


## 🧹 IF BUILD FAILS

Try:

File
→ Sync Project with Gradle Files

Then:

Build
→ Clean Project

Then:

Build
→ Rebuild Project

If necessary:

File
→ Invalidate Caches / Restart

Then reopen Android Studio.


## 🔍 COMMON PROBLEMS

### Gradle Error

File
→ Sync Project with Gradle Files

### SDK Missing

Tools
→ SDK Manager

Install the required Android SDK version.

### JDK Error

File
→ Settings
→ Build, Execution, Deployment
→ Build Tools
→ Gradle

Select a compatible JDK.

### APK Not Found

Build
→ Build Bundle(s) / APK(s)
→ Build APK(s)

Then select:

Locate


## 📂 PROJECT STRUCTURE

dh/
├── Setup.md
├── README-ANDROID.md
├── build.gradle
├── settings.gradle
├── app/
│   ├── build.gradle
│   └── src/
│       └── main/
│           ├── AndroidManifest.xml
│           ├── assets/
│           └── res/
└── ...


## 🧪 TESTING CHECKLIST

☑️ Boot Screen
☑️ Create Admin
☑️ Login
☑️ Setup Center
☑️ Settings
☑️ Troubleshooting
☑️ App Health
☑️ Guest Mode
☑️ Guest 1-minute timeout
☑️ Reset System
☑️ Code Assist
☑️ AI Features
☑️ File Manager
☑️ Browser
☑️ Terminal
☑️ Notes
☑️ Calculator
☑️ Games
☑️ App Store
☑️ Window Move
☑️ Window Resize
☑️ Minimize
☑️ Maximize
☑️ Restore
☑️ Close
☑️ Android Touch
☑️ Portrait Mode
☑️ Landscape Mode


## 🏷️ GITHUB TAG

Recommended tag:

v2.0.1-beta

GitHub Release Title:

DevX OS 2.0.1 BETA


## 📢 GITHUB RELEASE DESCRIPTION

DevX OS 2.0.1 BETA

🚀 Boot and Setup improvements
⚙️ Settings fixes
🛠️ Troubleshooting improvements
🩺 App Health improvements
👤 Limited Guest Mode
⏱️ 1-minute Guest session
♻️ Reset System
🤖 AI Features
💻 Code Assist
📁 File Manager
🌐 Browser
⌨️ Terminal
🎮 Gaming UI
🖥️ Windows-style virtual desktop
📱 Android responsive interface
🔧 Stability improvements


## ❤️ DEVX OS

DREAM → CODE → CREATE

🎮 DevX OS 2.0.1 BETA

Built with passion. 🚀


## ⚠️ DISCLAIMER

DevX OS is a custom virtual workspace/application project.

Some desktop, AI, system-monitoring, networking, terminal, file-management, or operating-system-like features may depend on Android permissions, device capabilities, configured services, or the implementation of the current build.

Always test the APK before distributing it.

Never publish private credentials, API keys, passwords, tokens or signing keys in GitHub.


Abhimanyu Verma 
