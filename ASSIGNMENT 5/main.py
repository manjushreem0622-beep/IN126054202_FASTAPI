from fastapi import FastAPI, Query, Response, status
from pydantic import BaseModel, Field

app = FastAPI()

# ══ MODELS ════════════════════════════════════════════════════════

class OrderRequest(BaseModel):
    customer_name: str = Field(..., min_length=2, max_length=100)
    product_id: int = Field(..., gt=0)
    quantity: int = Field(..., gt=0, le=100)
    delivery_address: str = Field(..., min_length=10)

class NewProduct(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    price: int = Field(..., gt=0)
    category: str = Field(..., min_length=2)
    in_stock: bool = True

class CheckoutRequest(BaseModel):
    customer_name: str = Field(..., min_length=2)
    delivery_address: str = Field(..., min_length=10)

# ══ DATA ══════════════════════════════════════════════════════════

products = [
    {'id': 1, 'name': 'Wireless Mouse', 'price': 499, 'category': 'Electronics', 'in_stock': True},
    {'id': 2, 'name': 'Notebook', 'price': 99, 'category': 'Stationery', 'in_stock': True},
    {'id': 3, 'name': 'USB Hub', 'price': 799, 'category': 'Electronics', 'in_stock': False},
    {'id': 4, 'name': 'Pen Set', 'price': 49, 'category': 'Stationery', 'in_stock': True},
]

orders = []
order_counter = 1
cart = []

# ══ HELPERS ═══════════════════════════════════════════════════════

def find_product(product_id: int):
    for p in products:
        if p['id'] == product_id:
            return p
    return None

def calculate_total(product: dict, quantity: int) -> int:
    return product['price'] * quantity

def filter_products_logic(category=None, min_price=None, max_price=None, in_stock=None):
    result = products
    if category is not None:
        result = [p for p in result if p['category'] == category]
    if min_price is not None:
        result = [p for p in result if p['price'] >= min_price]
    if max_price is not None:
        result = [p for p in result if p['price'] <= max_price]
    if in_stock is not None:
        result = [p for p in result if p['in_stock'] == in_stock]
    return result

# ══ ENDPOINTS ═════════════════════════════════════════════════════

@app.get('/')
def home():
    return {'message': 'Welcome to our E-commerce API'}

@app.get('/products')
def get_all_products():
    return {'products': products, 'total': len(products)}

# ── FILTER ───────────────────────────────────────────────────────

@app.get('/products/filter')
def filter_products(
    category: str = Query(None),
    min_price: int = Query(None),
    max_price: int = Query(None),
    in_stock: bool = Query(None),
):
    result = filter_products_logic(category, min_price, max_price, in_stock)
    return {'filtered_products': result, 'count': len(result)}

# ── COMPARE ──────────────────────────────────────────────────────

@app.get('/products/compare')
def compare_products(product_id_1: int = Query(...), product_id_2: int = Query(...)):
    p1 = find_product(product_id_1)
    p2 = find_product(product_id_2)

    if not p1:
        return {'error': f'Product {product_id_1} not found'}
    if not p2:
        return {'error': f'Product {product_id_2} not found'}

    cheaper = p1 if p1['price'] < p2['price'] else p2

    return {
        'product_1': p1,
        'product_2': p2,
        'better_value': cheaper['name'],
        'price_diff': abs(p1['price'] - p2['price']),
    }

# ── SEARCH PRODUCTS ──────────────────────────────────────────────

@app.get('/products/search')
def search_products(keyword: str = Query(...)):
    results = [p for p in products if keyword.lower() in p['name'].lower()]

    if not results:
        return {'message': f'No products found for: {keyword}', 'results': []}

    return {'keyword': keyword, 'total_found': len(results), 'results': results}

# ── SORT ─────────────────────────────────────────────────────────

@app.get('/products/sort')
def sort_products(sort_by: str = Query('price'), order: str = Query('asc')):
    if sort_by not in ['price', 'name']:
        return {'error': "sort_by must be 'price' or 'name'"}
    if order not in ['asc', 'desc']:
        return {'error': "order must be 'asc' or 'desc'"}

    sorted_products = sorted(products, key=lambda p: p[sort_by], reverse=(order == 'desc'))

    return {'sort_by': sort_by, 'order': order, 'products': sorted_products}

# ── PAGINATION ───────────────────────────────────────────────────

@app.get('/products/page')
def get_products_paged(page: int = Query(1, ge=1), limit: int = Query(2, ge=1, le=20)):
    start = (page - 1) * limit
    paged = products[start:start + limit]

    return {
        'page': page,
        'limit': limit,
        'total': len(products),
        'total_pages': -(-len(products) // limit),
        'products': paged,
    }

# ══════════════════════════════════════════════════════════════════
# 🔵 NEW QUESTIONS (Q4, Q5, Q6, BONUS)
# ══════════════════════════════════════════════════════════════════

# Q4
@app.get('/orders/search')
def search_orders(customer_name: str = Query(...)):
    results = [o for o in orders if customer_name.lower() in o['customer_name'].lower()]

    if not results:
        return {'message': f'No orders found for: {customer_name}'}

    return {'customer_name': customer_name, 'total_found': len(results), 'orders': results}

# Q5
@app.get('/products/sort-by-category')
def sort_by_category():
    sorted_products = sorted(products, key=lambda p: (p['category'], p['price']))
    return {'products': sorted_products, 'total': len(sorted_products)}

# Q6
@app.get('/products/browse')
def browse_products(
    keyword: str = Query(None),
    sort_by: str = Query('price'),
    order: str = Query('asc'),
    page: int = Query(1, ge=1),
    limit: int = Query(4, ge=1, le=20)
):
    result = products

    if keyword:
        result = [p for p in result if keyword.lower() in p['name'].lower()]

    if sort_by not in ['price', 'name']:
        return {'error': "sort_by must be 'price' or 'name'"}

    if order not in ['asc', 'desc']:
        return {'error': "order must be 'asc' or 'desc'"}

    result = sorted(result, key=lambda p: p[sort_by], reverse=(order == 'desc'))

    total = len(result)
    start = (page - 1) * limit
    paged = result[start:start + limit]

    return {
        'keyword': keyword,
        'sort_by': sort_by,
        'order': order,
        'page': page,
        'limit': limit,
        'total_found': total,
        'total_pages': -(-total // limit) if total > 0 else 0,
        'products': paged
    }

# BONUS
@app.get('/orders/page')
def get_orders_paged(page: int = Query(1, ge=1), limit: int = Query(3, ge=1, le=20)):
    total = len(orders)
    start = (page - 1) * limit
    paged = orders[start:start + limit]

    return {
        'page': page,
        'limit': limit,
        'total_orders': total,
        'total_pages': -(-total // limit) if total > 0 else 0,
        'orders': paged
    }

# ── PRODUCT CRUD ─────────────────────────────────────────────────

@app.post('/products')
def add_product(new_product: NewProduct, response: Response):
    existing_names = [p['name'].lower() for p in products]
    if new_product.name.lower() in existing_names:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'error': 'Product already exists'}

    new_id = max(p['id'] for p in products) + 1
    product = {**new_product.dict(), 'id': new_id}
    products.append(product)

    response.status_code = status.HTTP_201_CREATED
    return {'product': product}

@app.get('/products/{product_id}')
def get_product(product_id: int):
    product = find_product(product_id)
    if not product:
        return {'error': 'Product not found'}
    return {'product': product}


# ── ORDERS ───────────────────────────────────────────────────────

@app.post('/orders')
def place_order(order_data: OrderRequest):
    global order_counter

    product = find_product(order_data.product_id)
    if not product:
        return {'error': 'Product not found'}

    total = calculate_total(product, order_data.quantity)

    order = {
        'order_id': order_counter,
        'customer_name': order_data.customer_name,
        'product': product['name'],
        'quantity': order_data.quantity,
        'delivery_address': order_data.delivery_address,
        'total_price': total,
        'status': 'confirmed',
    }

    orders.append(order)
    order_counter += 1

    return {'order': order}
