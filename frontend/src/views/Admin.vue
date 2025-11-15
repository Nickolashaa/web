<template>
  <div class="admin">
    <header class="header">
      <h1>Панель администратора</h1>
      <div class="header-actions">
        <button @click="$router.push('/shop')" class="btn-back">
          Назад в магазин
        </button>
        <button @click="logout" class="btn-logout">Выйти</button>
      </div>
    </header>

    <div class="container">
      <div class="add-product">
        <h2>{{ editingProduct ? 'Редактировать товар' : 'Добавить товар' }}</h2>
        <form @submit.prevent="saveProduct">
          <div class="form-row">
            <div class="form-group">
              <label>Название</label>
              <input v-model="form.name" type="text" required />
            </div>

            <div class="form-group">
              <label>Тип товара</label>
              <select v-model.number="form.product_type_id" required>
                <option value="">Выберите тип</option>
                <option v-for="type in productTypes" :key="type.id" :value="type.id">
                  {{ type.name }}
                </option>
              </select>
            </div>
          </div>

          <div class="form-group">
            <label>Описание</label>
            <textarea v-model="form.description" rows="3"></textarea>
          </div>

          <div class="form-group">
            <label>Цена</label>
            <input v-model.number="form.price" type="number" step="0.01" required />
          </div>

          <div class="form-group">
            <label>Изображение</label>
            <input type="file" @change="handleImageUpload" accept="image/*" />
            <div v-if="imagePreview" class="image-preview">
              <img :src="imagePreview" alt="Preview" />
            </div>
          </div>

          <div class="form-actions">
            <button type="submit" class="btn-save">
              {{ editingProduct ? 'Сохранить' : 'Добавить' }}
            </button>
            <button
              v-if="editingProduct"
              @click="cancelEdit"
              type="button"
              class="btn-cancel"
            >
              Отмена
            </button>
          </div>
        </form>
      </div>

      <div class="products-list">
        <h2>Список товаров</h2>
        <div v-if="loading" class="loading">Загрузка...</div>

        <table v-else class="products-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Название</th>
              <th>Тип</th>
              <th>Описание</th>
              <th>Цена</th>
              <th>Действия</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="product in allProducts" :key="product.id">
              <td>{{ product.id }}</td>
              <td>{{ product.name }}</td>
              <td>{{ getTypeName(product.product_type_id) }}</td>
              <td>{{ product.description }}</td>
              <td>{{ product.price }} ₽</td>
              <td class="actions">
                <button @click="editProduct(product)" class="btn-edit">
                  Редактировать
                </button>
                <button @click="deleteProduct(product.id)" class="btn-delete">
                  Удалить
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <Footer />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { products, productTypes as productTypesApi } from '../api'
import Footer from '../components/Footer.vue'

const router = useRouter()

const allProducts = ref([])
const productTypes = ref([])
const loading = ref(true)
const editingProduct = ref(null)
const imagePreview = ref(null)

const form = ref({
  name: '',
  product_type_id: '',
  description: '',
  price: 0,
  image: null
})

const loadData = async () => {
  try {
    const [productsRes, typesRes] = await Promise.all([
      products.getAll(),
      productTypesApi.getAll()
    ])

    allProducts.value = productsRes.data
    productTypes.value = typesRes.data
  } catch (error) {
    console.error('Ошибка загрузки:', error)
  } finally {
    loading.value = false
  }
}

const getTypeName = (productTypeId) => {
  const type = productTypes.value.find(t => t.id === productTypeId)
  return type ? type.name : 'Неизвестно'
}

const handleImageUpload = (event) => {
  const file = event.target.files[0]
  if (file) {
    // Создаем preview
    const reader = new FileReader()
    reader.onload = (e) => {
      imagePreview.value = e.target.result
      // Сохраняем base64 без префикса "data:image/...;base64,"
      form.value.image = e.target.result.split(',')[1]
    }
    reader.readAsDataURL(file)
  }
}

const saveProduct = async () => {
  try {
    if (editingProduct.value) {
      await products.update(editingProduct.value.id, form.value)
    } else {
      await products.create(form.value)
    }

    resetForm()
    await loadData()
  } catch (error) {
    alert('Ошибка сохранения товара: ' + (error.response?.data?.detail || error.message))
  }
}

const editProduct = (product) => {
  editingProduct.value = product
  form.value = {
    name: product.name,
    product_type_id: product.product_type_id,
    description: product.description,
    price: product.price
  }
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

const cancelEdit = () => {
  resetForm()
}

const deleteProduct = async (id) => {
  if (confirm('Вы уверены, что хотите удалить этот товар?')) {
    try {
      await products.delete(id)
      await loadData()
    } catch (error) {
      alert('Ошибка удаления товара: ' + (error.response?.data?.detail || error.message))
    }
  }
}

const resetForm = () => {
  editingProduct.value = null
  imagePreview.value = null
  form.value = {
    name: '',
    product_type_id: '',
    description: '',
    price: 0,
    image: null
  }
}

const logout = () => {
  localStorage.removeItem('token')
  localStorage.removeItem('user')
  router.push('/login')
}

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.admin {
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
  max-width: 1400px;
  margin: 2rem auto;
  padding: 0 2rem;
}

.add-product,
.products-list {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  margin-bottom: 2rem;
}

h2 {
  margin: 0 0 1.5rem 0;
  color: #333;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.form-group {
  margin-bottom: 1rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  color: #555;
  font-weight: 500;
}

input,
textarea,
select {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 1rem;
  box-sizing: border-box;
}

input:focus,
textarea:focus,
select:focus {
  outline: none;
  border-color: #667eea;
}

.form-actions {
  display: flex;
  gap: 1rem;
}

.btn-save,
.btn-cancel {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  transition: opacity 0.3s;
}

.btn-save {
  background: #27ae60;
  color: white;
}

.btn-cancel {
  background: #95a5a6;
  color: white;
}

.btn-save:hover,
.btn-cancel:hover {
  opacity: 0.8;
}

.loading {
  text-align: center;
  padding: 2rem;
  color: #666;
}

.products-table {
  width: 100%;
  border-collapse: collapse;
}

.products-table th,
.products-table td {
  padding: 1rem;
  text-align: left;
  border-bottom: 1px solid #eee;
}

.products-table th {
  background: #f8f8f8;
  font-weight: 600;
  color: #333;
}

.products-table td {
  color: #666;
}

.actions {
  display: flex;
  gap: 0.5rem;
}

.btn-edit,
.btn-delete {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  font-size: 0.9rem;
  cursor: pointer;
  transition: opacity 0.3s;
}

.btn-edit {
  background: #3498db;
  color: white;
}

.btn-delete {
  background: #e74c3c;
  color: white;
}

.btn-edit:hover,
.btn-delete:hover {
  opacity: 0.8;
}

.image-preview {
  margin-top: 1rem;
  max-width: 300px;
}

.image-preview img {
  width: 100%;
  height: auto;
  border-radius: 6px;
  border: 2px solid #ddd;
}
</style>
