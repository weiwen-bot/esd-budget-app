import { defineStore } from 'pinia';

import axios from 'axios';

export const useAuthStore = defineStore({
    id: 'auth',
    state: () => ({
        // initialize state from local storage to enable user to stay logged in
        user: localStorage.getItem('username'),
        userID: localStorage.getItem('userid'),
        userData : null,
    }),
    persist: true,
    actions: {
        async login(username, password) {
            
            try {
                this.userData = await axios.post('http://127.0.0.1:5004/login',{"UserName":username,"Password":password})
                console.log(this.userData)
                this.userID = this.userData.data.data.UserID
                this.user = this.userData.data.data.UserName
                // store user details and jwt in local storage to keep user logged in between page refreshes
                
                localStorage.setItem('username',username);
                localStorage.setItem('userid',this.userID);
                return this.userData
            } catch (error) {
                // let the form component display the error
                console.log(error)
                return null
            }

        },
        logout() {
            this.user = null;
            this.userID = null;
            localStorage.removeItem('userid');
            localStorage.removeItem('username');
            this.$router.push('/Login');
        }
    }
});