import urllib.request
import urllib.parse
import json
import http.cookiejar
import sys

# Set up cookie jar to handle PHP sessions automatically
cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
urllib.request.install_opener(opener)

BASE_URL = "http://localhost/op/api/"

def request(endpoint, method="GET", data=None):
    url = BASE_URL + endpoint
    req_data = None
    headers = {}
    
    if data is not None:
        req_data = json.dumps(data).encode('utf-8')
        headers = {'Content-Type': 'application/json'}
        
    req = urllib.request.Request(url, data=req_data, headers=headers, method=method)
    
    try:
        with urllib.request.urlopen(req) as response:
            res_body = response.read().decode('utf-8')
            return response.status, json.loads(res_body)
    except urllib.error.HTTPError as e:
        try:
            err_body = e.read().decode('utf-8')
            return e.code, json.loads(err_body)
        except Exception:
            return e.code, {"error": str(e)}
    except Exception as e:
        return 0, {"error": str(e)}

def run_tests():
    print("=== STARTING LARAGON PHP MYSQL API VERIFICATION ===")
    
    # 1. Fetch all products
    print("\n1. Fetching all products...")
    status, res = request("products.php?action=all")
    print(f"Status: {status}")
    if status == 200 and isinstance(res, list):
        print(f"Success! Found {len(res)} products.")
        if len(res) > 0:
            p = res[0]
            print(f"Sample product: ID={p['id']}, Name='{p['name']}', Price={p['price']}")
            prod_id = p['id']
            prod_price = p['price']
            prod_name = p['name']
        else:
            print("Error: Product list is empty.")
            sys.exit(1)
    else:
        print(f"Failed to fetch products: {res}")
        sys.exit(1)
        
    # Generate unique email for registration to avoid conflicts
    import random
    test_email = f"testuser_{random.randint(1000, 9999)}@example.com"
    test_password = "Password123!"
    test_name = "Test User Laragon"
    
    # 2. Register new user
    print(f"\n2. Registering new user: {test_email}...")
    status, res = request("auth.php?action=register", method="POST", data={
        "email": test_email,
        "password": test_password,
        "name": test_name,
        "phone": "08123456789"
    })
    print(f"Status: {status}")
    if status == 200 and res.get('success'):
        print(f"Success! Registered: {res['user']}")
    else:
        print(f"Failed registration: {res}")
        sys.exit(1)
        
    # 3. Get profile
    print("\n3. Retrieving profile info...")
    status, res = request("auth.php?action=get_profile")
    print(f"Status: {status}")
    if status == 200 and res.get('success'):
        print(f"Success! Profile: {res['data']}")
    else:
        print(f"Failed to get profile: {res}")
        sys.exit(1)
        
    # 4. Add product to cart
    print(f"\n4. Adding product '{prod_id}' to cart...")
    status, res = request("cart.php?action=add", method="POST", data={
        "productId": prod_id,
        "quantity": 2,
        "variant": "100gr"
    })
    print(f"Status: {status}")
    if status == 200 and res.get('success'):
        print(f"Success! Cart item count: {res['itemCount']}")
    else:
        print(f"Failed to add to cart: {res}")
        sys.exit(1)
        
    # 5. Get cart content
    print("\n5. Fetching current cart...")
    status, res = request("cart.php?action=get")
    print(f"Status: {status}")
    if status == 200 and 'items' in res:
        print(f"Success! Cart items: {res['items']}")
        print(f"Cart total: {res['total']}")
        cart_items = res['items']
        cart_total = res['total']
    else:
        print(f"Failed to get cart: {res}")
        sys.exit(1)
        
    # 6. Create checkout order
    print("\n6. Placing order...")
    order_payload = {
        "items": cart_items,
        "subtotal": cart_total,
        "shipping": 0.0,
        "total": cart_total,
        "shippingAddress": "Jl. Mawar No. 12, Jakarta",
        "paymentMethod": "COD",
        "notes": "Testing local checkout flow"
    }
    status, res = request("orders.php?action=create", method="POST", data=order_payload)
    print(f"Status: {status}")
    if status == 200 and res.get('success'):
        print(f"Success! Order created with ID: {res['orderId']}")
        order_id = res['orderId']
    else:
        print(f"Failed to place order: {res}")
        sys.exit(1)
        
    # 7. Get order history
    print("\n7. Retrieving order history...")
    status, res = request("orders.php?action=user_orders")
    print(f"Status: {status}")
    if status == 200 and isinstance(res, list):
        print(f"Success! Found {len(res)} orders in history.")
        found = False
        for o in res:
            if o['id'] == order_id:
                print(f"Verified order {order_id} exists in history! Total={o['total']}, Status={o['status']}")
                found = True
                break
        if not found:
            print("Error: Created order not found in history.")
            sys.exit(1)
    else:
        print(f"Failed to fetch user orders: {res}")
        sys.exit(1)
        
    # 8. Verify cart is cleared after checkout
    print("\n8. Verifying cart is cleared...")
    status, res = request("cart.php?action=get")
    print(f"Status: {status}")
    if status == 200 and len(res.get('items', [])) == 0:
        print("Success! Cart is empty as expected.")
    else:
        print(f"Error: Cart is not empty: {res}")
        sys.exit(1)
        
    # 9. Logout
    print("\n9. Logging out...")
    status, res = request("auth.php?action=logout", method="POST")
    print(f"Status: {status}")
    if status == 200 and res.get('success'):
        print("Success! Logged out.")
    else:
        print(f"Failed to logout: {res}")
        sys.exit(1)
        
    print("\n=== ALL LARAGON PHP MYSQL API TESTS PASSED SUCCESSFULLY! ===")

if __name__ == "__main__":
    run_tests()
