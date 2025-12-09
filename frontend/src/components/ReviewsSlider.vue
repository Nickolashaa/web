<template>
  <div class="reviews-slider" v-if="reviews.length > 0">
    <div class="slider-header">
      <h2>Отзывы наших клиентов</h2>
    </div>

    <div class="slider-container">
      <button
        @click="prevSlide"
        class="slider-btn slider-btn-prev"
        aria-label="Предыдущий отзыв"
      >
        ‹
      </button>

      <div class="slider-track">
        <transition name="slide" mode="out-in">
          <div :key="currentIndex" class="review-card">
            <div class="review-rating">
              <span v-for="star in 5" :key="star" class="star" :class="{ filled: star <= currentReview.rating }">
                ★
              </span>
            </div>
            <p class="review-text">{{ currentReview.text }}</p>
            <div class="review-author">
              <span class="author-name">{{ currentReview.user_login || 'Клиент' }}</span>
              <span class="review-date">{{ formatDate(currentReview.created_at) }}</span>
            </div>
          </div>
        </transition>
      </div>

      <button
        @click="nextSlide"
        class="slider-btn slider-btn-next"
        aria-label="Следующий отзыв"
      >
        ›
      </button>
    </div>

    <div class="slider-dots">
      <button
        v-for="(review, index) in reviews"
        :key="review.id"
        @click="goToSlide(index)"
        :class="['dot', { active: index === currentIndex }]"
        :aria-label="`Перейти к отзыву ${index + 1}`"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import { reviews as reviewsApi } from '../api'

const reviews = ref([])
const currentIndex = ref(0)
let autoplayInterval = null

const currentReview = computed(() => {
  return reviews.value[currentIndex.value]
})

const loadReviews = async () => {
  try {
    const response = await reviewsApi.getLatest()
    reviews.value = response.data
  } catch (error) {
    console.error('Ошибка загрузки отзывов:', error)
  }
}

const nextSlide = () => {
  currentIndex.value = (currentIndex.value + 1) % reviews.value.length
  resetAutoplay()
}

const prevSlide = () => {
  currentIndex.value = currentIndex.value === 0
    ? reviews.value.length - 1
    : currentIndex.value - 1
  resetAutoplay()
}

const goToSlide = (index) => {
  currentIndex.value = index
  resetAutoplay()
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('ru-RU', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

const startAutoplay = () => {
  autoplayInterval = setInterval(() => {
    nextSlide()
  }, 5000) // Переключение каждые 5 секунд
}

const stopAutoplay = () => {
  if (autoplayInterval) {
    clearInterval(autoplayInterval)
    autoplayInterval = null
  }
}

const resetAutoplay = () => {
  stopAutoplay()
  startAutoplay()
}

onMounted(() => {
  loadReviews().then(() => {
    if (reviews.value.length > 1) {
      startAutoplay()
    }
  })
})

onBeforeUnmount(() => {
  stopAutoplay()
})
</script>

<style scoped>
.reviews-slider {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  margin: 2rem 0;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}

.slider-header {
  text-align: center;
  margin-bottom: 2rem;
}

.slider-header h2 {
  margin: 0;
  color: #333;
  font-size: 1.8rem;
  font-weight: 600;
}

.slider-container {
  display: flex;
  align-items: center;
  gap: 1rem;
  position: relative;
}

.slider-track {
  flex: 1;
  min-height: 250px;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.review-card {
  background: #f8f9fa;
  border-radius: 12px;
  padding: 2rem;
  width: 100%;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.review-rating {
  display: flex;
  gap: 0.25rem;
  margin-bottom: 1rem;
  justify-content: center;
}

.star {
  font-size: 1.5rem;
  color: #ddd;
  transition: color 0.3s;
}

.star.filled {
  color: #ffc107;
}

.review-text {
  font-size: 1.1rem;
  line-height: 1.6;
  color: #555;
  margin: 0 0 1.5rem 0;
  text-align: center;
  min-height: 100px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.review-author {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.25rem;
}

.author-name {
  font-weight: 600;
  color: #333;
  font-size: 1rem;
}

.review-date {
  font-size: 0.85rem;
  color: #999;
}

.slider-btn {
  background: #667eea;
  color: white;
  border: none;
  border-radius: 50%;
  width: 50px;
  height: 50px;
  font-size: 2rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s;
  flex-shrink: 0;
  line-height: 1;
  padding: 0;
}

.slider-btn:hover {
  background: #5568d3;
  transform: scale(1.1);
}

.slider-btn:active {
  transform: scale(0.95);
}

.slider-dots {
  display: flex;
  justify-content: center;
  gap: 0.5rem;
  margin-top: 1.5rem;
}

.dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  border: 2px solid #667eea;
  background: white;
  cursor: pointer;
  transition: all 0.3s;
  padding: 0;
}

.dot:hover {
  transform: scale(1.2);
}

.dot.active {
  background: #667eea;
}

/* Анимация переключения */
.slide-enter-active,
.slide-leave-active {
  transition: all 0.5s ease;
}

.slide-enter-from {
  opacity: 0;
  transform: translateX(30px);
}

.slide-leave-to {
  opacity: 0;
  transform: translateX(-30px);
}

/* Адаптивность */
@media (max-width: 768px) {
  .reviews-slider {
    padding: 1.5rem 1rem;
  }

  .slider-header h2 {
    font-size: 1.4rem;
  }

  .review-card {
    padding: 1.5rem;
  }

  .review-text {
    font-size: 1rem;
    min-height: 120px;
  }

  .slider-btn {
    width: 40px;
    height: 40px;
    font-size: 1.5rem;
  }
}
</style>
