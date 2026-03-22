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
Manju Shree
FastAPI Internship Project
