import { defineStore } from 'pinia';
import api from '../api/axios';
import { CATEGORIES } from '../utils/constants';

export const useUserStore = defineStore('user', {
  state: () => ({
    nickname: '',
    current_savings: 0,
    monthly_savings: 0,
    monthly_spendings: 0,
    free_budget: 0,
    availableCategories: [...CATEGORIES],
    settings: {
      email: '',
      notifyOnEnd: true,
      reportFrequency: 'none',
      forbiddenCategories: [] as string[],
      theme: 'light' as 'light' | 'dark',
    },
  }),
  getters: {
    isAuthenticated: (state) => !!state.nickname,
    hasFinancialData: (state) =>
      state.monthly_savings > 0 || state.current_savings > 0,
    freeBudget: (state) => state.free_budget,
    allCategories: (state) => state.availableCategories,
  },
  actions: {
    async auth(nickname: string) {
      try {
        const response = await api.post('/users/auth/', { nickname });
        this.updateState(response.data.data, true);
        this.nickname = nickname;
        return response.data.status;
      } catch (error) {
        throw error;
      }
    },

    async updateProfile(data: any) {
      try {
        if (data.theme) this.settings.theme = data.theme;
        this.settings.email = data.email;
        this.settings.notifyOnEnd = data.notifyOnEnd;
        this.settings.reportFrequency = data.reportFrequency;
        this.settings.forbiddenCategories = data.forbiddenCategories;

        const payload = {
          nickname: this.nickname,
          current_savings: data.current_savings,
          monthly_savings: data.monthly_savings,
          monthly_spendings: data.monthly_spendings,
          theme: data.theme,
          email: data.email,
          notify_on_end: data.notifyOnEnd,
          forbidden_categories: data.forbiddenCategories,
        };

        const response = await api.post('/users/auth/', payload);

        this.updateState(response.data.data, false);
      } catch (error) {
        throw error;
      }
    },

    async fetchProfile() {
      if (!this.nickname) return;
      try {
        const response = await api.get(`/users/${this.nickname}/`);
        this.updateState(response.data, false);
      } catch (error) {
        console.error(error);
      }
    },

    /**
     * @param data
     * @param syncSettings
     *
     */
    updateState(data: any, syncSettings = false) {
      this.nickname = data.nickname;
      this.current_savings = parseFloat(data.current_savings || 0);
      this.monthly_savings = parseFloat(data.monthly_savings || 0);
      this.monthly_spendings = parseFloat(data.monthly_spendings || 0);
      this.free_budget = parseFloat(data.available_cash || 0);

      if (syncSettings) {
        if (data.email) this.settings.email = data.email;

        if (data.theme && (data.theme === 'light' || data.theme === 'dark')) {
          this.settings.theme = data.theme;
        }

        if (data.forbidden_categories) {
          if (typeof data.forbidden_categories === 'string') {
            this.settings.forbiddenCategories = data.forbidden_categories
              .split(',')
              .map((s: string) => s.trim())
              .filter((s: string) => s);
          } else if (Array.isArray(data.forbidden_categories)) {
            this.settings.forbiddenCategories = data.forbidden_categories;
          }
        }
      }
    },

    addCustomCategory(newCategory: string) {
      const exists = this.availableCategories.some(
        (c) => c.toLowerCase() === newCategory.toLowerCase()
      );
      if (!exists && newCategory.trim() !== '') {
        this.availableCategories.push(newCategory);
      }
    },

    logout() {
      this.$reset();
      localStorage.clear();
    },
  },
  persist: true,
});
