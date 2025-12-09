<template>
  <div class="shop">
    <header class="header">
      <h1>DIAMANT</h1>
      <div class="header-actions">
        <button @click="openReviewModal" class="btn-review">
          Оставить отзыв
        </button>
        <button @click="$router.push('/admin')" v-if="isAdmin" class="btn-admin">
          Админ-панель
        </button>
        <button @click="$router.push('/cart')" class="btn-cart">
          Корзина ({{ cartCount }})
        </button>
        <button @click="logout" class="btn-logout">Выйти</button>
      </div>
    </header>

    <div class="reviews-section">
      <ReviewsSlider />
    </div>

    <div class="container">
      <aside class="sidebar">
        <h3>Категории</h3>
        <div class="category-list">
          <button
            @click="selectedType = null"
            :class="{ active: selectedType === null }"
            class="category-btn"
          >
            Все товары
          </button>
          <button
            v-for="type in productTypes"
            :key="type.id"
            @click="selectedType = type.id"
            :class="{ active: selectedType === type.id }"
            class="category-btn"
          >
            {{ type.name }}
          </button>
        </div>

        <div class="search-section">
          <h3>Поиск товаров</h3>
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Введите название или описание..."
            class="search-input"
          />
        </div>
      </aside>

      <main class="products">
        <div v-if="loading" class="loading">Загрузка...</div>

        <div v-else class="product-grid">
          <div
            v-for="product in filteredProducts"
            :key="product.id"
            class="product-card"
          >
            <img
              v-if="product.image"
              :src="`data:image/png;base64,${product.image}`"
              :alt="product.name"
              class="product-image"
            />
            <div v-else class="no-image">Нет фото</div>
            <h3>{{ product.name }}</h3>
            <p class="description">{{ product.description }}</p>
            <p class="price">{{ product.price }} ₽</p>
            <button @click="addToCart(product)" class="btn-add">
              В корзину
            </button>
          </div>
        </div>

        <div v-if="!loading && filteredProducts.length === 0" class="empty">
          Товары не найдены
        </div>
      </main>
    </div>

    <ReviewModal
      :isOpen="isReviewModalOpen"
      @close="closeReviewModal"
      @submitted="onReviewSubmitted"
    />

    <Footer />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { products, productTypes as productTypesApi, cart } from '../api'
import Footer from '../components/Footer.vue'
import ReviewModal from '../components/ReviewModal.vue'
import ReviewsSlider from '../components/ReviewsSlider.vue'

const router = useRouter()

const allProducts = ref([])
const productTypes = ref([])
const selectedType = ref(null)
const searchQuery = ref('')
const loading = ref(true)
const cartCount = ref(0)
const isAdmin = ref(false)
const isReviewModalOpen = ref(false)

const filteredProducts = computed(() => {
  let products = allProducts.value

  // Фильтр по категории
  if (selectedType.value !== null) {
    products = products.filter(p => p.product_type_id === selectedType.value)
  }

  // Фильтр по поисковому запросу
  if (searchQuery.value.trim()) {
    const query = searchQuery.value.toLowerCase().trim()
    products = products.filter(p =>
      p.name.toLowerCase().includes(query) ||
      (p.description && p.description.toLowerCase().includes(query))
    )
  }

  return products
})

const loadData = async () => {
  try {
    const [productsRes, typesRes] = await Promise.all([
      products.getAll(),
      productTypesApi.getAll()
    ])

    allProducts.value = productsRes.data
    productTypes.value = typesRes.data

    const user = JSON.parse(localStorage.getItem('user') || '{}')
    isAdmin.value = user.is_superuser || false

    updateCartCount()
  } catch (error) {
    console.error('Ошибка загрузки:', error)
  } finally {
    loading.value = false
  }
}

const addToCart = (product) => {
  cart.addItem(product, 1)
  updateCartCount()
}

const updateCartCount = () => {
  const items = cart.getItems()
  cartCount.value = items.reduce((sum, item) => sum + item.quantity, 0)
}

const logout = () => {
  localStorage.removeItem('token')
  localStorage.removeItem('user')
  router.push('/login')
}

const openReviewModal = () => {
  isReviewModalOpen.value = true
}

const closeReviewModal = () => {
  isReviewModalOpen.value = false
}

const onReviewSubmitted = () => {
  alert('Спасибо за ваш отзыв!')
}

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.shop {
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

.btn-review,
.btn-admin,
.btn-cart,
.btn-logout {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  transition: opacity 0.3s;
}

.btn-review {
  background: #2ecc71;
  color: white;
}

.btn-admin {
  background: #9b59b6;
  color: white;
}

.btn-cart {
  background: #667eea;
  color: white;
}

.btn-logout {
  background: #e74c3c;
  color: white;
}

.btn-review:hover,
.btn-admin:hover,
.btn-cart:hover,
.btn-logout:hover {
  opacity: 0.8;
}

.reviews-section {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 2rem;
}

.container {
  display: flex;
  max-width: 1400px;
  margin: 2rem auto;
  gap: 2rem;
  padding: 0 2rem;
}

.sidebar {
  flex: 0 0 250px;
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  height: fit-content;
}

.sidebar h3 {
  margin: 0 0 1rem 0;
}

.category-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.category-btn {
  padding: 0.75rem;
  border: 1px solid #ddd;
  background: white;
  border-radius: 6px;
  cursor: pointer;
  text-align: left;
  transition: all 0.3s;
}

.category-btn:hover {
  background: #f8f8f8;
}

.category-btn.active {
  background: #667eea;
  color: white;
  border-color: #667eea;
}

.search-section {
  margin-top: 2rem;
}

.search-section h3 {
  margin: 0 0 1rem 0;
}

.search-input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 0.95rem;
  transition: border-color 0.3s;
}

.search-input:focus {
  outline: none;
  border-color: #667eea;
}

.search-input::placeholder {
  color: #999;
}

.products {
  flex: 1;
}

.loading,
.empty {
  text-align: center;
  padding: 3rem;
  background: white;
  border-radius: 8px;
  color: #666;
}

.product-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
}

.product-card {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s;
}

.product-card:hover {
  transform: translateY(-4px);
}

.product-image {
  width: 100%;
  height: 200px;
  object-fit: cover;
  border-radius: 6px;
  margin-bottom: 1rem;
}

.no-image {
  width: 100%;
  height: 200px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f0f0f0;
  color: #999;
  border-radius: 6px;
  margin-bottom: 1rem;
}

.product-card h3 {
  margin: 0 0 0.5rem 0;
  color: #333;
  font-size: 1.1rem;
}

.description {
  color: #666;
  margin: 0.5rem 0;
  font-size: 0.85rem;
  line-height: 1.4;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.price {
  font-size: 1.3rem;
  font-weight: 700;
  color: #667eea;
  margin: 1rem 0;
}

.btn-add {
  width: 100%;
  padding: 0.75rem;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.3s;
}

.btn-add:hover {
  background: #5568d3;
}
</style>
