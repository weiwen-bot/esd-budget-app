<template>
  <div class="container mx-auto p-4 relative">
    <div class="absolute left-6">
      <router-link to="/" class="text-black hover:text-blue-700 text-lg">&lt; </router-link>
    </div>
    <h1 class="text-2xl font-bold mb-4">Pool Invites</h1>
    <div v-if="poolInvites.length === 0" class="mb-2">You have no pending pool invites</div>
        <div v-else class="mb-2">You have <strong>{{ poolInvites.length }}</strong> pending pool invite(s).</div>
    <div class="grid gap-4">
      <div v-for="(invite, index) in poolInvites" :key="index" class="bg-white shadow-md rounded-md p-4">
  <p class="text-xs text-gray-500 mb-2">{{daysAgo(invite.pool.inviteDate) }}</p>
  <p>You have been invited to join {{ invite.pool.name }} by {{ invite.pool.userName }}</p>
  <div class="flex justify-between mt-2">
    <button @click="acceptInvite(invite)" class="btn btn-accept">Accept</button>
  <button @click="declineInvite(invite)" class="btn btn-decline">Decline</button>
  </div>
</div>

    </div>
  </div>
</template>

<script>
export default {
  name: 'PoolInvitePage',
  data() {
    return {
      poolInvites: [
        { id: 1, pool: { name: 'Japan Trip', userName: 'John22', inviteDate: '2024-3-24'}},
        { id: 2, pool: { name: 'Mcdonald Thursday', userName: 'Dave3', inviteDate: '2024-3-30'}, },
        { id: 3, pool: { name: 'Bubble Tea', userName: 'Boris', inviteDate: '2024-2-24'} }
      ]
    };
  },
  methods: {
    acceptInvite(invite) {
      // Handle accept invite logic
      console.log('Accepted invite:', invite);
    },
    declineInvite(invite) {
      // Handle decline invite logic
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

.border {
  border-width: 2px;
}

.rounded-md {
  border-radius: 0.375rem;
}

.shadow-md {
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

.p-4 {
  padding: 1rem;
}

.text-lg {
  font-size: 1.125rem;
}

.text-sm {
  font-size: 0.875rem;
}

.font-semibold {
  font-weight: 600;
}

.italic {
  font-style: italic;
}

.mb-2 {
  margin-bottom: 0.5rem;
}

.flex {
  display: flex;
}

.justify-between {
  justify-content: space-between;
}

.py-2 {
  padding-top: 0.5rem;
  padding-bottom: 0.5rem;
}

.px-4 {
  padding-left: 1rem;
  padding-right: 1rem;
}

.btn {
  font-weight: 700;
  padding: 0.5rem 1rem;
  border-radius: 0.375rem;
}

.btn:hover {
  cursor: pointer;
}

.bg-green-500 {
  background-color: #34d399;
}

.bg-green-700 {
  background-color: #22c08c;
}

.bg-red-500 {
  background-color: #ef4444;
}

.bg-red-700 {
  background-color: #dc2626;
}

.focus\:outline-none:focus {
  outline: none;
  box-shadow: 0 0 0 3px rgba(66, 153, 225, 0.5);
}

.focus\:shadow-outline:focus {
  box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.5);
}

.hover\:text-blue-700:hover {
  color: #2563eb;
}

.text-white {
  color: #fff;
}

.btn-accept {
  background-color: #34d399;
  color: white;
  font-weight: bold;
  padding: 0.5rem 1rem;
  border-radius: 0.375rem;
  width: 45%; /* Adjust the width as needed */
}

.btn-decline {
  background-color: #ef4444;
  color: white;
  font-weight: bold;
  padding: 0.5rem 1rem;
  border-radius: 0.375rem;
  width: 45%; /* Adjust the width as needed */
}

</style>
