<template>
  <v-container class="fill-height align-start bg-background pa-8">
    <v-row justify="center">
      <v-col cols="12" md="8" lg="6">
        <div class="mb-6">
          <h1 class="text-h4 font-weight-bold text-secondary mb-2">
            Настройки
          </h1>
        </div>

        <v-card class="pa-6 rounded-xl" elevation="0" color="surface">
          <v-form ref="formRef" @submit.prevent="save">
            <section class="mb-8">
              <h2
                class="text-h6 font-weight-bold text-secondary mb-4 pb-2 border-b"
              >
                Оформление
              </h2>
              <div class="d-flex align-center justify-space-between py-2">
                <div class="d-flex flex-column">
                  <span class="text-body-1 font-weight-medium text-secondary"
                    >Темная тема</span
                  >
                  <span class="text-caption text-grey"
                    >Переключение между светлой и темной темой</span
                  >
                </div>
                <v-btn
                  icon
                  variant="tonal"
                  color="primary"
                  @click="toggleTheme"
                  height="48"
                  width="48"
                >
                  <v-icon
                    :icon="isDarkTheme ? mdiWeatherSunny : mdiWeatherNight"
                    size="28"
                    class="transition-swing"
                  ></v-icon>
                </v-btn>
              </div>
            </section>

            <section class="mb-8">
              <h2
                class="text-h6 font-weight-bold text-secondary mb-4 pb-2 border-b"
              >
                Личные данные
              </h2>
              <v-row>
                <v-col cols="12">
                  <p class="text-body-2 font-weight-bold text-secondary mb-2">
                    Никнейм
                  </p>
                  <v-text-field
                    :model-value="userStore.nickname"
                    readonly
                    variant="outlined"
                    rounded="xl"
                    :bg-color="inputBgColor"
                    class="force-opacity"
                    hide-details
                  ></v-text-field>
                </v-col>
                <v-col cols="12">
                  <p class="text-body-2 font-weight-bold text-secondary mb-2">
                    Email
                  </p>
                  <v-text-field
                    v-model="form.email"
                    placeholder="name@example.com"
                    variant="outlined"
                    rounded="xl"
                    :bg-color="inputBgColor"
                    :rules="[rules.email]"
                  ></v-text-field>
                </v-col>
              </v-row>
            </section>

            <section class="mb-8">
              <h2
                class="text-h6 font-weight-bold text-secondary mb-4 pb-2 border-b"
              >
                Финансы
              </h2>
              <v-row>
                <v-col cols="12" md="6">
                  <p class="text-body-2 font-weight-bold text-secondary mb-2">
                    Текущие накопления
                  </p>
                  <v-text-field
                    v-model.number="form.current_savings"
                    type="number"
                    variant="outlined"
                    rounded="xl"
                    :bg-color="inputBgColor"
                    suffix="₽"
                    :rules="[rules.required, rules.positive]"
                    @keydown="blockInvalidNumberChars"
                  ></v-text-field>
                </v-col>
                <v-col cols="12" md="6">
                  <p class="text-body-2 font-weight-bold text-secondary mb-2">
                    Откладываю в месяц
                  </p>
                  <v-text-field
                    v-model.number="form.monthly_savings"
                    type="number"
                    variant="outlined"
                    rounded="xl"
                    :bg-color="inputBgColor"
                    suffix="₽"
                    :rules="[rules.required, rules.positive]"
                    @keydown="blockInvalidNumberChars"
                  ></v-text-field>
                </v-col>
              </v-row>
            </section>

            <section class="mb-8">
              <h2
                class="text-h6 font-weight-bold text-secondary mb-4 pb-2 border-b"
              >
                Контроль категорий
              </h2>
              <v-col cols="12" class="pa-0">
                <p class="text-body-2 font-weight-bold text-secondary mb-2">
                  Запрещенные категории (Red Flags)
                </p>
                <v-combobox
                  v-model="form.forbiddenCategories"
                  :items="userStore.allCategories"
                  chips
                  multiple
                  closable-chips
                  placeholder="Выберите или введите категории"
                  variant="outlined"
                  rounded="xl"
                  :bg-color="inputBgColor"
                  hide-details
                  :menu-icon="mdiChevronDown"
                  color="primary"
                >
                  <template v-slot:item="{ props, item }">
                    <v-list-item
                      v-bind="props"
                      title=""
                      class="clean-list-item"
                    >
                      <template v-slot:prepend>
                        <v-icon
                          :color="
                            form.forbiddenCategories.includes(item.raw)
                              ? 'primary'
                              : 'grey-lighten-1'
                          "
                          :icon="
                            form.forbiddenCategories.includes(item.raw)
                              ? mdiCheckboxMarked
                              : mdiCheckboxBlankOutline
                          "
                          class="mr-2"
                        ></v-icon>
                      </template>

                      <v-list-item-title class="text-body-1 text-high-emphasis">
                        {{ item.raw }}
                      </v-list-item-title>
                    </v-list-item>
                  </template>
                </v-combobox>
              </v-col>
            </section>

            <section class="mb-8">
              <h2
                class="text-h6 font-weight-bold text-secondary mb-4 pb-2 border-b"
              >
                Уведомления и Отчеты
              </h2>
              <div class="d-flex flex-column gap-4">
                <div class="d-flex align-center justify-space-between py-2">
                  <span class="text-body-1 font-weight-medium text-secondary"
                    >Уведомлять об окончании таймера</span
                  >
                  <v-switch
                    v-model="form.notifyOnEnd"
                    color="primary"
                    base-color="grey-darken-2"
                    hide-details
                    inset
                    density="compact"
                  ></v-switch>
                </div>

                <v-divider></v-divider>

                <div class="py-2">
                  <p class="text-body-1 font-weight-medium text-secondary mb-3">
                    Финансовый отчет
                  </p>
                  <v-select
                    v-model="form.reportFrequency"
                    :items="reportOptions"
                    item-title="title"
                    item-value="value"
                    variant="outlined"
                    rounded="xl"
                    :bg-color="inputBgColor"
                    hide-details
                    density="comfortable"
                    color="primary"
                    :menu-icon="mdiChevronDown"
                  ></v-select>
                </div>
              </div>
            </section>

            <div class="d-flex justify-end ga-4 mt-4">
              <v-btn
                variant="text"
                size="large"
                to="/dashboard"
                rounded="xl"
                class="text-secondary"
                >Отмена</v-btn
              >
              <v-btn
                type="submit"
                color="primary"
                size="large"
                :loading="loading"
                elevation="0"
                class="text-on-primary font-weight-bold px-8"
                rounded="xl"
                >Сохранить</v-btn
              >
            </div>
          </v-form>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { useUserStore } from '../stores/user';
import { useNotificationStore } from '../stores/notifications';
import { useRouter } from 'vue-router';
import { rules, blockInvalidNumberChars } from '../utils/validators';
import {
  mdiChevronDown,
  mdiCheckboxMarked,
  mdiCheckboxBlankOutline,
  mdiWeatherSunny,
  mdiWeatherNight,
} from '@mdi/js';

const userStore = useUserStore();
const notifyStore = useNotificationStore();
const router = useRouter();
const loading = ref(false);
const formRef = ref();

const reportOptions = [
  { title: 'Не присылать', value: 'none' },
  { title: 'Ежедневно', value: 'daily' },
  { title: 'Еженедельно', value: 'weekly' },
  { title: 'Ежемесячно', value: 'monthly' },
];

const isDarkTheme = ref(false);

const form = ref({
  email: '',
  current_savings: 0,
  monthly_savings: 0,
  notifyOnEnd: true,
  reportFrequency: 'none',
  forbiddenCategories: [] as string[],
  theme: 'light' as 'light' | 'dark',
});

const inputBgColor = computed(() => {
  return isDarkTheme.value ? 'surface' : 'white';
});

onMounted(() => {
  form.value.current_savings = userStore.current_savings;
  form.value.monthly_savings = userStore.monthly_savings;
  form.value.email = userStore.settings.email;
  form.value.notifyOnEnd = userStore.settings.notifyOnEnd;
  form.value.reportFrequency = userStore.settings.reportFrequency || 'none';
  form.value.forbiddenCategories = [...userStore.settings.forbiddenCategories];

  form.value.theme = userStore.settings.theme;
  isDarkTheme.value = form.value.theme === 'dark';
});

const toggleTheme = () => {
  isDarkTheme.value = !isDarkTheme.value;
  form.value.theme = isDarkTheme.value ? 'dark' : 'light';
  userStore.settings.theme = form.value.theme;
};

const save = async () => {
  const { valid } = await formRef.value.validate();
  if (!valid) return;

  loading.value = true;
  try {
    await userStore.updateProfile({
      current_savings: form.value.current_savings,
      monthly_savings: form.value.monthly_savings,
      notifyOnEnd: form.value.notifyOnEnd,
      reportFrequency: form.value.reportFrequency,
      email: form.value.email,
      forbiddenCategories: form.value.forbiddenCategories,
      theme: form.value.theme,
    });

    notifyStore.notify('Настройки успешно сохранены!', 'success');
    router.push('/dashboard');
  } catch (e) {
    notifyStore.notify('Ошибка при сохранении настроек', 'error');
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.border-b {
  border-bottom: 1px solid rgba(var(--v-border-color), var(--v-border-opacity));
}
.ga-4 {
  gap: 16px;
}
.transition-swing {
  transition: 0.3s cubic-bezier(0.25, 0.8, 0.5, 1);
}
</style>
