import { defineStore } from 'pinia';
import api from '../api/axios';

export const useItemsStore = defineStore('items', {
  state: () => ({
    items: [] as any[],
    loading: false,
  }),
  getters: {
    activeItems: (state) =>
      state.items.filter(
        (i) => i.status !== 'bought' && i.status !== 'cancelled'
      ),
    historyItems: (state) =>
      state.items
        .filter((i) => i.status === 'bought' || i.status === 'cancelled')
        .sort(
          (a, b) =>
            new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
        ),
  },
  actions: {
    async fetchItems() {
      this.loading = true;
      try {
        const response = await api.get('/wishes/');
        this.items = response.data.map((item: any) => ({
          ...item,
          price: Number(item.price),
        }));
      } catch (error) {
        console.error(error);
      } finally {
        this.loading = false;
      }
    },

    async parseItem(link: string) {
      try {
        const response = await api.post('/wishes/parse/', { url: link });
        return response.data;
      } catch (error) {
        throw error;
      }
    },

    async addItem(payload: {
      title: string;
      price: number;
      category: string;
      link?: string;
      image_url?: string;
      manual_days?: number | null;
    }) {
      try {
        const response = await api.post('/wishes/', {
          title: payload.title,
          price: payload.price,
          category: payload.category,
          link_url: payload.link || '',
          image_url: payload.image_url || '',
          manual_days: payload.manual_days ? payload.manual_days : undefined,
        });

        const newItem = {
          ...response.data,
          price: Number(response.data.price),
        };

        this.items.unshift(newItem);
        return true;
      } catch (error) {
        throw error;
      }
    },

    async setItemStatus(id: number, status: 'bought' | 'cancelled') {
      try {
        await api.patch(`/wishes/${id}/`, { status });

        const item = this.items.find((i) => i.id === id);
        if (item) {
          item.status = status;
        }
      } catch (error) {
        console.error('Ошибка обновления статуса:', error);
      }
    },

    async markAsBought(id: number) {
      await this.setItemStatus(id, 'bought');
    },

    async cancelItem(id: number) {
      await this.setItemStatus(id, 'cancelled');
    },

    async deleteItem(id: number) {
      try {
        await api.delete(`/wishes/${id}/`);
        this.items = this.items.filter((i) => i.id !== id);
      } catch (e) {
        console.error(e);
      }
    },
  },
  persist: false,
});
