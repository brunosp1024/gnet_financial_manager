import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: "class",
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          blue:     "#1565c0",
          "blue-d": "#0d47a1",
          "blue-l": "#1976d2",
          red:      "#d32f2f",
          "red-d":  "#b71c1c",
          "red-l":  "#ef5350",
        },
      },
      fontFamily: {
        display: ["'Playpen Sans Thai'", "cursive"],
        body:    ["'DM Sans'", "sans-serif"],
      },
    },
  },
  plugins: [],
};

export default config;
