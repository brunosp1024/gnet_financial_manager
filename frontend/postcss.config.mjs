// Garante que o CSS gerado pelo Tailwind seja processado corretamente e funcione em todos os navegadores modernos

/** @type {import('postcss-load-config').Config} */
const config = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
};

export default config;
