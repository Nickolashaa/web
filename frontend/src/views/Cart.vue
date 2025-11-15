<template>
  <div class="cart">
    <header class="header">
      <h1>Корзина</h1>
      <div class="header-actions">
        <button @click="$router.push('/shop')" class="btn-back">
          Назад в магазин
        </button>
        <button @click="logout" class="btn-logout">Выйти</button>
      </div>
    </header>

    <div class="container">
      <div v-if="items.length === 0" class="empty">
        <p>Корзина пуста</p>
        <button @click="$router.push('/shop')" class="btn-shop">
          Перейти к покупкам
        </button>
      </div>

      <div v-else class="cart-content">
        <div class="cart-items">
          <div v-for="item in items" :key="item.id" class="cart-item">
            <div class="item-info">
              <h3>{{ item.name }}</h3>
              <p class="description">{{ item.description }}</p>
              <p class="price">{{ item.price }} ₽</p>
            </div>

            <div class="item-controls">
              <div class="quantity-control">
                <button @click="decreaseQuantity(item)" class="qty-btn">-</button>
                <span class="quantity">{{ item.quantity }}</span>
                <button @click="increaseQuantity(item)" class="qty-btn">+</button>
              </div>

              <div class="item-total">
                Итого: {{ item.price * item.quantity }} ₽
              </div>

              <button @click="removeItem(item.id)" class="btn-remove">
                Удалить
              </button>
            </div>
          </div>
        </div>

        <div class="cart-summary">
          <h2>Итого</h2>
          <div class="summary-row">
            <span>Товаров:</span>
            <span>{{ totalItems }}</span>
          </div>
          <div class="summary-row total">
            <span>Сумма:</span>
            <span>{{ totalPrice }} ₽</span>
          </div>
          <button @click="clearCart" class="btn-clear">
            Очистить корзину
          </button>
        </div>
      </div>
    </div>

    <Footer />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { cart } from '../api'
import Footer from '../components/Footer.vue'

const router = useRouter()
const items = ref([])

const totalItems = computed(() => {
  return items.value.reduce((sum, item) => sum + item.quantity, 0)
})

const totalPrice = computed(() => {
  return items.value.reduce((sum, item) => sum + item.price * item.quantity, 0)
})

const loadCart = () => {
  items.value = cart.getItems()
}

const increaseQuantity = (item) => {
  cart.updateQuantity(item.id, item.quantity + 1)
  loadCart()
}

const decreaseQuantity = (item) => {
  if (item.quantity > 1) {
    cart.updateQuantity(item.id, item.quantity - 1)
    loadCart()
  }
}

const removeItem = (id) => {
  cart.removeItem(id)
  loadCart()
}

const clearCart = () => {
  if (confirm('Вы уверены, что хотите очистить корзину?')) {
    cart.clear()
    loadCart()
  }
}

const logout = () => {
  localStorage.removeItem('token')
  localStorage.removeItem('user')
  router.push('/login')
}

onMounted(() => {
  loadCart()
})
</script>

<style scoped>
.cart {
  min-height: 100vh;
  background: #f5f5f5;
  display: flex;
  flex-direction: column;
}

.header {
  background: white;
  padding: 1rem 2rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header h1 {
  margin: 0;
  color: #333;
}

.header-actions {
  display: flex;
  gap: 1rem;
}

.btn-back,
.btn-logout {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  transition: opacity 0.3s;
}

.btn-back {
  background: #667eea;
  color: white;
}

.btn-logout {
  background: #e74c3c;
  color: white;
}

.btn-back:hover,
.btn-logout:hover {
  opacity: 0.8;
}

.container {
  max-width: 1200px;
  margin: 2rem auto;
  padding: 0 2rem;
}

.empty {
  text-align: center;
  padding: 4rem;
  background: white;
  border-radius: 8px;
}

.empty p {
  font-size: 1.5rem;
  color: #666;
  margin-bottom: 2rem;
}

.btn-shop {
  padding: 0.75rem 1.5rem;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.3s;
}

.btn-shop:hover {
  background: #5568d3;
}

.cart-content {
  display: grid;
  grid-template-columns: 1fr 350px;
  gap: 2rem;
}

.cart-items {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.cart-item {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.item-info h3 {
  margin: 0 0 0.5rem 0;
  color: #333;
}

.description {
  color: #666;
  font-size: 0.9rem;
  margin: 0.5rem 0;
}

.price {
  font-weight: 600;
  color: #667eea;
  margin: 0.5rem 0 0 0;
}

.item-controls {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 0.75rem;
}

.quantity-control {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.qty-btn {
  width: 32px;
  height: 32px;
  border: 1px solid #ddd;
  background: white;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1.2rem;
  transition: background 0.3s;
}

.qty-btn:hover {
  background: #f8f8f8;
}

.quantity {
  min-width: 40px;
  text-align: center;
  font-weight: 600;
}

.item-total {
  font-weight: 700;
  color: #333;
  font-size: 1.1rem;
}

.btn-remove {
  padding: 0.5rem 1rem;
  background: #e74c3c;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: opacity 0.3s;
}

.btn-remove:hover {
  opacity: 0.8;
}

.cart-summary {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  height: fit-content;
}

.cart-summary h2 {
  margin: 0 0 1rem 0;
  color: #333;
}

.summary-row {
  display: flex;
  justify-content: space-between;
  padding: 0.75rem 0;
  border-bottom: 1px solid #eee;
}

.summary-row.total {
  font-size: 1.5rem;
  font-weight: 700;
  color: #667eea;
  border-bottom: none;
  margin-top: 0.5rem;
}

.btn-clear {
  width: 100%;
  padding: 0.75rem;
  background: #e74c3c;
  color: white;
  border: none;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  margin-top: 1.5rem;
  transition: opacity 0.3s;
}

.btn-clear:hover {
  opacity: 0.8;
}
</style>
