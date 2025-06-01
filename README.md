# 🌍 Deka Website

> **The marketing website for Deka - One API to rule them all**

[![Next.js](https://img.shields.io/badge/Next.js-15.3.3-black?style=flat-square&logo=next.js)](https://nextjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0-blue?style=flat-square&logo=typescript)](https://www.typescriptlang.org/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind-4.0-38B2AC?style=flat-square&logo=tailwind-css)](https://tailwindcss.com/)
[![Framer Motion](https://img.shields.io/badge/Framer_Motion-12.15-FF0055?style=flat-square&logo=framer)](https://www.framer.com/motion/)

**Deka** is an open-source translation API aggregator that provides a unified interface to multiple translation providers including Google Translate, DeepL, and specialized African language providers like Lelapa AI and Khaya AI.

This repository contains the **marketing website** built with Next.js, showcasing Deka&apos;s features and vision.

---

## 🚀 **What is Deka?**

Deka solves the complexity of working with multiple translation APIs by providing:

- **🔗 One API, Many Providers** - Access Google, DeepL, and African language providers through a single endpoint
- **💰 Fair Pricing** - Transparent pricing model: provider cost + 10%, no hidden fees
- **🌍 Under-resourced Languages** - First-class support for African and other underserved languages
- **📖 Open Source** - Community-driven, transparent development

---

## 🏗️ **Project Structure**

```
deka-website/
├── deka-web-nextjs/          # Next.js website application
│   ├── app/                  # App router pages
│   ├── components/           # Reusable React components
│   │   ├── hero/            # Hero section variants
│   │   ├── sections/        # Page sections (Features, WhyDeka, etc.)
│   │   └── ui/              # shadcn/ui components
│   ├── lib/                 # Utility functions
│   └── public/              # Static assets
├── LICENSE                  # Apache 2 License
└── README.md               # This file
```

---

## 🛠️ **Tech Stack**

- **Framework**: [Next.js 15.3.3](https://nextjs.org/) with App Router
- **Language**: [TypeScript 5.0](https://www.typescriptlang.org/)
- **Styling**: [Tailwind CSS 4.0](https://tailwindcss.com/)
- **Animations**: [Framer Motion 12.15](https://www.framer.com/motion/)
- **UI Components**: [shadcn/ui](https://ui.shadcn.com/) with [Radix UI](https://www.radix-ui.com/)
- **Icons**: [Lucide React](https://lucide.dev/)
- **Deployment**: [Vercel](https://vercel.com/) (recommended)

---

## 🚀 **Quick Start**

### Prerequisites

- Node.js 18+
- npm, yarn, or pnpm

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/deka-website.git
   cd deka-website/deka-web-nextjs
   ```

2. **Install dependencies**
   ```bash
   npm install
   # or
   yarn install
   # or
   pnpm install
   ```

3. **Start the development server**
   ```bash
   npm run dev
   # or
   yarn dev
   # or
   pnpm dev
   ```

4. **Open your browser**

   Navigate to [http://localhost:3000](http://localhost:3000) to see the website.

---

## 📝 **Available Scripts**

| Script | Description |
|--------|-------------|
| `npm run dev` | Start development server with Turbopack |
| `npm run build` | Build the application for production |
| `npm run start` | Start the production server |
| `npm run lint` | Run ESLint for code quality checks |

---

## 🎨 **Design System**

The website follows a clean **black and white** design philosophy:

- **Colors**: Primarily grayscale with black accents
- **Typography**: Clean, readable fonts with clear hierarchy
- **Components**: Modular, reusable components with consistent styling
- **Animations**: Smooth, purposeful animations using Framer Motion
- **Responsive**: Mobile-first design that works on all devices

### Key Components

- **Hero Section**: Interactive flow diagram showing translation process
- **Why Deka**: Tabbed interface explaining core benefits
- **What We&apos;re Building**: Honest roadmap of features in development
- **CTA Section**: Clear call-to-action for early access

---

## 🔗 **Related Repositories**

| Repository | Description | Status |
|------------|-------------|---------|
| **[deka-api](https://github.com/yourusername/deka-api)** | FastAPI backend server | 🚧 In Development |
| **[deka-docs](https://github.com/yourusername/deka-docs)** | API documentation | 📋 Planned |
| **[deka-sdk](https://github.com/yourusername/deka-sdk)** | Client SDKs | 📋 Planned |

---

## 🤝 **Contributing**

We welcome contributions! Here&apos;s how you can help:

### Website Improvements

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes**: Improve design, fix bugs, add features
4. **Commit your changes**: `git commit -m 'Add amazing feature'`
5. **Push to the branch**: `git push origin feature/amazing-feature`
6. **Open a Pull Request**

### Areas for Contribution

- 🎨 **Design improvements** - Better animations, responsive design
- 🌐 **Internationalization** - Multi-language support for the website
- ♿ **Accessibility** - Improve screen reader support, keyboard navigation
- 📱 **Mobile experience** - Enhanced mobile interactions
- 🐛 **Bug fixes** - Fix any issues you find

---

## 📄 **License**

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 🌟 **Support the Project**

If you find Deka useful, please consider:

- ⭐ **Starring this repository**
- 🐛 **Reporting bugs** via [Issues](https://github.com/yourusername/deka-website/issues)
- 💡 **Suggesting features** via [Discussions](https://github.com/yourusername/deka-website/discussions)
- 🤝 **Contributing code** via Pull Requests

---

## 📞 **Contact & Community**

- **Website**: [deka.dev](https://deka.dev) *(coming soon)*
- **API Docs**: [docs.deka.dev](https://docs.deka.dev) *(coming soon)*
- **GitHub**: [@yourusername](https://github.com/yourusername)
- **Twitter**: [@deka_dev](https://twitter.com/deka_dev) *(coming soon)*

---

<div align="center">

**Built with ❤️ for the developer community**

*Making translation APIs simple, fair, and accessible to everyone*

[⭐ Star on GitHub](https://github.com/yourusername/deka-website) • [🚀 Try the API](https://github.com/yourusername/deka-api) • [📖 Read the Docs](https://docs.deka.dev)

</div>