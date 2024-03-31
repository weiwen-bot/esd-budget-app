<template>
  <div>
    <h1>Create a New Pool</h1>
    <div>
      <label for="poolName">Pool Name:</label>
      <input class="shadow appearance-none border rounded w-64 py-2 px-3 text-black leading-tight focus:outline-none focus:shadow-outline bg-white" type="text" id="poolName" v-model="poolName" />
    </div>
    <div>
      <label for="poolType">Pool Type:</label>
      <select class="shadow appearance-none border rounded w-64 py-2 px-3 text-black leading-tight focus:outline-none focus:shadow-outline bg-white" id="poolType" v-model="poolType">
        <option value="payment">Payment</option>
        <option value="fund">Fund</option>
      </select>
    </div>
    <div>
      <label for="targetBudget">Target Budget:</label>
      <input class="shadow appearance-none border rounded w-64 py-2 px-3 text-black leading-tight focus:outline-none focus:shadow-outline bg-white" type="number" id="targetBudget" v-model="targetBudget" />
    </div>
    <div>
      <label for="expiryDate">Expiry Date:</label>
      <input class="shadow appearance-none border rounded w-64 py-2 px-3 text-black leading-tight focus:outline-none focus:shadow-outline bg-white" type="date" id="expiryDate" v-model="expiryDate" />
    </div>
    <button @click="createPool" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline mt-4">
      Create Pool
    </button>
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