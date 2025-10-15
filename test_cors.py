import requests

def test_cors():
    url = 'http://127.0.0.1:5000/api/auth/login'
    headers = {
        'Origin': 'http://127.0.0.1:5500',
        'Content-Type': 'application/json'
    }
    
    # Test OPTIONS request (preflight)
    print("Testing OPTIONS request (preflight)...")
    options_response = requests.options(url, headers=headers)
    print(f"Status Code: {options_response.status_code}")
    print(f"Headers: {dict(options_response.headers)}")
    
    # Look for specific CORS headers
    cors_headers = {k: v for k, v in options_response.headers.items() if 'access-control' in k.lower()}
    print(f"CORS Headers: {cors_headers}")
    
    # Test POST request
    print("\nTesting POST request...")
    data = {
        'email': 'jadmin@gmail.com',
        'password': 'secret123'
    }
    
    post_response = requests.post(url, json=data, headers=headers)
    print(f"Status Code: {post_response.status_code}")
    
    # Look for CORS headers in POST response
    cors_headers_post = {k: v for k, v in post_response.headers.items() if 'access-control' in k.lower()}
    print(f"CORS Headers in POST: {cors_headers_post}")
    
    print(f"Response: {post_response.text[:200]}...")

if __name__ == "__main__":
    test_cors()