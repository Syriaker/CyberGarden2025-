<template>
  <v-container class="fill-height justify-center bg-background">
    <v-card width="600" class="pa-8 rounded-xl" elevation="0" color="surface">
      <div class="mb-6">
        <h1 class="text-h4 font-weight-black text-secondary mb-2">
          Финансовый профиль
        </h1>
        <p class="text-body-1 text-secondary">
          Укажите ваши базовые показатели (строго положительные числа).
        </p>
      </div>

      <v-form ref="formRef" @submit.prevent="save">
        <v-row>
          <v-col cols="12">
            <p class="text-body-2 font-weight-bold text-secondary mb-2">
              Текущие накопления (₽)
            </p>
            <v-text-field
              v-model.number="form.current_savings"
              placeholder="0"
              type="number"
              min="0"
              variant="outlined"
              rounded="xl"
              :bg-color="inputBgColor"
              :rules="[rules.required, rules.positive]"
              @keydown="blockInvalidNumberChars"
            ></v-text-field>
          </v-col>

          <v-col cols="12" md="6">
            <p class="text-body-2 font-weight-bold text-secondary mb-2">
              Откладываю в месяц (₽)
            </p>
            <v-text-field
              v-model.number="form.monthly_savings"
              placeholder="0"
              type="number"
              min="0"
              variant="outlined"
              rounded="xl"
              :bg-color="inputBgColor"
              :rules="[rules.required, rules.positive]"
              @keydown="blockInvalidNumberChars"
            ></v-text-field>
          </v-col>

          <v-col cols="12" md="6">
            <p class="text-body-2 font-weight-bold text-secondary mb-2">
              Обязательные траты (₽)
            </p>
            <v-text-field
              v-model.number="form.monthly_spendings"
              placeholder="0"
              type="number"
              min="0"
              variant="outlined"
              rounded="xl"
              :bg-color="inputBgColor"
              :rules="[rules.required, rules.positive]"
              @keydown="blockInvalidNumberChars"
            ></v-text-field>
          </v-col>
        </v-row>

        <div class="mt-8 d-flex justify-end">
          <v-btn
            type="submit"
            color="primary"
            size="x-large"
            class="px-8 text-on-primary font-weight-bold"
            :loading="loading"
          >
            Сохранить
          </v-btn>
        </div>
      </v-form>
    </v-card>
  </v-container>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { useUserStore } from '../stores/user';
import { useNotificationStore } from '../stores/notifications';
import { useRouter } from 'vue-router';
import { rules, blockInvalidNumberChars } from '../utils/validators';

const userStore = useUserStore();
const notifyStore = useNotificationStore();
const router = useRouter();
const loading = ref(false);
const formRef = ref();

const form = ref({
  current_savings: 0,
  monthly_savings: 0,
  monthly_spendings: 0,
});

const isDark = computed(() => userStore.settings.theme === 'dark');
const inputBgColor = computed(() =>
  isDark.value ? 'surface-variant' : 'grey-lighten-4'
);

onMounted(() => {
  form.value.current_savings = userStore.current_savings;
  form.value.monthly_savings = userStore.monthly_savings;
  form.value.monthly_spendings = userStore.monthly_spendings;
});

const save = async () => {
  const { valid } = await formRef.value.validate();
  if (!valid) return;

  loading.value = true;
  try {
    await userStore.updateProfile(form.value);
    router.push('/dashboard');
    notifyStore.notify('Профиль сохранен', 'success');
  } catch (e) {
    notifyStore.notify('Ошибка сохранения', 'error');
  } finally {
    loading.value = false;
  }
};
</script>
