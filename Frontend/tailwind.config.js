/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
    './node_modules/flowbite/**/*.js',
    './src/pages/**/*.{html,js}'
  ],
  
  theme: {
    extend: {
      backgroundImage: {
        // Undefined
      }
    },
  },
  plugins: [
    require('flowbite/plugin')
  ],
  theme: {
    screens: {
      'sm': '640px',
      // => @media (min-width: 640px) { ... }

      'md': '972px',
      // => @media (min-width: 768px) { ... }

      'lg': '1020px',
      // => @media (min-width: 1024px) { ... }

      'xl': '1280px',
      // => @media (min-width: 1280px) { ... }

      '2xl': '1536px',
      // => @media (min-width: 1536px) { ... }
    }
  }
}

