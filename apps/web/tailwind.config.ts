import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./src/**/*.{js,ts,jsx,tsx,mdx}"],
  theme: {
    extend: {
      colors: {
        background: "#0b0f14",
        panel: "#111821",
        line: "#233040",
        text: "#e6edf3",
        muted: "#93a4b7",
        accent: "#38bdf8",
        buy: "#22c55e",
        sell: "#ef4444",
        hold: "#f59e0b"
      },
      fontFamily: {
        sans: ["Inter", "ui-sans-serif", "system-ui"]
      }
    }
  },
  plugins: []
};

export default config;
