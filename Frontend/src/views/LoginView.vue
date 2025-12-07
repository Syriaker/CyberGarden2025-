<template>
  <v-container class="fill-height justify-center bg-background">
    <v-card width="400" class="pa-6 rounded-xl" elevation="0" color="surface">
      <div class="d-flex flex-column align-center gap-4 mb-6">
        <img
          src="/logo.svg"
          alt="T-Bank Rational Assistant"
          style="height: 64px; width: auto; object-fit: contain"
          class="mb-2"
        />

        <h1 class="text-h5 font-weight-black text-secondary">
          Добро пожаловать
        </h1>
        <p class="text-body-2 text-secondary text-center">
          Введите ваш никнейм (только латиница и цифры).
        </p>
      </div>

      <v-form ref="form" @submit.prevent="handleLogin">
        <v-text-field
          v-model="nickname"
          label="Ваш Никнейм"
          placeholder="user123"
          variant="outlined"
          rounded="xl"
          :bg-color="inputBgColor"
          :rules="[rules.required, rules.nickname]"
          required
          @keydown.space.prevent
        ></v-text-field>

        <v-btn
          type="submit"
          block
          color="primary"
          size="x-large"
          class="mt-4 text-on-primary font-weight-bold"
          :loading="loading"
        >
          Войти / Зарегистрироваться
        </v-btn>
      </v-form>
    </v-card>
  </v-container>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import { useUserStore } from '../stores/user';
import { useNotificationStore } from '../stores/notifications';
import { rules } from '../utils/validators';

const nickname = ref('');
const loading = ref(false);
const router = useRouter();
const userStore = useUserStore();
const notifyStore = useNotificationStore();
const form = ref();

const isDark = computed(() => userStore.settings.theme === 'dark');
const inputBgColor = computed(() =>
  isDark.value ? 'surface-variant' : 'grey-lighten-4'
);

const handleLogin = async () => {
  const { valid } = await form.value.validate();
  if (!valid) return;

  loading.value = true;
  try {
    const status = await userStore.auth(nickname.value);
    if (status === 'created') {
      router.push('/setup');
      notifyStore.notify('Аккаунт создан! Заполните профиль', 'info');
    } else {
      router.push('/dashboard');
      notifyStore.notify('С возвращением!', 'success');
    }
  } catch (e) {
    notifyStore.notify('Ошибка соединения с сервером', 'error');
  } finally {
    loading.value = false;
  }
};
</script>
