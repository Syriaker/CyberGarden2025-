<template>
  <v-app :theme="currentTheme">
    <v-app-bar
      v-if="showHeader"
      flat
      color="surface"
      height="80"
      class="border-b px-4"
    >
      <template v-slot:prepend>
        <div
          class="d-flex align-center cursor-pointer logo-container mr-8"
          @click="router.push('/dashboard')"
        >
          <img
            src="/logo.svg"
            alt="T-Bank Rational Assistant"
            class="rounded-lg"
            style="height: 36px; width: 36px; object-fit: cover"
          />
        </div>
      </template>

      <div class="d-none d-md-flex align-center gap-2">
        <v-btn
          to="/dashboard"
          variant="text"
          class="nav-btn text-body-2 font-weight-bold"
          rounded="xl"
          height="44"
        >
          <v-icon :icon="mdiHeartOutline" class="mr-2"></v-icon>
          Желаемое
        </v-btn>

        <v-btn
          to="/history"
          variant="text"
          class="nav-btn text-body-2 font-weight-bold"
          rounded="xl"
          height="44"
        >
          <v-icon :icon="mdiHistory" class="mr-2"></v-icon>
          История
        </v-btn>

        <v-btn
          to="/settings"
          variant="text"
          class="nav-btn text-body-2 font-weight-bold"
          rounded="xl"
          height="44"
        >
          <v-icon :icon="mdiCogOutline" class="mr-2"></v-icon>
          Настройки
        </v-btn>
      </div>

      <v-spacer></v-spacer>

      <div class="d-flex d-md-none">
        <v-btn icon to="/dashboard" color="secondary">
          <v-icon :icon="mdiHeartOutline"></v-icon>
        </v-btn>
        <v-btn icon to="/history" color="secondary">
          <v-icon :icon="mdiHistory"></v-icon>
        </v-btn>
        <v-btn icon to="/settings" color="secondary">
          <v-icon :icon="mdiCogOutline"></v-icon>
        </v-btn>
      </div>

      <v-divider vertical inset class="mx-4 hidden-xs"></v-divider>

      <v-btn
        @click="handleLogout"
        variant="text"
        color="grey-darken-1"
        rounded="xl"
        class="text-caption font-weight-bold px-4"
      >
        <v-icon :icon="mdiLogout" class="mr-1"></v-icon>
        <span class="hidden-xs">Выйти</span>
      </v-btn>
    </v-app-bar>

    <v-main class="bg-background">
      <router-view />
    </v-main>

    <v-snackbar
      v-model="notifyStore.show"
      :color="notifyStore.color"
      :timeout="notifyStore.timeout"
      location="bottom right"
      rounded="xl"
      elevation="4"
    >
      <div class="d-flex align-center gap-2">
        <v-icon
          v-if="notifyStore.color === 'error'"
          :icon="mdiAlertCircle"
          color="white"
        ></v-icon>
        <v-icon v-else :icon="mdiCheckCircle" color="white"></v-icon>
        <span class="text-white font-weight-medium">{{
          notifyStore.message
        }}</span>
      </div>
    </v-snackbar>
  </v-app>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useUserStore } from './stores/user';
import { useNotificationStore } from './stores/notifications';
import { useRouter, useRoute } from 'vue-router';

import {
  mdiHeartOutline,
  mdiCogOutline,
  mdiLogout,
  mdiAlertCircle,
  mdiCheckCircle,
  mdiHistory,
} from '@mdi/js';

const userStore = useUserStore();
const notifyStore = useNotificationStore();
const router = useRouter();
const route = useRoute();

const currentTheme = computed(() => {
  return userStore.settings.theme === 'dark' ? 'tbankDarkTheme' : 'tbankTheme';
});

const showHeader = computed(() => {
  return route.name !== 'Login' && route.name !== 'Setup';
});

const handleLogout = () => {
  userStore.logout();
  router.push('/login');
  notifyStore.notify('Вы вышли из системы', 'info');
};
</script>

<style>
.border-b {
  border-bottom: 1px solid rgba(var(--v-border-color), var(--v-border-opacity));
}

.logo-container {
  transition: opacity 0.2s ease;
}
.logo-container:hover {
  opacity: 0.8;
}
</style>
