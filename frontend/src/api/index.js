import axios from 'axios'

const API_URL = 'http://localhost:8000'

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

api.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export const auth = {
  register: (login, password) => api.post('/auth/register', { login, password }),
  login: (login, password) => api.post('/auth/login', { login, password }),
  getCurrentUser: () => api.get('/users/me')
}

export const products = {
  getAll: () => api.get('/products/'),
  getById: (id) => api.get(`/products/${id}`),
  create: (data) => api.post('/products/', data),
  update: (id, data) => api.put(`/products/${id}`, data),
  delete: (id) => api.delete(`/products/${id}`)
}

export const productTypes = {
  getAll: () => api.get('/product_types/'),
  getById: (id) => api.get(`/product_types/${id}`)
}

export const reviews = {
  getAll: () => api.get('/reviews/'),
  getLatest: () => api.get('/reviews/latest'),
  getById: (id) => api.get(`/reviews/${id}`),
  create: (data) => api.post('/reviews/', data)
}

export const cart = {
  getItems: () => {
    const items = localStorage.getItem('cart')
    return items ? JSON.parse(items) : []
  },
  addItem: (product, quantity = 1) => {
    const items = cart.getItems()
    const existingItem = items.find(item => item.id === product.id)

    if (existingItem) {
      existingItem.quantity += quantity
    } else {
      items.push({ ...product, quantity })
    }

    localStorage.setItem('cart', JSON.stringify(items))
    return items
  },
  updateQuantity: (productId, quantity) => {
    const items = cart.getItems()
    const item = items.find(item => item.id === productId)

    if (item) {
      item.quantity = quantity
      if (item.quantity <= 0) {
        return cart.removeItem(productId)
      }
      localStorage.setItem('cart', JSON.stringify(items))
    }

    return items
  },
  removeItem: (productId) => {
    const items = cart.getItems().filter(item => item.id !== productId)
    localStorage.setItem('cart', JSON.stringify(items))
    return items
  },
  clear: () => {
    localStorage.removeItem('cart')
    return []
  }
}

export default api
