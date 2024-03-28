<template> 
    
  <div class="flex justify-center items-center h-screen">
    <div class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4 w-full max-w-xs relative">
      <div class="absolute left-3">
      <router-link to="/login" class="text-black hover:text-blue-700 text-lg">&lt; </router-link>   
      </div>
      <h1 class="text-2xl mb-4">Create Account</h1>
        <div class="mb-4">
          <label for="username" class="block text-gray-700 text-sm font-bold mb-2">Username:</label>
          <input id="username" type="text" v-model="username" class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" />
        </div>
        <div class="mb-4">
          <label for="mobileNumber" class="block text-gray-700 text-sm font-bold mb-2">Mobile Number:</label>
          <input id="mobileNumber" type="text" v-model="mobileNumber" class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" />
        </div>
        <div class="mb-4">
          <label for="accountNumber" class="block text-gray-700 text-sm font-bold mb-2">Account Number:</label>
          <input id="accountNumber" type="text" v-model="accountNumber" class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" />
        </div>
        <div class="mb-6">
          <label for="password" class="block text-gray-700 text-sm font-bold mb-2">Password:</label>
          <input id="password" type="password" v-model="password" class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" />
        </div>
      <button @click="register" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline">Register</button>
    </div>
  </div>
</template> 
   
  <script> 
  export default { 
    name: 'RegisterPage', 
    data() { 
      return { 
        username: '', 
        mobileNumber: '', 
        accountNumber: '', 
        password: '' 
      }; 
    }, 
    methods: { 
      register() { 
        console.log('Registering user'); 
        // Register user code 
      } 
    } 
  }; 
  </script> 
   
  <style> 
  </style>