from fastapi import FastAPI, HTTPException, Query, status
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List

app = FastAPI(title="Car Rental Service API")


# ═══════════════════════════════════════════════════════════════
# PYDANTIC MODELS
# ═══════════════════════════════════════════════════════════════

class CarCreate(BaseModel):
    brand: str = Field(..., min_length=2, max_length=50)
    model: str = Field(..., min_length=1, max_length=50)
    year: int = Field(..., ge=2000, le=2035)
    rent_per_day: int = Field(..., gt=0)
    fuel_type: str = Field(..., min_length=3, max_length=20)
    transmission: str = Field(..., min_length=3, max_length=20)
    available: bool = True


class CarUpdate(BaseModel):
    brand: str = Field(..., min_length=2, max_length=50)
    model: str = Field(..., min_length=1, max_length=50)
    year: int = Field(..., ge=2000, le=2035)
    rent_per_day: int = Field(..., gt=0)
    fuel_type: str = Field(..., min_length=3, max_length=20)
    transmission: str = Field(..., min_length=3, max_length=20)
    available: bool = True


class CustomerCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    phone: str = Field(..., min_length=10, max_length=15)
    email: EmailStr
    license_number: str = Field(..., min_length=5, max_length=30)


class CustomerUpdate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    phone: str = Field(..., min_length=10, max_length=15)
    email: EmailStr
    license_number: str = Field(..., min_length=5, max_length=30)


class BookingCreate(BaseModel):
    customer_id: int = Field(..., gt=0)
    car_id: int = Field(..., gt=0)
    days: int = Field(..., gt=0, le=30)


class BookingUpdate(BaseModel):
    days: int = Field(..., gt=0, le=30)


# ═══════════════════════════════════════════════════════════════
# SAMPLE DATA
# ═══════════════════════════════════════════════════════════════

cars = [
    {
        "id": 1,
        "brand": "Hyundai",
        "model": "i20",
        "year": 2022,
        "rent_per_day": 1800,
        "fuel_type": "Petrol",
        "transmission": "Manual",
        "available": True
    },
    {
        "id": 2,
        "brand": "Maruti",
        "model": "Swift",
        "year": 2021,
        "rent_per_day": 1500,
        "fuel_type": "Petrol",
        "transmission": "Manual",
        "available": True
    },
    {
        "id": 3,
        "brand": "Honda",
        "model": "City",
        "year": 2023,
        "rent_per_day": 2500,
        "fuel_type": "Petrol",
        "transmission": "Automatic",
        "available": True
    },
    {
        "id": 4,
        "brand": "Tata",
        "model": "Nexon",
        "year": 2022,
        "rent_per_day": 2200,
        "fuel_type": "Diesel",
        "transmission": "Manual",
        "available": True
    },
    {
        "id": 5,
        "brand": "Kia",
        "model": "Seltos",
        "year": 2024,
        "rent_per_day": 3000,
        "fuel_type": "Diesel",
        "transmission": "Automatic",
        "available": True
    }
]

customers = [
    {
        "id": 1,
        "name": "Rahul Sharma",
        "phone": "9876543210",
        "email": "rahul@example.com",
        "license_number": "DL12345"
    },
    {
        "id": 2,
        "name": "Sneha Reddy",
        "phone": "9123456780",
        "email": "sneha@example.com",
        "license_number": "DL67890"
    }
]

bookings = []


# ═══════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════

def get_next_car_id():
    return len(cars) + 1


def get_next_customer_id():
    return len(customers) + 1


def get_next_booking_id():
    return len(bookings) + 1


def find_car(car_id: int):
    for car in cars:
        if car["id"] == car_id:
            return car
    return None


def find_customer(customer_id: int):
    for customer in customers:
        if customer["id"] == customer_id:
            return customer
    return None


def find_booking(booking_id: int):
    for booking in bookings:
        if booking["id"] == booking_id:
            return booking
    return None


def calculate_total_amount(rent_per_day: int, days: int):
    return rent_per_day * days


# ═══════════════════════════════════════════════════════════════
# ROOT
# ═══════════════════════════════════════════════════════════════

@app.get("/")
def home():
    return {"message": "Welcome to Car Rental Service API"}


# ═══════════════════════════════════════════════════════════════
#  GET /cars
# ═══════════════════════════════════════════════════════════════

@app.get("/cars")
def get_all_cars(
    brand: Optional[str] = None,
    fuel_type: Optional[str] = None,
    available: Optional[bool] = None,
    sort_by: Optional[str] = Query(None, pattern="^(rent_per_day|year)$"),
    order: Optional[str] = Query("asc", pattern="^(asc|desc)$"),
    page: int = Query(1, gt=0),
    limit: int = Query(5, gt=0)
):
    result = cars.copy()

    if brand:
        result = [car for car in result if car["brand"].lower() == brand.lower()]

    if fuel_type:
        result = [car for car in result if car["fuel_type"].lower() == fuel_type.lower()]

    if available is not None:
        result = [car for car in result if car["available"] == available]

    if sort_by:
        reverse_order = True if order == "desc" else False
        result = sorted(result, key=lambda x: x[sort_by], reverse=reverse_order)

    start = (page - 1) * limit
    end = start + limit
    paginated_result = result[start:end]

    return {
        "total_records": len(result),
        "page": page,
        "limit": limit,
        "cars": paginated_result
    }


#  GET /cars/{car_id}
@app.get("/cars/{car_id}")
def get_car_by_id(car_id: int):
    car = find_car(car_id)
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")
    return car


#  POST /cars
@app.post("/cars", status_code=status.HTTP_201_CREATED)
def add_car(car: CarCreate):
    new_car = {
        "id": get_next_car_id(),
        "brand": car.brand,
        "model": car.model,
        "year": car.year,
        "rent_per_day": car.rent_per_day,
        "fuel_type": car.fuel_type,
        "transmission": car.transmission,
        "available": car.available
    }
    cars.append(new_car)
    return {"message": "Car added successfully", "car": new_car}


#  PUT /cars/{car_id}
@app.put("/cars/{car_id}")
def update_car(car_id: int, updated_car: CarUpdate):
    car = find_car(car_id)
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")

    car["brand"] = updated_car.brand
    car["model"] = updated_car.model
    car["year"] = updated_car.year
    car["rent_per_day"] = updated_car.rent_per_day
    car["fuel_type"] = updated_car.fuel_type
    car["transmission"] = updated_car.transmission
    car["available"] = updated_car.available

    return {"message": "Car updated successfully", "car": car}


#  DELETE /cars/{car_id}
@app.delete("/cars/{car_id}")
def delete_car(car_id: int):
    car = find_car(car_id)
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")

    for booking in bookings:
        if booking["car_id"] == car_id and booking["status"] in ["pending", "confirmed", "picked_up"]:
            raise HTTPException(status_code=400, detail="Cannot delete car with active booking")

    cars.remove(car)
    return {"message": "Car deleted successfully"}


#  GET /cars/available/list
@app.get("/cars/available/list")
def get_available_cars():
    available_cars = [car for car in cars if car["available"]]
    return {
        "message": "Available cars fetched successfully",
        "available_cars": available_cars
    }


# ═══════════════════════════════════════════════════════════════
# CUSTOMERS
# ═══════════════════════════════════════════════════════════════

#  GET /customers
@app.get("/customers")
def get_all_customers():
    return {"customers": customers}


#  GET /customers/{customer_id}
@app.get("/customers/{customer_id}")
def get_customer_by_id(customer_id: int):
    customer = find_customer(customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


#  POST /customers
@app.post("/customers", status_code=status.HTTP_201_CREATED)
def add_customer(customer: CustomerCreate):
    new_customer = {
        "id": get_next_customer_id(),
        "name": customer.name,
        "phone": customer.phone,
        "email": customer.email,
        "license_number": customer.license_number
    }
    customers.append(new_customer)
    return {"message": "Customer added successfully", "customer": new_customer}


#  PUT /customers/{customer_id}
@app.put("/customers/{customer_id}")
def update_customer(customer_id: int, updated_customer: CustomerUpdate):
    customer = find_customer(customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    customer["name"] = updated_customer.name
    customer["phone"] = updated_customer.phone
    customer["email"] = updated_customer.email
    customer["license_number"] = updated_customer.license_number

    return {"message": "Customer updated successfully", "customer": customer}


#  DELETE /customers/{customer_id}
@app.delete("/customers/{customer_id}")
def delete_customer(customer_id: int):
    customer = find_customer(customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    for booking in bookings:
        if booking["customer_id"] == customer_id and booking["status"] in ["pending", "confirmed", "picked_up"]:
            raise HTTPException(status_code=400, detail="Cannot delete customer with active booking")

    customers.remove(customer)
    return {"message": "Customer deleted successfully"}


# ═══════════════════════════════════════════════════════════════
# BOOKINGS
# ═══════════════════════════════════════════════════════════════

#  GET /bookings
@app.get("/bookings")
def get_all_bookings():
    return {"bookings": bookings}


#  GET /bookings/{booking_id}
@app.get("/bookings/{booking_id}")
def get_booking_by_id(booking_id: int):
    booking = find_booking(booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking


#  POST /bookings
@app.post("/bookings", status_code=status.HTTP_201_CREATED)
def create_booking(booking: BookingCreate):
    customer = find_customer(booking.customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    car = find_car(booking.car_id)
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")

    if not car["available"]:
        raise HTTPException(status_code=400, detail="Car is not available for booking")

    total_amount = calculate_total_amount(car["rent_per_day"], booking.days)

    new_booking = {
        "id": get_next_booking_id(),
        "customer_id": booking.customer_id,
        "car_id": booking.car_id,
        "days": booking.days,
        "total_amount": total_amount,
        "status": "pending"
    }

    bookings.append(new_booking)
    return {"message": "Booking created successfully", "booking": new_booking}


#  PUT /bookings/{booking_id}
@app.put("/bookings/{booking_id}")
def update_booking(booking_id: int, updated_booking: BookingUpdate):
    booking = find_booking(booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    if booking["status"] not in ["pending", "confirmed"]:
        raise HTTPException(status_code=400, detail="Only pending or confirmed bookings can be updated")

    car = find_car(booking["car_id"])
    booking["days"] = updated_booking.days
    booking["total_amount"] = calculate_total_amount(car["rent_per_day"], updated_booking.days)

    return {"message": "Booking updated successfully", "booking": booking}


#  DELETE /bookings/{booking_id}
@app.delete("/bookings/{booking_id}")
def delete_booking(booking_id: int):
    booking = find_booking(booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    if booking["status"] == "picked_up":
        raise HTTPException(status_code=400, detail="Picked up booking cannot be deleted")

    if booking["status"] in ["pending", "confirmed"]:
        booking["status"] = "cancelled"
        return {"message": "Booking cancelled successfully", "booking": booking}

    bookings.remove(booking)
    return {"message": "Booking deleted successfully"}


#  PATCH /bookings/{booking_id}/confirm
@app.patch("/bookings/{booking_id}/confirm")
def confirm_booking(booking_id: int):
    booking = find_booking(booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    if booking["status"] != "pending":
        raise HTTPException(status_code=400, detail="Only pending bookings can be confirmed")

    booking["status"] = "confirmed"
    return {"message": "Booking confirmed successfully", "booking": booking}


#  PATCH /bookings/{booking_id}/pickup
@app.patch("/bookings/{booking_id}/pickup")
def pickup_car(booking_id: int):
    booking = find_booking(booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    if booking["status"] != "confirmed":
        raise HTTPException(status_code=400, detail="Only confirmed bookings can be picked up")

    car = find_car(booking["car_id"])
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")

    if not car["available"]:
        raise HTTPException(status_code=400, detail="Car is already not available")

    booking["status"] = "picked_up"
    car["available"] = False

    return {
        "message": "Car picked up successfully",
        "booking": booking,
        "car": car
    }


#  PATCH /bookings/{booking_id}/return-car
@app.patch("/bookings/{booking_id}/return-car")
def return_car(booking_id: int):
    booking = find_booking(booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    if booking["status"] != "picked_up":
        raise HTTPException(status_code=400, detail="Only picked up bookings can be returned")

    car = find_car(booking["car_id"])
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")

    booking["status"] = "returned"
    car["available"] = True

    return {
        "message": "Car returned successfully",
        "booking": booking,
        "car": car
    }


#  GET /bookings/search/filter
@app.get("/bookings/search/filter")
def search_filter_bookings(
    status_filter: Optional[str] = None,
    customer_id: Optional[int] = None,
    sort_by: Optional[str] = Query(None, pattern="^(total_amount|days)$"),
    order: Optional[str] = Query("asc", pattern="^(asc|desc)$"),
    page: int = Query(1, gt=0),
    limit: int = Query(5, gt=0)
):
    result = bookings.copy()

    if status_filter:
        result = [booking for booking in result if booking["status"].lower() == status_filter.lower()]

    if customer_id:
        result = [booking for booking in result if booking["customer_id"] == customer_id]

    if sort_by:
        reverse_order = True if order == "desc" else False
        result = sorted(result, key=lambda x: x[sort_by], reverse=reverse_order)

    start = (page - 1) * limit
    end = start + limit
    paginated_result = result[start:end]

    return {
        "total_records": len(result),
        "page": page,
        "limit": limit,
        "bookings": paginated_result
    }


    # ═══════════════════════════════════════════════════════════════
# 💰 DISCOUNT + COUPON FEATURES (BONUS)
# ═══════════════════════════════════════════════════════════════

# Coupon Database
coupons = {
    "CODE10": 10,
    "SAVE20": 20,
    "MEGA30": 30
}


# Helper for discount
def apply_discount(total_amount: int, discount_percent: int):
    discount_value = (total_amount * discount_percent) / 100
    final_amount = total_amount - discount_value
    return discount_value, final_amount


#  GET /bookings/{booking_id}/discount
@app.get("/bookings/{booking_id}/discount")
def get_discount(
    booking_id: int,
    discount_percent: int = Query(..., ge=0, le=50)
):
    booking = find_booking(booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    if booking["status"] not in ["confirmed", "picked_up", "returned"]:
        raise HTTPException(
            status_code=400,
            detail="Discount allowed only for confirmed or completed bookings"
        )

    discount_value, final_amount = apply_discount(
        booking["total_amount"],
        discount_percent
    )

    return {
        "message": "Discount applied successfully",
        "booking_id": booking_id,
        "original_amount": booking["total_amount"],
        "discount_percent": discount_percent,
        "discount_value": discount_value,
        "final_amount": final_amount
    }


#  GET /bookings/{booking_id}/apply-coupon
@app.get("/bookings/{booking_id}/apply-coupon")
def apply_coupon(
    booking_id: int,
    coupon_code: str
):
    booking = find_booking(booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    if booking["status"] not in ["confirmed", "picked_up", "returned"]:
        raise HTTPException(
            status_code=400,
            detail="Coupon can only be applied to confirmed or completed bookings"
        )

    coupon_code = coupon_code.upper()

    if coupon_code not in coupons:
        raise HTTPException(status_code=400, detail="Invalid coupon code")

    discount_percent = coupons[coupon_code]

    discount_value, final_amount = apply_discount(
        booking["total_amount"],
        discount_percent
    )

    return {
        "message": "Coupon applied successfully",
        "booking_id": booking_id,
        "coupon_code": coupon_code,
        "discount_percent": discount_percent,
        "discount_value": discount_value,
        "final_amount": final_amount
    }
