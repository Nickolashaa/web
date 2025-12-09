<template>
  <footer class="footer">
    <p>&copy; {{ currentYear }} DIAMANT. Все права защищены</p>
    <router-link to="/privacy" class="privacy-link">Политика конфиденциальности</router-link>
  </footer>
</template>

<script setup>
import { computed } from 'vue'

const currentYear = computed(() => new Date().getFullYear())
</script>

<style scoped>
.footer {
  background: #2c3e50;
  color: white;
  text-align: center;
  padding: 1.5rem;
  margin-top: auto;
}

.footer p {
  margin: 0 0 0.5rem 0;
  font-size: 0.9rem;
}

.privacy-link {
  color: #667eea;
  text-decoration: none;
  font-size: 0.85rem;
  transition: color 0.3s;
}

.privacy-link:hover {
  color: #5568d3;
  text-decoration: underline;
}
</style>
