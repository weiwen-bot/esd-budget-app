<template> 
    <div> 
      <h1>Create a New Pool</h1> 
      <div> 
        <label for="poolName">Pool Name:</label> 
        <input type="text" id="poolName" v-model="poolName" /> 
      </div> 
      <div> 
        <label for="poolType">Pool Type:</label> 
        <select id="poolType" v-model="poolType"> 
          <option value="payment">Payment</option> 
          <option value="fund">Fund</option> 
        </select> 
      </div> 
      <div> 
        <label for="targetBudget">Target Budget:</label> 
        <input type="number" id="targetBudget" v-model="targetBudget" /> 
      </div> 
      <div> 
        <label for="expiryDate">Expiry Date:</label> 
        <input type="date" id="expiryDate" v-model="expiryDate" /> 
      </div> 
      <button @click="createPool">Create Pool</button> 
    </div> 
  </template> 
   
  <script> 
  export default { 
    name: 'PoolCreation', 
    data() { 
      return { 
        poolName: '', 
        poolType: 'payment', 
        targetBudget: '', 
        expiryDate: '' 
      }; 
    }, 
    methods: { 
      createPool() { 
        console.log('Creating pool'); 
        // pool creating logic 
      } 
    } 
  }; 
  </script> 
   
  <style> 
  
  </style>