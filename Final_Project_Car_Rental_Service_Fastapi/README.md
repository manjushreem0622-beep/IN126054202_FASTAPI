🚗 **Car Rental Service API**

A fully functional REST API built using FastAPI that simulates a real-world car rental system.
This project allows users to manage cars, customers, and bookings with features like booking lifecycle, filtering, sorting, and pagination.

📌 **Features**
🚘 **Car Management**
    • Add new cars
    • View all cars (with pagination)
    • Get car by ID
    • Update car details
    • Delete car
    • View available cars
    
👤 **Customer Management**
    • Add new customers
    • View all customers
    • Update customer details
    • Delete customer
    
📅 **Booking Management**
    • Create booking
    • View all bookings
    • Get booking by ID
    • Update booking
    • Delete booking
    • Confirm booking
    • Pickup car
    • Return car
    
🔍 **Advanced Features**
    • Search & filter bookings
    • Sorting (by total_amount / days)
    • Pagination support
    • Validation using Pydantic
    • Error handling (404, 422)
    
🛠️ **Tech Stack**
    • Python
    • FastAPI
    • Uvicorn
    • Pydantic

**📌 Project Highlights**
- Implemented complete booking lifecycle
- Designed real-world business logic
- Integrated search, sorting, pagination
- Structured API with clean endpoints

▶️ **How to Run**
Install dependencies:
pip install fastapi uvicorn

Run the server:
uvicorn main:app --reload

Open in browser:
http://127.0.0.1:8000/docs

**📌 API Overview**
🚘 Cars
GET /cars → Get all cars
GET /cars/{id} → Get car by ID
POST /cars → Add new car
PUT /cars/{id} → Update car
DELETE /cars/{id} → Delete car
GET /cars/available/list → Get available cars

👤 **Customers**
GET /customers → Get all customers
GET /customers/{id} → Get customer by ID
POST /customers → Add customer
PUT /customers/{id} → Update customer
DELETE /customers/{id} → Delete customer

📅 **Bookings**
POST /bookings → Create booking
GET /bookings → View all bookings
GET /bookings/{id} → Get booking by ID
PUT /bookings/{id} → Update booking
DELETE /bookings/{id} → Delete booking

🔄 **Booking Workflow**
PATCH /bookings/{id}/confirm → Confirm booking
PATCH /bookings/{id}/pickup → Pickup car
PATCH /bookings/{id}/return-car → Return car

**🔍 Advanced Features**
GET /cars → Filtering, sorting, pagination
GET /bookings/search/filter → Search & filter bookings

💡 **Business Logic**
Car must be available before booking
Total amount is calculated based on rent per day and number of days
Booking status flow:
pending → confirmed → picked_up → returned
Car availability becomes false when picked up and true when returned
Cars/customers with active bookings cannot be deleted

💰 **Discount & Coupon Feature**
**Discount Endpoint**
GET /bookings/{booking_id}/discount
**Coupon Endpoint**
GET /bookings/{booking_id}/apply-coupon
 Available Coupons:
 CODE10 → 10%
 SAVE20 → 20%
 MEGA30 → 30%

📊 **Sample Data**
  Cars
    • Hyundai i20
    • Maruti Swift
    • Honda City
    • Tata Nexon
    • Kia Seltos
    • Toyota Innova Crysta
  Customers
    • Rahul Sharma
    • Sneha Reddy
    • Manjushree  

🧪 **Testing**
All endpoints were tested using Swagger UI:
Valid and invalid inputs checked
Error handling (404, 400, 422) verified
Workflow (pending → confirmed → picked up → returned) tested

⭐ **Conclusion**
    This project demonstrates:
      • REST API development using FastAPI
      • Real-world system design
      • Clean backend structure
      • Validation and error handling

🙋 **Author**
Manjushree M
FastAPI Internship Project
