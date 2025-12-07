import { defineStore } from 'pinia';

export const useNotificationStore = defineStore('notifications', {
  state: () => ({
    show: false,
    message: '',
    color: 'success',
    timeout: 3000,
  }),
  actions: {
    notify(message: string, type: 'success' | 'error' | 'info' = 'success') {
      this.message = message;
      this.color = type;
      this.show = true;
    },
  },
});
