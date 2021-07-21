from django.shortcuts import render
import tinvest as ti

 
TOKEN = 't.Cz0mvF5Z-uPelMSg5eTTHTSe06y2E227cjLXqp09J4ZzjdFrsw7Mk1VG6fgiuE_iJWcPzYbNjpvB5LZUkIV92Q'
 
# регистрируем аккаунт
client = ti.SyncClient(TOKEN, use_sandbox=True)
body = ti.SandboxRegisterRequest.tinkoff()
response = client.register_sandbox_account(body)
broker_account_id = response.payload.broker_account_id
# print(response.payload)
 
# получение списка акций
response = client.get_market_stocks()
print(response.payload)