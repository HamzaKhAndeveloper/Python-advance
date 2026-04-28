from requests import request

response = request("POST","https://dummyjson.com/users/add",headers={'Content-Type': 'application/json'},json={"firstName":"ALi","lastName":"khan","age":23})
user =  response.json()

print(user)