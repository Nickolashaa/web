<template>
  <footer class="footer">
    <p>&copy; {{ currentYear }} DIAMANT. Все права защищены</p>
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
  margin: 0;
  font-size: 0.9rem;
}
</style>
