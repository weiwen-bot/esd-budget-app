<template>
    <div class="flex justify-center items-center h-screen">
      <div class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4 w-full max-w-xs">
        <h2 class="text-2xl mb-4">Login</h2>
        <form @submit.prevent="login">
          <div class="mb-4">
            <label class="block text-gray-700 text-sm font-bold mb-2" for="username">Username:</label>
            <input class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" id="username" type="text" v-model="username" required>
          </div>
          <div class="mb-6">
            <label class="block text-gray-700 text-sm font-bold mb-2" for="password">Password:</label>
            <input class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" id="password" type="password" v-model="password" required>
          </div>
          <div class="flex items-center justify-between">
            <button class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline" type="submit">
              Login
            </button>
          </div>
        </form>
        <div v-if="errorMessage" class="mt-4 text-red-500">{{ errorMessage }}</div>
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
    methods: {
      login() {
        if (!this.username || !this.password) {
          this.errorMessage = 'Please enter both username and password';
          return;
        }
        console.log('Logged in with:', this.username, this.password);
        // After successful login, you can redirect the user to another page
        // For example, using Vue Router: this.$router.push('/dashboard');
      }
    }
  };
  </script>
  

<style>
</style>