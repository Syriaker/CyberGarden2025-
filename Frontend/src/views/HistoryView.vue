<template>
  <v-container
    class="fill-height align-start bg-background pa-8"
    style="max-width: 1200px"
  >
    <v-row>
      <v-col cols="12">
        <h1 class="text-h4 font-weight-bold text-secondary mb-6">
          История решений
        </h1>

        <v-row class="mb-6">
          <v-col cols="12" sm="4">
            <v-card class="pa-4 rounded-xl h-100" elevation="0" color="surface">
              <div class="d-flex align-center gap-3 mb-2">
                <v-avatar color="red-lighten-4" size="40">
                  <v-icon :icon="mdiCashMinus" color="error"></v-icon>
                </v-avatar>
                <span
                  class="text-caption text-secondary font-weight-bold text-uppercase"
                  >Потрачено</span
                >
              </div>
              <div class="text-h5 font-weight-bold text-error">
                {{ stats.spent.toLocaleString() }} ₽
              </div>
            </v-card>
          </v-col>

          <v-col cols="12" sm="4">
            <v-card class="pa-4 rounded-xl h-100" elevation="0" color="surface">
              <div class="d-flex align-center gap-3 mb-2">
                <v-avatar color="green-lighten-4" size="40">
                  <v-icon :icon="mdiPiggyBank" color="success"></v-icon>
                </v-avatar>
                <span
                  class="text-caption text-secondary font-weight-bold text-uppercase"
                  >Сэкономлено</span
                >
              </div>
              <div class="text-h5 font-weight-bold text-success">
                {{ stats.saved.toLocaleString() }} ₽
              </div>
            </v-card>
          </v-col>

          <v-col cols="12" sm="4">
            <v-card class="pa-4 rounded-xl h-100" elevation="0" color="surface">
              <div class="d-flex align-center gap-3 mb-2">
                <v-avatar color="blue-lighten-4" size="40">
                  <v-icon :icon="mdiChartPie" color="info"></v-icon>
                </v-avatar>
                <span
                  class="text-caption text-secondary font-weight-bold text-uppercase"
                  >Рациональность</span
                >
              </div>
              <div class="text-h5 font-weight-bold text-info">
                {{ stats.rationalScore }}%
              </div>
              <v-progress-linear
                :model-value="stats.rationalScore"
                color="info"
                height="4"
                rounded
                class="mt-2"
              ></v-progress-linear>
            </v-card>
          </v-col>
        </v-row>

        <div
          class="d-flex flex-column flex-md-row align-center justify-space-between mb-6 gap-4"
        >
          <v-tabs
            v-model="activeTab"
            color="primary"
            bg-color="transparent"
            density="compact"
            class="rounded-xl"
          >
            <v-tab value="all" class="text-capitalize rounded-xl text-secondary"
              >Все</v-tab
            >
            <v-tab
              value="bought"
              class="text-capitalize rounded-xl text-secondary"
              >Куплено</v-tab
            >
            <v-tab
              value="cancelled"
              class="text-capitalize rounded-xl text-secondary"
              >Отменено</v-tab
            >
          </v-tabs>

          <v-text-field
            v-model="search"
            placeholder="Поиск по истории..."
            variant="outlined"
            density="compact"
            rounded="xl"
            bg-color="surface"
            hide-details
            :prepend-inner-icon="mdiMagnify"
            style="max-width: 300px; width: 100%"
          ></v-text-field>
        </div>

        <div
          v-if="filteredItems.length === 0"
          class="d-flex flex-column align-center justify-center py-12 text-center"
        >
          <v-sheet
            color="surface"
            height="120"
            width="120"
            class="rounded-circle d-flex align-center justify-center mb-4"
          >
            <v-icon :icon="mdiHistory" size="64" color="grey"></v-icon>
          </v-sheet>
          <h3 class="text-h6 text-secondary font-weight-bold">История пуста</h3>
          <p class="text-body-2 text-secondary">
            Здесь будут отображаться ваши завершенные решения.
          </p>
        </div>

        <v-fade-transition group>
          <div v-for="item in filteredItems" :key="item.id" class="mb-3">
            <v-card
              class="rounded-xl pa-2 pl-4 pr-4"
              elevation="0"
              color="surface"
            >
              <div class="d-flex align-center justify-space-between py-2">
                <div class="d-flex align-center gap-4 flex-grow-1">
                  <v-sheet
                    :color="
                      item.status === 'bought'
                        ? 'red-lighten-5'
                        : 'green-lighten-5'
                    "
                    height="48"
                    width="48"
                    class="d-flex align-center justify-center rounded-lg flex-shrink-0"
                  >
                    <v-icon
                      :icon="
                        item.status === 'bought'
                          ? mdiShopping
                          : mdiPiggyBankOutline
                      "
                      :color="item.status === 'bought' ? 'error' : 'success'"
                      size="24"
                    ></v-icon>
                  </v-sheet>

                  <div class="d-flex flex-column" style="min-width: 0">
                    <div class="d-flex align-center gap-2">
                      <h3
                        class="text-subtitle-1 font-weight-bold text-secondary text-truncate"
                      >
                        {{ item.title }}
                      </h3>
                      <v-btn
                        v-if="item.link_url"
                        icon
                        variant="text"
                        density="compact"
                        size="small"
                        color="grey-darken-1"
                        :href="item.link_url"
                        target="_blank"
                      >
                        <v-icon :icon="mdiOpenInNew" size="16"></v-icon>
                      </v-btn>
                    </div>
                    <span class="text-caption text-secondary">
                      {{ new Date(item.created_at).toLocaleDateString() }} •
                      {{ item.category }}
                    </span>
                  </div>
                </div>

                <div
                  class="text-right d-flex flex-column align-end flex-shrink-0 ml-4"
                >
                  <span
                    class="text-h6 font-weight-bold"
                    :class="
                      item.status === 'bought'
                        ? 'text-secondary'
                        : 'text-success'
                    "
                  >
                    {{ item.status === 'bought' ? '-' : '+' }}
                    {{ item.price.toLocaleString() }} ₽
                  </span>

                  <v-chip
                    size="small"
                    :color="getStatusColor(item)"
                    variant="tonal"
                    class="font-weight-bold mt-1"
                  >
                    {{ getStatusText(item) }}
                  </v-chip>
                </div>
              </div>
            </v-card>
          </div>
        </v-fade-transition>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useItemsStore } from '../stores/items';
import {
  mdiHistory,
  mdiShopping,
  mdiPiggyBankOutline,
  mdiOpenInNew,
  mdiMagnify,
  mdiCashMinus,
  mdiPiggyBank,
  mdiChartPie,
} from '@mdi/js';

const itemsStore = useItemsStore();
const activeTab = ref('all');
const search = ref('');

onMounted(() => {
  itemsStore.fetchItems();
});

const stats = computed(() => {
  const history = itemsStore.historyItems;

  const spent = history
    .filter((i) => i.status === 'bought')
    .reduce((acc, curr) => acc + Number(curr.price), 0);

  const saved = history
    .filter((i) => i.status === 'cancelled')

    .reduce((acc, curr) => acc + Number(curr.price), 0);

  const total = history.length;
  const rationalActions = history.filter(
    (i) => i.status === 'cancelled'
  ).length;

  const rationalScore =
    total > 0 ? Math.round((rationalActions / total) * 100) : 100;

  return { spent, saved, rationalScore };
});

const filteredItems = computed(() => {
  let items = itemsStore.historyItems;

  if (activeTab.value === 'bought') {
    items = items.filter((i) => i.status === 'bought');
  } else if (activeTab.value === 'cancelled') {
    items = items.filter((i) => i.status === 'cancelled');
  }

  if (search.value) {
    const q = search.value.toLowerCase();
    items = items.filter(
      (i) =>
        i.title.toLowerCase().includes(q) ||
        i.category.toLowerCase().includes(q)
    );
  }

  return items;
});

const getStatusColor = (item: any) => {
  if (item.status === 'cancelled') return 'success';
  return 'grey-darken-1';
};

const getStatusText = (item: any) => {
  if (item.status === 'cancelled') return 'Сэкономлено';
  return 'Куплено';
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
</style>
