<template>
  <div class="flex justify-center">
    <div class="border-2 border-gray-300 rounded-lg shadow-md px-6 pt-6 pb-8 mb-4 w-full max-w-xs">
      <h1 class="text-2xl font-bold mb-4 text-gray-800">Login</h1>
      <form @submit.prevent="login" class="card flex flex-col items-center">
        <div>
        <div class="mb-4">
          <label class="block text-gray-700 text-sm font-bold mb-1" for="username">Username: </label>
          <input class="w-full px-3 py-2 border rounded-md focus:outline-none focus:shadow-outline-blue focus:ring focus:ring-blue-400" id="username" type="text" v-model="username" required>
        </div>
        <div class="mb-6">
          <div class="mb-4">
            <label class="block text-gray-700 text-sm font-bold mb-1" for="password">
              Password:
            </label>
            <input class="w-full px-3 py-2 border rounded-md focus:outline-none focus:shadow-outline-blue focus:ring focus:ring-blue-400" id="password" type="password" v-model="password" required>
          </div>
        </div>
        <div class="flex items-center justify-center">
          <button class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline" type="submit">
            Login
          </button>
        </div>
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

*{
  color:black;
}

</style>