import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import vuetify from 'vite-plugin-vuetify';

export default defineConfig(({ command }) => {
  const isBuild = command === 'build';

  return {
    base: isBuild ? '/static/' : '/',
    plugins: [vue(), vuetify({ autoImport: true })],
    build: {
      cssCodeSplit: false,
      assetsDir: 'assets',
      rollupOptions: {
        output: {
          manualChunks: () => 'main',
          entryFileNames: 'assets/main.js',
          chunkFileNames: 'assets/main.js',
          assetFileNames: (assetInfo) => {
            if (assetInfo.name && assetInfo.name.endsWith('.css')) {
              return 'assets/style.css';
            }
            return 'assets/[name].[ext]';
          },
        },
      },
    },
  };
});
