<template>
  <div class="container mx-auto p-4 relative">
    <div class="absolute left-6">
      <router-link to="/" class="text-black hover:text-blue-700 text-lg">&lt; </router-link>
    </div>
    <h1 class="text-2xl font-bold mb-4">Notifications</h1>
    <div v-if="notification.length + request.length === 0" class="mb-2">You have no notifications</div>
    <div v-else class="mb-2">You have <strong>{{ notifications.length }}</strong> notification(s)</div>
    <div class="grid gap-4">

      <div v-for="(notification, index) in request" :key="index" class="bg-white shadow-md rounded-md p-4">
        <p class="text-xs text-gray-500 mb-2">{{ daysAgo(notification.notificationDate) }}</p>


          <p>You have been invited to join {{ notification.pool.name }} by {{ notification.pool.userName }}</p>
          <div class="flex justify-between mt-2">
            <button @click="acceptInvite(notification)" class="btn btn-accept">Accept</button>
            <button @click="declineInvite(notification)" class="btn btn-decline">Decline</button>
          </div>


    

      </div>

      <div v-for="(notification, index) in notifications" :key="index" class="bg-white shadow-md rounded-md p-4">
        <p class="text-xs text-gray-500 mb-2">{{ daysAgo(notification.date) }}</p>

        <div v-if="notification.type === 'invite'">
          <p>You have been invited to join {{ notification.pool.name }} by {{ notification.pool.userName }}</p>
          <div class="flex justify-between mt-2">
            <button @click="acceptInvite(notification)" class="btn btn-accept">Accept</button>
            <button @click="declineInvite(notification)" class="btn btn-decline">Decline</button>
          </div>
        </div>

        <div v-else>
          <p>{{ notification.message }}</p>
        </div>

      </div>


    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { mapStores } from 'pinia';
import { useAuthStore } from '../store/authStore';
import { useUsersStore } from '../store/userStore';

export default {
  name: 'NotificationsPage',
  data() {
    return {
      userid: '',
      data:[],
      notification: [

      ],
      request:[

      ]

      // notifications: [
      //   { id: 1, type: 'invite', date: '2024-3-30', pool: { name: 'Japan Trip', userName: 'John22'}},
      //   { id: 3, type: 'message', message: 'You have a new message',date: '2024-3-25'},
      //   { id: 2, type: 'invite', date: '2024-3-22', pool: { name: 'Mcdonald Thursday', userName: 'Dave3'} },
  
      // ]
    };
  },
  computed: {
    // computed
    ...mapStores(useAuthStore),
    ...mapStores(useUsersStore),
  },
  methods: {
    acceptInvite(invite) {
      console.log('Accepted invite:', invite);
    },
    declineInvite(invite) {
      console.log('Declined invite:', invite);
    },
    daysAgo(dateString) {
      const today = new Date();
      const inviteDate = new Date(dateString);
      const diffTime = today.getTime() - inviteDate.getTime();
      const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24));

      if (diffDays === 0) {
        return "Today";
      } else if (diffDays === 1) {
        return "1 day ago";
      } else {
        return `${diffDays} days ago`;
      }
    },
  },
  async created(){
    const authStore = useAuthStore();
    const userStore = useUsersStore();
    this.userid = authStore.userID;

    this.data = await userStore.getUserNoti(this.userid);
    this.notification = this.pools.data.data.data.notif
    this.request = this.pools.data.data.data.request

  }
};
</script>

  
  <style>

  .btn-accept {
    background-color: #34d399; 
    color: white; 
    font-weight: bold;
    padding: 0.5rem 1rem;
    border-radius: 0.375rem;
  }

  .btn-decline {
    background-color: #ef4444; 
    color: white; 
    font-weight: bold;
    padding: 0.5rem 1rem;
    border-radius: 0.375rem;
  }
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
  