<template>
  <div class="flex justify-center items-center h-screen">
    <div class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4 w-full max-w-xs">
      <h1 class="text-2xl mb-4">Create a New Pool</h1>
      <div class="mb-4">
        <label class="block text-gray-700 text-sm font-bold mb-2" for="poolName">Pool Name:</label>
        <input class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" id="poolName" type="text" v-model="poolName" required>
      </div>
      <div class="mb-4">
        <label class="block text-gray-700 text-sm font-bold mb-2" for="poolType">Pool Type:</label>
        <select class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" id="poolType" v-model="poolType">
          <option value="payment">Payment</option>
          <option value="fund">Fund</option>
        </select>
      </div>
      <div class="mb-4">
        <label class="block text-gray-700 text-sm font-bold mb-2" for="targetBudget">Target Budget:</label>
        <input class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline " id="targetBudget" type="number" v-model="targetBudget" required>
        
      </div>
      <div class="mb-4">
        <label class="block text-gray-700 text-sm font-bold mb-2" for="expiryDate">Expiry Date:</label>
        <input class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" id="expiryDate" type="date" v-model="expiryDate" required>
      </div>
      <div class="flex items-center justify-center">
        <button class="border border-black text-black font-bold py-1 px-2 rounded focus:outline-none focus:shadow-outline text-sm" @click="showUserList =!showUserList">
          Add Participants
        </button>
      </div>
      <div v-if="showUserList" class="mt-4">
        <h2 class="text-lg font-semibold mb-2">Users:</h2>
        <div v-for="user in userList" :key="user.id" class="flex items-center mb-2">
          <input type="checkbox"  v-model="selectedUsers" :value="user.id" class="mr-2">
          <span class="text-center">{{ user.name }}</span>
        </div>
      </div>
      <div class="flex items-center justify-center mt-4">
        <button class="bg-blue-500 hover:bg-blue-700 text-white font-bold py- px-4 rounded focus:outline-none focus:shadow-outline" @click="createPool">
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
        expiryDate: '',
        userList: [ 
        { id: 1, name: 'User1' },
        { id: 2, name: 'User2' },
        { id: 3, name: 'User3' },
      ],
      showUserList: false,
      selectedUsers: []
      }; 
    }, 
    methods: { 
      createPool() { 
        console.log('Creating pool with selected users');
        console.log('Selected users:', this.selectedUsers);
  
        // pool creating logic 
      },
  }
}
  </script> 
   
  <style> 
  
  </style>