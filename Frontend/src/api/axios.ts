import axios from 'axios'
import { useUserStore } from '../stores/user'

const api = axios.create({
  baseURL: 'http://localhost:8000/api', 
  headers: {
    'Content-Type': 'application/json',
  }
})

api.interceptors.request.use((config) => {
  const userStore = useUserStore()
  if (userStore.nickname) {
    config.headers['X-User-Nickname'] = userStore.nickname
  }
  return config
})

export default api