<template>
    <div class="container mx-auto p-4">
        <h1 class="text-2xl font-bold mb-4">Notifications</h1>
        <div v-if="notifications.length === 0" class="mb-2">You have no notifications</div>
        <div v-else class="mb-2">You have <strong>{{ notifications.length }}</strong> notification(s).</div>
        <div class="grid grid-cols-1 gap-4">
        <div v-for="(notification, index) in notifications" :key="index" class="bg-white shadow-md rounded-md p-4 relative">
            <button @click="deleteNotification(index)" class="text-red-500 relative top-0 left-0 text-xs">
                X
            </button>
          <p>{{ notification }}</p>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'Notifications',
    data() {
      return {
        notifications: [
          'User contributed to "Japan Trip" pool.',
          'Boris deleted Bubble Tea pool',
          'User declined your invitation to "Bubble Tea" pool.'
        ]
      };
    },
    methods: {
    deleteNotification(index) {
      this.notifications.splice(index, 1);
    }
  }
  };
  </script>
  
  <style>
  .container {
    margin-left: auto;
    margin-right: auto;
    padding-left: 1rem;
    padding-right: 1rem;
  }
  
  .text-2xl {
    font-size: 1.5rem;
  }
  
  .font-bold {
    font-weight: 700;
  }
  
  .mb-4 {
    margin-bottom: 1rem;
  }
  
  .grid {
    display: grid;
  }
  
  .grid-cols-1 {
    grid-template-columns: repeat(1, minmax(0, 1fr));
  }
  
  .bg-white {
    background-color: #ffffff;
  }
  
  .shadow-md {
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  }
  
  .rounded-md {
    border-radius: 0.375rem;
  }
  
  .p-4 {
    padding: 1rem;
  }
  </style>
  