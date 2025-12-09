<template>
  <div v-if="isOpen" class="modal-overlay" @click.self="closeModal">
    <div class="modal-content">
      <div class="modal-header">
        <h2>Оставить отзыв</h2>
        <button @click="closeModal" class="btn-close">&times;</button>
      </div>

      <form @submit.prevent="submitReview" class="review-form">
        <div class="form-group">
          <label>Оценка</label>
          <div class="rating">
            <button
              v-for="star in 5"
              :key="star"
              type="button"
              @click="rating = star"
              class="star-btn"
              :class="{ active: star <= rating }"
            >
              ★
            </button>
          </div>
          <p v-if="errors.rating" class="error">{{ errors.rating }}</p>
        </div>

        <div class="form-group">
          <label for="text">Текст отзыва</label>
          <textarea
            id="text"
            v-model="text"
            placeholder="Расскажите о вашем опыте..."
            rows="5"
            maxlength="1000"
          ></textarea>
          <p class="char-count">{{ text.length }} / 1000</p>
          <p v-if="errors.text" class="error">{{ errors.text }}</p>
        </div>

        <p v-if="errors.general" class="error">{{ errors.general }}</p>

        <div class="modal-actions">
          <button type="button" @click="closeModal" class="btn btn-cancel">
            Отмена
          </button>
          <button type="submit" class="btn btn-submit" :disabled="loading">
            {{ loading ? 'Отправка...' : 'Отправить' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { reviews } from '../api'

const props = defineProps({
  isOpen: {
    type: Boolean,
    required: true
  }
})

const emit = defineEmits(['close', 'submitted'])

const rating = ref(5)
const text = ref('')
const loading = ref(false)
const errors = ref({})

watch(() => props.isOpen, (newVal) => {
  if (newVal) {
    rating.value = 5
    text.value = ''
    errors.value = {}
  }
})

const validateForm = () => {
  errors.value = {}
  let isValid = true

  if (rating.value < 1 || rating.value > 5) {
    errors.value.rating = 'Выберите оценку от 1 до 5'
    isValid = false
  }

  if (!text.value.trim()) {
    errors.value.text = 'Текст отзыва не может быть пустым'
    isValid = false
  } else if (text.value.length > 1000) {
    errors.value.text = 'Текст слишком длинный (максимум 1000 символов)'
    isValid = false
  }

  return isValid
}

const submitReview = async () => {
  if (!validateForm()) {
    return
  }

  loading.value = true
  errors.value = {}

  try {
    await reviews.create({
      rating: rating.value,
      text: text.value
    })

    emit('submitted')
    closeModal()
  } catch (error) {
    console.error('Ошибка при отправке отзыва:', error)
    if (error.response?.status === 401) {
      errors.value.general = 'Необходима авторизация для отправки отзыва'
    } else if (error.response?.data?.detail) {
      errors.value.general = error.response.data.detail
    } else {
      errors.value.general = 'Произошла ошибка при отправке отзыва'
    }
  } finally {
    loading.value = false
  }
}

const closeModal = () => {
  emit('close')
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  animation: fadeIn 0.2s;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.modal-content {
  background: white;
  border-radius: 12px;
  width: 90%;
  max-width: 600px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
  animation: slideUp 0.3s;
}

@keyframes slideUp {
  from {
    transform: translateY(20px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #e0e0e0;
}

.modal-header h2 {
  margin: 0;
  color: #333;
  font-size: 1.5rem;
}

.btn-close {
  background: none;
  border: none;
  font-size: 2rem;
  color: #999;
  cursor: pointer;
  line-height: 1;
  padding: 0;
  width: 32px;
  height: 32px;
  transition: color 0.3s;
}

.btn-close:hover {
  color: #333;
}

.review-form {
  padding: 1.5rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: #333;
}

.rating {
  display: flex;
  gap: 0.5rem;
}

.star-btn {
  background: none;
  border: none;
  font-size: 2rem;
  color: #ddd;
  cursor: pointer;
  transition: all 0.2s;
  padding: 0;
}

.star-btn:hover,
.star-btn.active {
  color: #ffd700;
  transform: scale(1.1);
}

textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-family: inherit;
  font-size: 1rem;
  resize: vertical;
  transition: border-color 0.3s;
}

textarea:focus {
  outline: none;
  border-color: #667eea;
}

.char-count {
  text-align: right;
  font-size: 0.85rem;
  color: #999;
  margin-top: 0.25rem;
}

.error {
  color: #e74c3c;
  font-size: 0.9rem;
  margin-top: 0.25rem;
}

.modal-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  margin-top: 2rem;
}

.btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  font-size: 1rem;
}

.btn-cancel {
  background: #f0f0f0;
  color: #333;
}

.btn-cancel:hover {
  background: #e0e0e0;
}

.btn-submit {
  background: #667eea;
  color: white;
}

.btn-submit:hover:not(:disabled) {
  background: #5568d3;
}

.btn-submit:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>
