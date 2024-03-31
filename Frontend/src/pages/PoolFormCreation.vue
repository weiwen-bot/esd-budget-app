<template>
  <div>
    <div class="absolute left-15 top-18">
      <router-link to="/" class="text-black hover:text-blue-700 text-lg">&lt;</router-link>
    </div>
    <h1 class="text-2xl font-bold mb-4">Create a New Pool</h1>
    <div class="card grid grid-cols-1 gap-y-4 items-center mt-4"> 
      <div class="flex flex-col items-center"> 
        <label for="poolName" class="mr-2">Pool Name:</label>
        <input class="shadow appearance-none border rounded w-64 py-2 px-3 text-black leading-tight focus:outline-none focus:shadow-outline bg-white text-center" type="text" id="poolName" v-model="poolName" />
      </div>
      <div class="flex flex-col items-center"> 
        <label for="poolType" class="mr-2">Pool Type:</label>
        <select class="shadow appearance-none border rounded w-64 py-2 px-3 text-center text-black leading-tight focus:outline-none focus:shadow-outline bg-white" id="poolType" v-model="poolType">
          <option value="payment">Payment</option>
          <option value="fund">Fund</option>
        </select>
      </div>
      <div class="flex flex-col items-center"> 
        <label for="targetBudget" class="mr-2">Target Budget:</label>
        <input class="shadow appearance-none border rounded w-64 py-2 px-3 text-black leading-tight focus:outline-none focus:shadow-outline bg-white text-center" type="number" id="targetBudget" v-model="targetBudget" />
      </div>
      <div class="flex flex-col items-center"> 
        <label for="expiryDate" class="mr-2">Expiry Date:</label>
        <input class="shadow appearance-none border rounded w-64 py-2 px-3 text-black leading-tight focus:outline-none focus:shadow-outline bg-white text-center" type="date" id="expiryDate" v-model="expiryDate" />
      </div>
      <div class="flex items-center justify-center">
        <button class="border border-black text-black font-bold py-1 px-2 rounded focus:outline-none focus:shadow-outline text-sm" @click="showUserList =!showUserList">
          Add Participants
        </button>
      </div>
      <div v-if="showUserList" class="mt-4 ">
        <h2 class="text-lg font-semibold mb-2">Users:</h2>
        <div v-for="user in userList" :key="user.id" class="mb-2">
          <input type="checkbox"  v-model="selectedUsers" :value="user.id" class="mr-2">
          <span>{{ user.name }}</span>
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