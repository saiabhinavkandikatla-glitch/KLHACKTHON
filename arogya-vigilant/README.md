# Arogya Vigilant 🏥🛡️

**AI-Powered Fraud Intelligence & Risk Scoring Dashboard for the Ayushman Bharat Ecosystem.**

Arogya Vigilant is a strict, production-grade web application designed for government authorities to monitor, detect, and investigate fraudulent billing patterns and anomalies in healthcare claims.

---

## 💻 Technology Stack

### Core Architecture
*   **React 18** - Component-driven UI library for building the interactive dashboard.
*   **Vite** - Next-generation frontend tooling for instantaneous HMR (Hot Module Replacement) and optimized production builds.
*   **TypeScript** - Strict static typing to ensure enterprise-level code reliability and maintainability.

### Styling & UI Framework
*   **Tailwind CSS (v3)** - Utility-first CSS framework used for developing the custom "Government-Grade" design system.
    *   *Custom Theme*: Deep Healthcare Blue (`#0F2C59`), Teal (`#008080`), and Muted Red (`#B91C1C`).
*   **Lucide React** - Clean, modern, and consistent SVG iconography suite used throughout the platform.

### Data Visualization
*   **Recharts** - Composable, reliable charting library built on React components used for rendering the Claim Analytics volume trends and Regional Risk Distribution.
*   **Custom Scatter Plots** - Used for visualizing mathematical Isolation Forest algorithm outputs intuitively for auditors.

### Simulated Machine Learning Pipeline (Frontend)
*This React application simulates a strict backend pipeline within the browser for demonstration purposes:*
*   **Isolation Forest Anomaly Simulation**: Mathematical simulation representing unsupervised learning over standardized claim features.
*   **CNN/ResNet Simulation**: Simulates an image validation pipeline verifying medical X-Rays via perceptual hashing and confidence thresholding (Strictly >80%).

---

## 🚀 Features

1.  **Strict Image Validation Pipeline**: 
    - Hard-rejects non-PDF files immediately.
    - Simulates extracting Phase 1 scans, performing grayscale conversions, and checking against a ResNet model for X-ray verification.
2.  **Unified Risk Index**: 
    - Merges isolated anomaly signals into a single trustworthy metric: `(0.7 × Isolation Forest) + (0.3 × Image Duplication)`.
3.  **High-Risk Provider Matrix**: 
    - Tabular ranking of hospital networks displaying only strict Provider IDs and their calculated Risk Vectors.
4.  **Claim Analytics Trends**: 
    - Area and Bar charts displaying adjudication volumes vs. flagged metrics.
5.  **Professional Government Aesthetic**: 
    - Clean, accessible, minimal UI optimized for desktop auditing, dropping all "gamified" or flashy elements in favor of raw data visibility.

---

## 🛠️ Getting Started (Local Development)

### Prerequisites
*   Node.js (v18+ recommended)
*   npm or yarn

### Installation
1. Clone the repository and navigate to the project directory:
   ```bash
   cd arogya-vigilant
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

4. Open your browser and navigate to `http://localhost:5173/`
