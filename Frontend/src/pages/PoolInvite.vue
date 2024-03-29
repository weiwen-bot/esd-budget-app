<template>
  <div class="flex justify-center items-center h-screen">
    <div class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4 w-full max-w-xs relative">
      <div class="absolute left-3">
      <router-link to="/" class="text-black hover:text-blue-700 text-lg">&lt; </router-link>   
      </div>
      <h1 class="text-2xl mb-4">Pool Invitations</h1>
      <div v-if="pools.length > 0">
        <div v-for="(pool, index) in pools" :key="pool.id">
          <p><strong>Pool Number:</strong> {{ index + 1 }}</p>
          <button @click="acceptInvitation(pool)" class="accept-button">Accept</button>
          <button @click="declineInvitation(pool)" class="decline-button">Decline</button>
        </div>
      </div>
      <div v-else>
        <p>No pool invitations</p>
      </div>
    </div>
  </div>
</template>
   
  <script> 
  export default { 
    name: 'PoolInvitePage', 
    data() { 
      return { 
        pools: [
        {
          id: 1,
          name: 'Pool 1',
        },
        {
          id: 2,
          name: 'Pool 2',
        },
        {
          id: 3,
          name: 'Pool 3',
        },
      ],
    };
      ; 
    }, 
    created() { 
      this.fetchPoolInvitations(); 
    }, 
    methods: { 
      async fetchPoolInvitations() { 
        try { 
          const response = await fetch('http://localhost:5005/PoolInvitations'); // Adjust URL as needed 
          resob
          const data = await response.json(); 
          if (response.ok) { 
            this.pools = data.data.pools; 
          } else { 
            console.error('Failed to fetch pool invitations:', data.message); 
          } 
        } catch (error) { 
          console.error('Error fetching pool invitations:', error); 
        } 
      }, 
      async acceptInvitation(pool) { 
        // Implement logic to accept the invitation for the specified pool 
        console.log('Accepted invitation for pool:', pool); 
      }, 
      async declineInvitation(pool) { 
        // Implement logic to decline the invitation for the specified pool 
        console.log('Declined invitation for pool:', pool); 
      } 
    } 
  }; 
  </script> 
   
  <style> 
  /* Add your styles here if needed */ 
  .accept-button { 
    background-color: #28a745; 
    color: white; 
    border: none; 
    padding: 5px 10px; 
    margin-right: 5px; 
    cursor: pointer; 
  } 
   
  .decline-button { 
    background-color: #dc3545; 
    color: white; 
    border: none; 
    padding: 5px 10px; 
    cursor: pointer; 
  } 
  </style>