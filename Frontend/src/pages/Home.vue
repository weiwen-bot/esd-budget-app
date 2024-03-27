<template>
  <div>
      <h1>HOME</h1>
      <button
                  type="button"
                  class="btn btn-primary btn-sm"
                  @click="handlePurchaseBook(book)">
                  Purchase
                </button>
  </div>
  <h1>Add Components</h1>
</template>


<script>
import axios from 'axios';
export default {
name: 'home',
data() {
  return {
    stripe: null,
  }
},
computed: {
},
methods: {
  getStripePublishableKey() {
    fetch('http://localhost:4242/config')
      .then((result) => result.json())
      .then((data) => {
        // Initialize Stripe.js
        this.stripe = Stripe(data.publicKey);
      });
  },
  handlePurchaseBook() {
    // Get Checkout Session ID
    fetch('http://127.0.0.1:4242/create-checkout-session', {
      method: 'POST',
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Expose-Headers':'*',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ user_id: '2', pool_id:'2' }),
    })
      .then((result) => result.json())
      .then((data) => {
        console.log(data);
        // Redirect to Stripe Checkout
        return this.stripe.redirectToCheckout({ sessionId: data.sessionId });
      })
      .then((res) => {
        console.log(res);
      });
  },
},
components: {},
created() {
  this.getStripePublishableKey();
},
}
</script>