<template>
  <div>
    <h1 class="text-2xl font-bold mb-4">Create a New Pool</h1>
    <div class="card grid grid-cols-1 gap-y-4 items-center mt-4"> <!-- Adjusted margin -->
      <div class="flex flex-col items-center"> <!-- Center the content -->
        <label for="poolName" class="mr-2">Pool Name:</label>
        <input class="shadow appearance-none border rounded w-64 py-2 px-3 text-black leading-tight focus:outline-none focus:shadow-outline bg-white text-center" type="text" id="poolName" v-model="poolName" />
      </div>
      <div class="flex flex-col items-center"> <!-- Center the content -->
        <label for="poolType" class="mr-2">Pool Type:</label>
        <select class="shadow appearance-none border rounded w-64 py-2 px-3 text-center text-black leading-tight focus:outline-none focus:shadow-outline bg-white" id="poolType" v-model="poolType">
          <option value="payment">Payment</option>
          <option value="fund">Fund</option>
        </select>
      </div>
      <div class="flex flex-col items-center"> <!-- Center the content -->
        <label for="targetBudget" class="mr-2">Target Budget:</label>
        <input class="shadow appearance-none border rounded w-64 py-2 px-3 text-black leading-tight focus:outline-none focus:shadow-outline bg-white text-center" type="number" id="targetBudget" v-model="targetBudget" />
      </div>
      <div class="flex flex-col items-center"> <!-- Center the content -->
        <label for="expiryDate" class="mr-2">Expiry Date:</label>
        <input class="shadow appearance-none border rounded w-64 py-2 px-3 text-black leading-tight focus:outline-none focus:shadow-outline bg-white text-center" type="date" id="expiryDate" v-model="expiryDate" />
      </div>
      <div class="flex justify-center w-full"> <!-- Center the button -->
        <button @click="createPool" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline mt-4 w-48">
          Create Pool
        </button>
      </div>
    </div>
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