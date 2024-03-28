<template>

    <div class="container mx-auto p-4">
        <h1 class="text-2xl font-bold mb-4">Pool Details</h1>
        <div class="bg-white shadow-md rounded-md p-4">
            <div class="border-b-2 border-gray-400 mb-4 pb-2">
                <h2 class="text-lg font-semibold">{{ pool.name }}</h2>
            </div>
            <div class="mb-4">
                <p class="mb-4"><strong>Description:</strong><br> {{ pool.description }}</p>
                <p class="mb-4"><strong>Category:</strong><br>{{ pool.category }}</p>
                <p class="mb-4"><strong>Expiry Date:</strong><br>{{ pool.expiryDate }}</p> 
            </div>
            <div class="mb-4">
                <p><strong>Progress:</strong></p>
                <p>${{ pool.currentAmount }} / ${{ pool.totalAmount }}</p>
                <div class="progress-bar-container">
                    <div class="progress-bar" :style="{ width: `${pool.currentAmount/pool.totalAmount * 100}%` }"></div>
                </div>
            </div>
            <div class="flex justify-center mb-4 space-x-4">
                <button @click="makePayment" class="make-payment-btn">Make Payment</button>
                <button @click="refund" class="make-payment-btn">Refund</button>
            </div>
            <div class="flex justify-center mb-4 space-x-4">
                <button @click="collect" class="make-payment-btn">Collect</button>
                <button @click="deletePool" class="make-payment-btn">Delete</button>
            </div>
          <p class="mb-4"><strong>Transaction History:</strong><br></p>
          <div class="overflow-x-auto">
        <table class="table-auto w-full">
          <thead>
            <tr>
              <th class="border px-4 py-2">Date</th>
              <th class="border px-4 py-2">UserID</th>
              <th class="border px-4 py-2">Amount</th>
              <th class="border px-4 py-2">Description</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(transaction, index) in transactions" :key="transaction.id" :class="{ 'bg-gray-300': index % 2 === 0 }">
              <td class="border px-4 py-2">{{ transaction.date }}</td>
              <td class="border px-4 py-2">{{ transaction.userID }}</td>
              <td class="border px-4 py-2">${{ transaction.amount }}</td>
              <td class="border px-4 py-2">{{ transaction.description }}</td>
            </tr>
          </tbody>
        </table>
      </div>
          
      </div>
    </div> 
  
  </template>
      

<script>
export default {
    name: 'OwnerPoolPage',
    data() {
    return {
      pool: {
        id: 1,
        name: 'Japan Trip',
        category: 'Fund',
        description: 'Japan Trip after Finals',
        currentAmount: 1200,
        totalAmount: 5000,
        expiryDate: '2025-01-03',
      },
      transactions: [
        { id: 1, date: '2022-01-01', amount: 800, description: 'Transaction 1',userID:3 },
        { id: 2, date: '2022-01-05', amount: 200, description: 'Transaction 2',userID: 1 },
        { id: 3, date: '2022-01-06', amount: 200, description: 'Transaction 3',userID: 1 }
      ]
    };
  },
    created() {
        this.fetchPoolDetails();
        this.fetchTransactionHistory();
    },
    methods: {
        async fetchPoolDetails() {
            try {
                const response = await fetch('http://microservice-url:port/pool-details'); // Replace 'microservice-url' and 'port' with your actual microservice URL and port
                const data = await response.json();
                if (response.ok) {
                    this.pool = data;
                } else {
                    console.error('Failed to fetch pool details:', data.message);
                }
            } catch (error) {
                console.error('Error fetching pool details:', error);
            }
        },
        async fetchTransactionHistory() {
            try {
                const response = await fetch('http://microservice-url:port/transaction-history'); // Replace 'microservice-url' and 'port' with your actual microservice URL and port
                const data = await response.json();
                if (response.ok) {
                    this.transactions = data;
                } else {
                    console.error('Failed to fetch transaction history:', data.message);
                }
            } catch (error) {
                console.error('Error fetching transaction history:', error);
            }
        },
        async makePayment() {
            // Make payment logic
        },
        refund() {
            // Refund logic
        },
        collect() {
            // Collect logic
        },
        deletePool() {
            // Delete pool logic
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

.font-semibold {
  font-weight: 600;
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

.make-payment-btn {
  background-color: #3b82f6;
  color: #fff;
  font-weight: 700;
  padding: 0.5rem 1rem;
  border-radius: 0.375rem;
}

.make-payment-btn:hover {
  background-color: #2563eb;
}

.progress-bar-container {
  width: 100%;
  background-color: #e5e7eb;
  border-radius: 0.375rem;
}

.progress-bar {
  height: 0.75rem;
  background-color: #4caf50;
  border-radius: 0.375rem;
}

ul {
  list-style-type: none;
  padding-left: 0;
}

li {
  margin-bottom: 0.5rem;
}


@media (min-width: 576px) {
  .grid-cols-1 {
    grid-template-columns: repeat(1, minmax(0, 1fr));
  }
  .grid-cols-2 {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
  .grid-cols-3 {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }
}
</style>
