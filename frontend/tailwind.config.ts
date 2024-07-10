import type { Config } from "tailwindcss";
import {nextui} from "@nextui-org/react";


const config: Config = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./node_modules/@nextui-org/theme/dist/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      backgroundImage: {
        'gradient-to-b-header': 'linear-gradient(to bottom, #495de3 0%, #F7F7F7 100%)',
        "gradient-radial": "radial-gradient(var(--tw-gradient-stops))",
        "gradient-conic":
            "conic-gradient(from 180deg at 50% 50%, var(--tw-gradient-stops))",
        'hero-gradient': "linear-gradient(-40deg, rgba(133, 192, 245, .7) 50%, rgb(62, 176, 125, .9) 50%)",
      },
      backgroundColor: {
        bodyDefault: "#f7f7f7",
      },
      backgroundSize: {
        '100x200': '100% 200px',
      },
      backgroundPosition: {
        'bottom-100': '0% 100%',
      },
      transitionProperty: {
        'position': 'background-position',
      },
      height: {
        'content': 'calc(100vh - 6rem)',
        800:  '50rem'
      },
      width: {
        18: "4.5rem",
        800: '50rem',
      }
    },
  },
  plugins: [nextui()],
};
export default config;
