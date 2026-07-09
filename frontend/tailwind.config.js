/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        // "Trail map" palette — signature: routes/waypoints, not generic SaaS blue.
        ink: "#14192B",        // near-black navy, primary text/bg in dark mode
        parchment: "#F7F3E9",  // warm map-paper background (light mode)
        trail: "#2F6F5E",      // deep pine — primary brand color (the "path" color)
        trailLight: "#4C8C79",
        waypoint: "#E0A845",   // ochre/gold — waypoints, XP, achievements
        summit: "#C1502E",     // clay red — alerts, deadlines, streaks-at-risk
        slate: "#5B6472",
        mist: "#DDE3E0",
      },
      fontFamily: {
        display: ["'Fraunces'", "serif"],
        body: ["'Inter'", "sans-serif"],
        mono: ["'IBM Plex Mono'", "monospace"],
      },
      backgroundImage: {
        "contour": "radial-gradient(circle at 1px 1px, rgba(20,25,43,0.06) 1px, transparent 0)",
      },
    },
  },
  plugins: [],
};
