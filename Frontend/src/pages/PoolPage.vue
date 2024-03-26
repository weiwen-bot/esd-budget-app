<template> 
 
  <div> 
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark"> 
      <div class="container-fluid"> 
        <a class="navbar-brand" href="#">Navbar</a> 
        <button 
          class="navbar-toggler" 
          type="button" 
          data-bs-toggle="collapse" 
          data-bs-target="#navbarNav" 
          aria-controls="navbarNav" 
          aria-expanded="false" 
          aria-label="Toggle navigation" 
        > 
          <span class="navbar-toggler-icon"></span> 
        </button> 
        <div class="collapse navbar-collapse" id="navbarNav"> 
          <ul class="navbar-nav"> 
            <li class="nav-item"> 
              <router-link class="nav-link" to="/">Home</router-link> 
            </li> 
            <li class="nav-item"> 
              <router-link class="nav-link" to="/about">About</router-link> 
            </li> 
            <li class="nav-item"> 
              <router-link class="nav-link" to="/contact">Contact</router-link> 
            </li> 
          </ul> 
        </div> 
      </div> 
    </nav> 
  </div> 
 
   
 
 
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
        'Content-Type': 'application/json', 
      }, 
      body: JSON.stringify({ book_id: '2' }), 
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
