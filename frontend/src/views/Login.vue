<template>
  <div class="auth-container">
    <div class="auth-card">
      <h1>{{ isLogin ? 'Вход' : 'Регистрация' }}</h1>

      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <label>Логин</label>
          <input v-model="login" type="text" required />
        </div>

        <div class="form-group">
          <label>Пароль</label>
          <input v-model="password" type="password" required />
        </div>

        <div v-if="error" class="error">{{ error }}</div>

        <button type="submit" class="btn-primary">
          {{ isLogin ? 'Войти' : 'Зарегистрироваться' }}
        </button>
      </form>

      <p class="toggle-mode">
        {{ isLogin ? 'Нет аккаунта?' : 'Уже есть аккаунт?' }}
        <a @click="isLogin = !isLogin">
          {{ isLogin ? 'Зарегистрируйтесь' : 'Войдите' }}
        </a>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { auth } from '../api'

const router = useRouter()

const isLogin = ref(true)
const login = ref('')
const password = ref('')
const error = ref('')

const handleSubmit = async () => {
  error.value = ''

  try {
    const response = isLogin.value
      ? await auth.login(login.value, password.value)
      : await auth.register(login.value, password.value)

    localStorage.setItem('token', response.data.access_token)

    const userResponse = await auth.getCurrentUser()
    localStorage.setItem('user', JSON.stringify(userResponse.data))

    router.push('/shop')
  } catch (err) {
    error.value = err.response?.data?.detail || 'Произошла ошибка'
  }
}
</script>

<style scoped>
.auth-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.auth-card {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
}

h1 {
  margin-bottom: 1.5rem;
  text-align: center;
  color: #333;
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

input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 1rem;
  box-sizing: border-box;
}

input:focus {
  outline: none;
  border-color: #667eea;
}

.error {
  color: #e74c3c;
  margin-bottom: 1rem;
  padding: 0.75rem;
  background: #fee;
  border-radius: 6px;
  text-align: center;
}

.btn-primary {
  width: 100%;
  padding: 0.75rem;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.3s;
}

.btn-primary:hover {
  background: #5568d3;
}

.toggle-mode {
  text-align: center;
  margin-top: 1.5rem;
  color: #666;
}

.toggle-mode a {
  color: #667eea;
  cursor: pointer;
  text-decoration: none;
  font-weight: 600;
}

.toggle-mode a:hover {
  text-decoration: underline;
}
</style>
