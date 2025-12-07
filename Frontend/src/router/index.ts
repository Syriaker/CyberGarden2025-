import { createRouter, createWebHistory } from 'vue-router';
import { useUserStore } from '../stores/user';

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      redirect: '/dashboard',
    },
    {
      path: '/login',
      name: 'Login',
      component: () => import('../views/LoginView.vue'),
    },
    {
      path: '/setup',
      name: 'Setup',
      component: () => import('../views/SetupView.vue'),
    },
    {
      path: '/dashboard',
      name: 'Dashboard',
      component: () => import('../views/DashboardView.vue'),
    },
    {
      path: '/history',
      name: 'History',
      component: () => import('../views/HistoryView.vue'),
    },
    {
      path: '/settings',
      name: 'Settings',
      component: () => import('../views/SettingsView.vue'),
    },
  ],
});

router.beforeEach((to, _from, next) => {
  const userStore = useUserStore();

  if (!userStore.isAuthenticated && to.name !== 'Login') {
    return next({ name: 'Login' });
  }

  if (userStore.isAuthenticated) {
    if (to.name === 'Login') {
      return next({ name: userStore.hasFinancialData ? 'Dashboard' : 'Setup' });
    }

    if (!userStore.hasFinancialData && to.name !== 'Setup') {
      return next({ name: 'Setup' });
    }

    if (userStore.hasFinancialData && to.name === 'Setup') {
      return next({ name: 'Dashboard' });
    }
  }

  next();
});

export default router;
