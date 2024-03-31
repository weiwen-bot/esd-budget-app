<template>
  <div class="flex justify-center">
    <div class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4 w-full max-w-xs">
      <h1 class="text-2xl mb-4">Login</h1>
      <form @submit.prevent="login">
        <div class="mb-4">
          <label class="block text-gray-700 text-sm font-bold mb-2" for="username">Username:</label>
          <input class="shadow appearance-none border rounded w-full py-2 px-3 text-black leading-tight focus:outline-none focus:shadow-outline bg-white" id="username" type="text" v-model="username" required>
        </div>
        <div class="mb-6">
          <label class="block text-gray-700 text-sm font-bold mb-2" for="password">Password:</label>
          <input class="shadow appearance-none border rounded w-full py-2 px-3 text-black leading-tight focus:outline-none focus:shadow-outline bg-white" id="password" type="password" v-model="password" required>
        </div>
        <div class="flex items-center justify-center">
          <button class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline" type="submit">
            Login
          </button>
        </div>
      </form>
      <div v-if="errorMessage" class="mt-4 text-red-500">{{ errorMessage }}</div>
      <p class="text-sm text-black text-center mt-4">
  Don't have an account? <router-link to="/register" class="underline text-blue-500 hover:text-blue-700"><p>Register</p></router-link>
</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Login',
  data() {
    return {
      username: '',
      password: '',
      errorMessage: ''
    };
  },
  created(){
      this.username = sessionStorage.getItem("username");
      this.password = sessionStorage.getItem("password");
    
  },
  methods: {
    async login() {
      if (!this.username || !this.password) {
        this.errorMessage = 'Please enter both username and password';
        return;
      }
      try {
        const response = await fetch('http://localhost:5173/login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            username: this.username,
            password: this.password
          })
        });
        const data = await response.json();
        if (response.ok) {
          console.log('Logged in successfully:', data);
          console.log(this.username);
          console.log(this.password);
          
          // Redirect the user to another page after successful login
          // For example, using Vue Router: this.$router.push('/dashboard');
        } else {
          this.errorMessage = data.message || 'Failed to login';
        }
      } catch (error) {
        console.error('Error logging in:', error);
        this.errorMessage = 'An error occurred while logging in';
      }
    }
  }
};
</script>

<style>
</style>
