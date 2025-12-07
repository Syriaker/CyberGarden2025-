<template>
  <v-container
    fluid
    class="bg-background pa-6 pa-md-8"
    style="max-width: 1600px"
  >
    <v-row>
      <v-col cols="12" md="3" lg="3">
        <v-card class="rounded-xl pa-6" elevation="0" color="surface">
          <div class="d-flex align-center flex-column text-center mb-6">
            <v-avatar size="80" color="primary" class="mb-4 elevation-2">
              <span class="text-h3 font-weight-bold text-on-primary">
                {{
                  userStore.nickname
                    ? userStore.nickname.charAt(0).toUpperCase()
                    : 'U'
                }}
              </span>
            </v-avatar>
            <h2 class="text-h6 font-weight-black text-secondary">
              {{ userStore.nickname }}
            </h2>
          </div>
          <v-divider class="mb-6"></v-divider>
          <div class="d-flex flex-column gap-4">
            <div class="d-flex align-center justify-space-between">
              <div class="d-flex align-center gap-3">
                <v-avatar color="green-lighten-5" size="40" rounded="lg">
                  <v-icon :icon="mdiCashMultiple" color="success"></v-icon>
                </v-avatar>
                <div>
                  <div class="text-caption text-secondary font-weight-bold">
                    Накопления
                  </div>
                  <div class="text-body-2 font-weight-black text-secondary">
                    {{ userStore.current_savings.toLocaleString() }} ₽
                  </div>
                </div>
              </div>
            </div>
            <div class="d-flex align-center justify-space-between">
              <div class="d-flex align-center gap-3">
                <v-avatar color="blue-lighten-5" size="40" rounded="lg">
                  <v-icon :icon="mdiCalendarRefresh" color="info"></v-icon>
                </v-avatar>
                <div>
                  <div class="text-caption text-secondary font-weight-bold">
                    Откладываю/мес
                  </div>
                  <div class="text-body-2 font-weight-black text-secondary">
                    {{ userStore.monthly_savings.toLocaleString() }} ₽
                  </div>
                </div>
              </div>
            </div>
          </div>
          <v-sheet
            class="mt-6 pa-4 rounded-xl d-flex flex-column align-center text-center border-dashed"
            color="transparent"
            style="border: 2px dashed rgba(var(--v-theme-primary), 1)"
          >
            <span
              class="text-caption text-secondary font-weight-bold text-uppercase ls-1"
            >
              Свободный бюджет
            </span>
            <span class="text-h4 font-weight-black text-primary mt-1">
              {{ userStore.freeBudget.toLocaleString() }} ₽
            </span>
          </v-sheet>
        </v-card>
      </v-col>

      <v-col cols="12" md="6" lg="6">
        <div class="d-flex align-center justify-space-between mb-6">
          <h1 class="text-h5 font-weight-black text-secondary">
            Мои желания
            <span class="text-body-1 ml-2 text-secondary"
              >({{ itemsStore.activeItems.length }})</span
            >
          </h1>
        </div>

        <div v-if="itemsStore.loading" class="d-flex justify-center py-12">
          <v-progress-circular
            indeterminate
            color="primary"
            size="64"
          ></v-progress-circular>
        </div>

        <div
          v-else-if="itemsStore.activeItems.length === 0"
          class="d-flex flex-column align-center justify-center py-12 text-center"
        >
          <v-sheet
            color="surface"
            height="160"
            width="160"
            class="rounded-circle d-flex align-center justify-center mb-6 elevation-1"
          >
            <v-icon :icon="mdiBasketOutline" size="80" color="primary"></v-icon>
          </v-sheet>
          <h3 class="text-h6 font-weight-bold text-secondary mb-2">
            Список пока пуст
          </h3>
          <p class="text-body-1 text-secondary" style="max-width: 400px">
            Добавьте свою первую "хотелку" справа.
          </p>
        </div>

        <v-row v-else>
          <v-col
            cols="12"
            v-for="item in itemsStore.activeItems"
            :key="item.id"
          >
            <v-card
              class="rounded-xl overflow-hidden transition-swing"
              elevation="0"
              color="surface"
            >
              <div class="d-flex flex-column flex-sm-row">
                <div
                  class="flex-shrink-0 position-relative"
                  style="width: 100%; max-width: 200px"
                >
                  <v-img
                    v-if="item.image_url"
                    :src="item.image_url"
                    height="180"
                    cover
                    class="bg-grey-lighten-2"
                  ></v-img>
                  <v-sheet
                    v-else
                    :color="isDark ? 'surface-variant' : 'grey-lighten-3'"
                    height="180"
                    class="d-flex align-center justify-center"
                  >
                    <v-icon
                      :icon="getCategoryIcon(item.category)"
                      size="64"
                      color="grey"
                    ></v-icon>
                  </v-sheet>
                  <v-chip
                    class="position-absolute bottom-0 left-0 ma-3 font-weight-bold bg-surface text-secondary"
                    size="small"
                    variant="flat"
                  >
                    {{ item.price.toLocaleString() }} ₽
                  </v-chip>
                </div>

                <div class="pa-5 d-flex flex-column flex-grow-1">
                  <div class="d-flex justify-space-between align-start mb-2">
                    <div>
                      <div class="d-flex align-center gap-2 mb-1">
                        <v-chip
                          size="x-small"
                          :color="
                            userStore.settings.forbiddenCategories.includes(
                              item.category
                            )
                              ? 'error'
                              : 'grey-darken-1'
                          "
                          variant="tonal"
                          class="font-weight-bold"
                        >
                          {{ item.category }}
                        </v-chip>
                        <v-btn
                          v-if="item.link_url"
                          icon
                          variant="text"
                          density="compact"
                          size="x-small"
                          color="primary"
                          :href="item.link_url"
                          target="_blank"
                        >
                          <v-icon :icon="mdiLink" size="16"></v-icon>
                        </v-btn>
                      </div>
                      <h3
                        class="text-h6 font-weight-bold text-secondary text-truncate"
                        style="max-width: 300px"
                      >
                        {{ item.title }}
                      </h3>
                    </div>
                    <v-chip
                      :color="item.days_left <= 0 ? 'success' : 'warning'"
                      variant="flat"
                      class="font-weight-bold"
                      :prepend-icon="
                        item.days_left <= 0 ? mdiCheckDecagram : mdiTimerSand
                      "
                    >
                      {{
                        item.days_left <= 0 ? 'Готово' : `${item.days_left} дн.`
                      }}
                    </v-chip>
                  </div>

                  <div class="mt-4 mb-4">
                    <div
                      class="d-flex justify-space-between text-caption font-weight-bold mb-1"
                    >
                      <span
                        :class="
                          item.days_left <= 0
                            ? 'text-success'
                            : 'text-secondary'
                        "
                      >
                        {{
                          item.days_left <= 0
                            ? 'Охлаждение завершено!'
                            : 'Период ожидания'
                        }}
                      </span>
                      <span class="text-secondary"
                        >{{ Math.round(calculateProgress(item)) }}%</span
                      >
                    </div>
                    <v-progress-linear
                      :model-value="calculateProgress(item)"
                      :color="item.days_left <= 0 ? 'success' : 'primary'"
                      height="8"
                      rounded
                      :bg-color="isDark ? 'grey-darken-2' : 'grey-lighten-2'"
                      striped
                      :active="true"
                    ></v-progress-linear>
                  </div>

                  <div class="mt-auto d-flex gap-3">
                    <v-btn
                      variant="text"
                      color="error"
                      class="flex-grow-1"
                      rounded="xl"
                      height="40"
                      :prepend-icon="mdiClose"
                      @click="itemsStore.cancelItem(item.id)"
                    >
                      Не нужно
                    </v-btn>
                    <v-btn
                      variant="flat"
                      color="success"
                      class="flex-grow-1 text-white font-weight-bold"
                      rounded="xl"
                      height="40"
                      :prepend-icon="mdiCartCheck"
                      @click="itemsStore.markAsBought(item.id)"
                      :disabled="item.days_left > 0"
                    >
                      Купить
                    </v-btn>
                  </div>
                </div>
              </div>
            </v-card>
          </v-col>
        </v-row>
      </v-col>

      <v-col cols="12" md="3" lg="3">
        <div class="position-sticky" style="top: 80px">
          <v-card
            class="pa-6 rounded-xl form-card"
            elevation="0"
            color="surface"
          >
            <div class="d-flex align-center gap-2 mb-6">
              <v-icon :icon="mdiPlusCircle" color="primary" size="28"></v-icon>
              <h3 class="text-h6 font-weight-bold text-secondary">
                Новая цель
              </h3>
            </div>

            <v-tabs
              v-model="tab"
              color="primary"
              align-tabs="center"
              :class="['mb-6 rounded-xl', tabsBgColor]"
              density="compact"
              height="40"
              hide-slider
              :selected-class="activeTabClass"
            >
              <v-tab
                value="manual"
                class="rounded-xl w-50 font-weight-bold text-capitalize"
                style="z-index: 1"
                >Вручную</v-tab
              >
              <v-tab
                value="link"
                class="rounded-xl w-50 font-weight-bold text-capitalize"
                style="z-index: 1"
                >По ссылке</v-tab
              >
            </v-tabs>

            <v-window v-model="tab">
              <v-window-item value="link">
                <v-text-field
                  v-model="newItem.link"
                  placeholder="Вставьте ссылку..."
                  variant="outlined"
                  :bg-color="inputBgColor"
                  rounded="xl"
                  :prepend-inner-icon="mdiLink"
                  color="primary"
                  hide-details
                  class="mb-4"
                ></v-text-field>
                <div class="rational-tip-box mb-4">
                  <v-icon :icon="mdiAutoFix" size="20" class="mb-1"></v-icon>
                  <p>Мы сами найдем название, цену и категорию.</p>
                </div>
                <v-btn
                  block
                  color="primary"
                  variant="flat"
                  rounded="xl"
                  class="text-on-primary font-weight-bold"
                  height="48"
                  @click="simulateParsing"
                  :loading="adding"
                  >Распознать</v-btn
                >
              </v-window-item>

              <v-window-item value="manual">
                <v-form ref="form" @submit.prevent="handleAddItem">
                  <div class="d-flex flex-column gap-4">
                    <div v-if="newItem.image_url" class="mb-2">
                      <v-img
                        :src="newItem.image_url"
                        height="120"
                        class="rounded-lg bg-grey-lighten-2"
                        cover
                      ></v-img>
                    </div>

                    <div>
                      <span
                        class="text-caption font-weight-bold text-secondary ml-1"
                        >Что покупаем?</span
                      >
                      <v-text-field
                        v-model="newItem.title"
                        placeholder="Например: PS5"
                        variant="outlined"
                        :bg-color="inputBgColor"
                        rounded="xl"
                        hide-details="auto"
                        color="primary"
                        density="comfortable"
                        :rules="[rules.required]"
                      ></v-text-field>
                    </div>

                    <div>
                      <span
                        class="text-caption font-weight-bold text-secondary ml-1"
                        >Цена</span
                      >
                      <v-text-field
                        v-model.number="newItem.price"
                        placeholder="0"
                        type="number"
                        variant="outlined"
                        :bg-color="inputBgColor"
                        rounded="xl"
                        hide-details="auto"
                        color="primary"
                        density="comfortable"
                        suffix="₽"
                        :rules="[rules.required, rules.positive]"
                        @keydown="blockInvalidNumberChars"
                      ></v-text-field>
                    </div>

                    <div>
                      <span
                        class="text-caption font-weight-bold text-secondary ml-1"
                        >Категория</span
                      >
                      <v-combobox
                        v-model="newItem.category"
                        :items="userStore.allCategories"
                        variant="outlined"
                        :bg-color="inputBgColor"
                        rounded="xl"
                        density="comfortable"
                        hide-details
                        color="primary"
                        :menu-icon="mdiChevronDown"
                        placeholder="Выберите или введите свою"
                        :return-object="false"
                      ></v-combobox>
                    </div>

                    <div class="pt-2">
                      <div
                        class="d-flex align-center justify-space-between mb-2"
                      >
                        <span
                          class="text-caption font-weight-bold text-secondary ml-1"
                        >
                          Период охлаждения
                        </span>

                        <div class="d-flex align-center">
                          <span
                            class="text-caption font-weight-bold text-secondary mr-2"
                            style="
                              min-width: 100px;
                              text-align: right;
                              transition: opacity 0.2s;
                            "
                          >
                            {{ isAutoCooling ? 'Автоматически' : 'Вручную' }}
                          </span>

                          <v-switch
                            v-model="isAutoCooling"
                            color="primary"
                            density="compact"
                            hide-details
                            inset
                            class="mt-0"
                          ></v-switch>
                        </div>
                      </div>

                      <v-expand-transition>
                        <div v-if="!isAutoCooling">
                          <v-text-field
                            v-model.number="newItem.manualDays"
                            placeholder="Количество дней"
                            type="number"
                            min="1"
                            variant="outlined"
                            :bg-color="inputBgColor"
                            rounded="xl"
                            hide-details="auto"
                            color="primary"
                            density="comfortable"
                            suffix="дн."
                            :rules="[rules.required, rules.positive, (v: any) => (v && v >= 1) || 'Минимум 1 день']"
                            @keydown="blockInvalidNumberChars"
                          ></v-text-field>
                        </div>
                        <div
                          v-else
                          class="text-caption text-grey-darken-1 ml-1"
                        >
                          Рассчитаем срок на основе ваших доходов и цены товара.
                        </div>
                      </v-expand-transition>
                    </div>
                  </div>

                  <v-btn
                    block
                    color="primary"
                    size="large"
                    class="text-on-primary font-weight-bold mt-6"
                    rounded="xl"
                    elevation="2"
                    :loading="adding"
                    @click="handleAddItem"
                  >
                    <v-icon :icon="mdiTimerPlayOutline" class="mr-2"></v-icon>
                    Запустить таймер
                  </v-btn>
                </v-form>
              </v-window-item>
            </v-window>
          </v-card>
        </div>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { useUserStore } from '../stores/user';
import { useItemsStore } from '../stores/items';
import { useNotificationStore } from '../stores/notifications';
import { rules, blockInvalidNumberChars } from '../utils/validators';

import {
  mdiBasketOutline,
  mdiImageFilterHdr,
  mdiLink,
  mdiChevronDown,
  mdiClose,
  mdiCartCheck,
  mdiCashMultiple,
  mdiCalendarRefresh,
  mdiPlusCircle,
  mdiAutoFix,
  mdiTimerPlayOutline,
  mdiCheckDecagram,
  mdiTimerSand,
  mdiCellphone,
  mdiTshirtCrew,
  mdiGamepadVariant,
  mdiHome,
} from '@mdi/js';

const userStore = useUserStore();
const itemsStore = useItemsStore();
const notifyStore = useNotificationStore();
const tab = ref('manual');
const adding = ref(false);
const form = ref();

const isAutoCooling = ref(true);

const newItem = ref({
  title: '',
  price: null as number | null,
  category: null as string | null,
  link: '',
  image_url: '',
  manualDays: null as number | null,
});

const isDark = computed(() => userStore.settings.theme === 'dark');
const tabsBgColor = computed(() =>
  isDark.value ? 'bg-grey-darken-4' : 'bg-grey-lighten-3'
);
const activeTabClass = computed(() =>
  isDark.value
    ? 'bg-grey-darken-3 elevation-1 text-primary'
    : 'bg-white elevation-1 text-primary'
);
const inputBgColor = computed(() =>
  isDark.value ? 'surface-variant' : 'grey-lighten-4'
);

onMounted(() => {
  userStore.fetchProfile();
  itemsStore.fetchItems();
});

const simulateParsing = async () => {
  if (!newItem.value.link) {
    notifyStore.notify('Введите ссылку', 'error');
    return;
  }
  adding.value = true;
  try {
    const data = await itemsStore.parseItem(newItem.value.link);
    tab.value = 'manual';
    newItem.value.title = data.title;
    newItem.value.price = Number(data.price);
    newItem.value.category = data.category || 'Другое';
    if (data.image_url) {
      newItem.value.image_url = data.image_url;
    }
    notifyStore.notify('Товар распознан!', 'success');
  } catch (e) {
    console.error(e);
    notifyStore.notify(
      'Не удалось распознать ссылку. Заполните вручную.',
      'error'
    );
    tab.value = 'manual';
  } finally {
    adding.value = false;
  }
};

const calculateProgress = (item: any) => {
  if (item.days_left <= 0) return 100;

  const start = new Date(item.created_at).getTime();
  const end = new Date(item.cooling_end_date).getTime();
  const now = Date.now();

  const totalDuration = end - start;

  if (totalDuration <= 0) return 100;

  const elapsed = now - start;

  const percentage = (elapsed / totalDuration) * 100;

  return Math.max(0, Math.min(100, percentage));
};

const getCategoryIcon = (category: string) => {
  if (category.includes('Смартфон') || category.includes('Электроника'))
    return mdiCellphone;
  if (category.includes('Одежда')) return mdiTshirtCrew;
  if (category.includes('Игры')) return mdiGamepadVariant;
  if (category.includes('Дом')) return mdiHome;
  return mdiImageFilterHdr;
};

const handleAddItem = async () => {
  if (form.value) {
    const { valid } = await form.value.validate();
    if (!valid) {
      notifyStore.notify('Заполните поля корректно', 'error');
      return;
    }
  }

  if (
    !isAutoCooling.value &&
    (!newItem.value.manualDays || newItem.value.manualDays <= 0)
  ) {
    notifyStore.notify('Укажите корректное количество дней', 'error');
    return;
  }

  if (newItem.value.category) {
    userStore.addCustomCategory(newItem.value.category);
  }

  adding.value = true;
  try {
    await itemsStore.addItem({
      title: newItem.value.title || 'Товар по ссылке',
      price: newItem.value.price || 0,
      category: newItem.value.category || 'Другое',
      link: newItem.value.link,
      image_url: newItem.value.image_url,
      manual_days: !isAutoCooling.value ? newItem.value.manualDays : null,
    });

    newItem.value = {
      title: '',
      price: null,
      category: null,
      link: '',
      image_url: '',
      manualDays: null,
    };
    isAutoCooling.value = true;

    if (form.value) form.value.resetValidation();
    notifyStore.notify('Желание добавлено!', 'success');
  } catch (e) {
    console.error(e);
    notifyStore.notify('Ошибка при добавлении', 'error');
  } finally {
    adding.value = false;
  }
};
</script>

<style scoped>
.gap-2 {
  gap: 8px;
}
.gap-3 {
  gap: 12px;
}
.gap-4 {
  gap: 16px;
}
.rational-tip-box {
  background-color: rgba(var(--v-theme-primary), 0.1);
  border: 1px dashed rgb(var(--v-theme-primary));
  border-radius: 12px;
  padding: 16px;
  text-align: center;
  color: rgb(var(--v-theme-secondary));
  font-size: 0.85rem;
  font-weight: 600;
}
.border-dashed {
  border-style: dashed !important;
}
.transition-swing {
  transition: 0.3s cubic-bezier(0.25, 0.8, 0.5, 1);
}
.transition-swing:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05) !important;
}
.ls-1 {
  letter-spacing: 1px;
}
.form-card :deep(.v-field__input),
.form-card :deep(.v-field__input::placeholder),
.form-card :deep(.v-select__selection-text) {
  color: rgb(var(--v-theme-secondary)) !important;
  opacity: 1 !important;
}
</style>
