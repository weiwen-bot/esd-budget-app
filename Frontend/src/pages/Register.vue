<template> 
    <div> 
      <h1>Create Your Account</h1> 
      <div> 
        <label for="username">Username:</label> 
        <input type="text" id="username" v-model="username" /> 
      </div> 
      <div> 
        <label for="mobileNumber">Mobile Number:</label> 
        <input type="text" id="mobileNumber" v-model="mobileNumber" /> 
      </div> 
      <div> 
        <label for="accountNumber">Account Number:</label> 
        <input type="text" id="accountNumber" v-model="accountNumber" /> 
      </div> 
      <div> 
        <label for="password">Password:</label> 
        <input type="password" id="password" v-model="password" /> 
      </div> 
      <button @click="register">Register</button> 
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