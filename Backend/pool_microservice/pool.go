package pool

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"github.com/gorilla/mux"
	"github.com/jinzhu/gorm"
)

// Define the Pool model structure
type Pool struct {
	PoolID        uint      `gorm:"primary_key;autoIncrement"`
	DateCreation  *time.Time `json:"DateCreation"`
	pool_name      string     `json:"pool_name"`
	pool_desc      string     `json:"pool_desc"`
	Expiry_Date    time.Time `json:"Expiry_Date"`
	Current_amount float64   `json:"Current_amount"`
	Budget        float64   `json:"Budget"`
	Pool_Type      string     `json:"Pool_Type"`
	UserID        uint      `json:"UserID"`
	Status        string     `json:"Status"`
}


// Define the PoolMapping model structure
type PoolMapping struct {
	PoolID uint `gorm:"primary_key"`
	UserID uint `gorm:"primary_key"`
}

// Initialize a global database connection variable
var db *gorm.DB

func init() {
	var err error
	db, err = gorm.Open("mysql", "root:@tcp(host.docker.internal:3306)/pool")
	if err != nil {
		log.Fatal(err)
	}

	// Migrate database schema 
	db.AutoMigrate(&Pool{}, &PoolMapping{})
}

func main() {
	router := mux.NewRouter()

	// API endpoint to create a new pool
	router.HandleFunc("/Pool", createPool).Methods("POST")

	// API endpoint to update an existing pool
	router.HandleFunc("/Pool/{PoolID}", updatePool).Methods("PUT")

	// API endpoint to get all pools
	router.HandleFunc("/Pool", getPools).Methods("GET")

	// API endpoint to get a specific pool by PoolID
	router.HandleFunc("/Pool/{PoolID}", getPool).Methods("GET")

	// API endpoint to delete a pool
	router.HandleFunc("/Pool/{PoolID}", deletePool).Methods("DELETE")

	log.Fatal(http.ListenAndServe(":5001", router))
}

func createPool(w http.ResponseWriter, r *http.Request) {
	var pool Pool
	decoder := json.NewDecoder(r.Body)
	err := decoder.Decode(&pool)
	if err != nil {
		w.WriteHeader(http.StatusBadRequest)
		fmt.Fprintln(w, "Invalid pool data")
		return
	}

	db.Create(&pool)
	w.WriteHeader(http.StatusCreated)
	json.NewEncoder(w).Encode(pool)
}

func updatePool(w http.ResponseWriter, r *http.Request) {
	vars := mux.Vars(r)
	poolID := mustAtoi(vars["PoolID"])

	var pool Pool
	decoder := json.NewDecoder(r.Body)
	err := decoder.Decode(&pool)
	if err != nil {
		w.WriteHeader(http.StatusBadRequest)
		fmt.Fprintln(w, "Invalid pool data")
		return
	}

	result := db.Model(&Pool{}).Where("PoolID = ?", poolID).Updates(&pool)
	if result.Error != nil {
		w.WriteHeader(http.StatusInternalServerError)
		fmt.Fprintln(w, result.Error)
		return
	}

	if result.RowsAffected == 0 {
		w.WriteHeader(http.StatusNotFound)
		fmt.Fprintln(w, "Pool not found")
		return
	}

	w.WriteHeader(http.StatusOK)
	json.NewEncoder(w).Encode(pool)
}