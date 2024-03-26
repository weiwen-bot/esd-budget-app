
## Download CLI and Log in to the Stripe Account 
Full Name: esdbudgetmain
Email : weiwen.tan.2022@smu.edu.sg
pwd: esd_buDgET_2024@

1) Download the [CLI](https://docs.stripe.com/stripe-cli) and login with the Stripe account
```
stripe Login
```
2) Listen for events from webhooks
```
stripe listen --forward-to localhost:4242/webhook
```

3) Trigger events with CLI
```
stripe trigger payment_intent.succeeded
```

It should show Trigger has been successful