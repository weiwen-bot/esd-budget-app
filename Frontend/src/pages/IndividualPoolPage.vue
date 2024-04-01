<template>

  <div class="container mx-auto p-4 relative">
    <div class="absolute left-6">
      <router-link to="/" class="text-black hover:text-blue-700 text-lg">&lt; </router-link>
    </div>
    <h1 class="text-2xl font-bold mb-4">Pool Details</h1>
    <div class="bg-white shadow-md rounded-md p-4">
      <div class="border-b-2 border-gray-400 mb-4 pb-2">
        <div class="card-credit" @click="flipCard">
          <div class="card-inner" :class="{ flipped: isFlipped }">
            <div class="front">
              <img src="https://i.ibb.co/PYss3yv/map.png" class="map-img">
              <div class="row">
                <img src="https://i.ibb.co/G9pDnYJ/chip.png" width="60px" style="margin-top: 15px;">
                <img src="../assets/logo.png" width="250px" style="position: absolute; right:-50px; top: 5px;">
              </div>
              <div class="row card-no">
                <p >5244</p>
                <p >2150</p>
                <p >8252</p>
                <p >6420</p>
              </div>
              <div class="row card-holder">
                <p>CARD HOLDER</p>
                <p>VALID TILL</p>
              </div>
              <div class="row name">
                <p>MIKE CHANG</p>
                <p>10 / 25</p>
              </div>
            </div>
            <div class="back">
              <img src="https://i.ibb.co/PYss3yv/map.png" class="map-img">
              <div class="bar"></div>
              <div class="row card-cvv">
                <div>
                  <img src="https://i.ibb.co/S6JG8px/pattern.png">
                </div>
                <p>824</p>
              </div>

              <div class="row signature">
                <img src="../assets/signature.png" width="250px" style="position: absolute; left:10px; bottom:35px;">
                <img src="../assets/logo.png" width="250px" style="position: absolute; right:-50px; bottom:-10px;">
              </div>
            </div>
          </div>
        </div>
        <h2 class="text-lg font-semibold flex flex-col items-center justify-center">
          {{ pool.pool_name }}
        </h2>
        <h2 class="text-sm font-semibold italic black mt-2 mb-2">Created by {{ pool.UserID }}</h2>
        <div class="flex justify-center mt-2 mb-2">
          <button @click="toggleModal" style="margin: 0px; padding: 1px; border: 1px solid black; border-radius: 3px; background-color: #f8f8f8; box-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);" class="flex flex-col items-center">
          <span class="text-sm" style="margin:3px;">View Users</span>
          </button>
        </div>
      </div>
      <div class="mb-4">
  
        <p class="mb-4" style="color:black"><strong>Description:</strong><br> {{ pool.pool_desc}}</p>
        <p class="mb-4 text-black" style="color:black"><strong>Category:</strong><br>{{ pool.Pool_Type }}</p>
        <p class="mb-4 text-black" style="color:black"><strong>Created by:</strong><br>{{ pool.UserID }}</p>
      </div>
      <div class="mb-4">
        <p><strong>Progress:</strong></p>
        <p style="color:black">${{ pool.Current_amount }} / ${{ pool.Budget }}</p>
        <div class="progress-bar-container">
          <div class="progress-bar"
            :style="{ width: `${calculateProgressPercentage(pool.Current_amount, pool.Budget)}` }"></div>
        </div>
      </div>
      <div class="flex justify-center mb-4">
        <button @click="makePayment" class="make-payment-btn">Contribute</button>
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
            <tr v-for="(transaction, index) in transactions" :key="transaction.id"
              :class="{ 'bg-gray-300': index % 2 === 0 }">
              <td class="border px-4 py-2">{{ transaction.date }}</td>
              <td class="border px-4 py-2">{{ transaction.userID }}</td>
              <td class="border px-4 py-2">${{ transaction.amount }}</td>
              <td class="border px-4 py-2">{{ transaction.description }}</td>
            </tr>
          </tbody>
        </table>
      </div>

    </div>
    <div v-if="showModal" class="modal">
    <div class="modal-content">
      <span class="close" @click="toggleModal">&times;</span>
      <h2 class="text-center"><strong>Participants</strong></h2>
      <p>There are {{ users.length }} participants</p>
      <table class="border-collapse border border-gray-400">
        <thead>
          <tr>
            <th class="border border-gray-400 px-4 py-2">S/N</th>
            <th class="border border-gray-400 px-4 py-2">Username</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(user, index) in users" :key="index" class="border border-gray-400">
            <td class="border border-gray-400 px-4 py-2">{{ index + 1 }}</td>
            <td class="border border-gray-400 px-4 py-2">{{ user }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
  </div>
  

</template>

<script>
export default {
  name: 'IndividualPoolPage',
  props: ['poolID'],
  data() {
    return {
      isFlipped: false,
      pool: {
        id: 1,
        userName: "John44",
        name: 'Japan Trip',
        category: 'Fund',
        description: 'Japan Trip after Finals',
        currentAmount: 1200,
        totalAmount: 5000,
        expiryDate: '2025-01-03',

      },
      users: ['232323', '2323232', '2323'],
      showModal: false,
      transactions: [
        { id: 1, date: '2022-01-01', amount: 800, description: 'Transaction 1', userID: 3 },
        { id: 2, date: '2022-01-05', amount: 200, description: 'Transaction 2', userID: 1 },
        { id: 3, date: '2022-01-06', amount: 200, description: 'Transaction 3', userID: 1 }
      ],

    };
  },
  created() {
    const poolID = this.$route.params.poolID;
    this.fetchPoolDetails();
    this.fetchTransactionHistory();
    console.log('PoolID:', this.poolID);
  },
  methods: {
    toggleModal() {
      this.showModal = !this.showModal;
    },
    async fetchPoolDetails(poolID) {
  try {
    const response = await fetch(`http://127.0.0.1:5001/Pool/${this.poolID}`);
    const data = await response.json();
    if (response.ok) {
      this.pool = data.data;
    } else {
      console.error('Failed to fetch pool details:', data.message);
    }
  } catch (error) {
    console.error('Error fetching pool details:', error);
  }
},

    async fetchTransactionHistory() {
      try {
        const response = await fetch('http://localhost:5005/TransactionHistory/1'); // Replace '1' with the actual pool ID
        const data = await response.json();
        if (response.ok) {
          this.transactions = data.data.transactions;
        } else {
          console.error('Failed to fetch transaction history:', data.message);
        }
      } catch (error) {
        console.error('Error fetching transaction history:', error);
      }
    },
    async makePayment() {
      try {
        const response = await fetch('http://localhost:5100/pool_management', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            poolID: 1, // Replace '1' with the actual pool ID
            userID: 1, // User ID = 1 
            amount: 100 // Replace '100' with the actual payment amount
          })
        });
        const data = await response.json();
        if (response.ok) {
          alert('Payment successful');
          // Optionally, you can update the pool details or transaction history after payment
          // this.fetchPoolDetails();
          // this.fetchTransactionHistory();
        } else {
          console.error('Failed to make payment:', data.message);
        }
      } catch (error) {
        console.error('Error making payment:', error);
      }
    },
    calculateProgressPercentage(currentAmount, totalAmount) {
      return (currentAmount / totalAmount) * 100 + '%';
    },
    flipCard() {
      this.isFlipped = !this.isFlipped;
    },
  }
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=josefin+Sans:wght@400;500;600;700&display=swap');

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

.modal {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: white;
  border-radius: 0.375rem;
  padding: 2rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  z-index: 1000;
  max-width: 500px;
}

.modal-content {
  background-color: white;
  padding: 50px;
  border: 1px solid #888;
  text-align: center;
  width: 100%;
}

.close {
  color: #aaa;
  position: absolute;
  top: 1rem;
  right: 1rem;
  font-size: 1.5rem;
  font-weight: bold;
  cursor: pointer;
}

.close:hover,
.close:focus {
  color: black;
  text-decoration: none;
  cursor: pointer;
}


* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: 'Josefin Sans', sans-serif;
}

.container-credit {
  min-height: 100vh;
  width: 100%;
  background: #000;
  display: flex;
  align-items: center;
  justify-content: center;
}

.card-credit {
  width: 500px;
  height: 300px;
  color: #fff;
  cursor: pointer;
  perspective: 1000px;
  margin-bottom: 20px;
  
}

.card-inner {
  width: 100%;
  height: 100%;
  position: relative;
  transition: transform 1s;
  transform-style: preserve-3d;
}

.front,
.back {
  width: 100%;
  height: 100%;
  background-image: linear-gradient(45deg, black, black);
  position: absolute;
  top: 0;
  left: 0;
  padding: 20px 30px;
  border-radius: 15px;
  overflow: hidden;
  z-index: 1;
  backface-visibility: hidden;
}

.row {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.map-img {
  width: 100%;
  position: absolute;
  top: 0;
  left: 0;
  opacity: 0.5;
  z-index: -1;
}

.card-no {
  font-size: 20px;
  margin-top: 50px;
  font-weight: bold;;
  font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
}

.card-holder {
  font-size: 12px;
  margin-top: 40px;
}

.name {
  font-size: 22px;
  
}

.bar {
  background: #222;
  margin-left: -30px;
  margin-right: -30px;
  height: 60px;
  margin-top: 10px;
}

.card-cvv {
  margin-top: 20px;
}

.card-cvv div {
  flex: 1;
}

.card-cvv img {
  width: 100%;
  display: block;
  line-height: 0;
}

.card-cvv p {
  background: #fff;
  color: #000;
  font-size: 22px;
  padding: 10px 20px;
}

.card-text {
  margin-top: 30px;
  font-size: 14px;
}

.signature {
  margin-top: 60px;
}

.back {
  transform: rotateY(180deg);
}

.card-credit:hover .card-inner {
  transform: rotateY(-180deg);
}

p{
  color: white;
}

</style>