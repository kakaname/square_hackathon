from square.http.auth.o_auth_2 import BearerAuthCredentials
from square.client import Client
import os
import json
import sys, uuid
from include.database import record_data

demo_location = ""

def kill_all():
  kill_all_cards()
  kill_all_users()

def kill_all_cards():
  client = get_client()

  # get all existing customers
  customer_list = []
  result = client.customers.list_customers()
  if result.is_success():
    if result.body != {}:
      for customer in result.body["customers"]:
        customer_list.append(customer["id"])
  elif result.is_error():
    print("ERROR: Listing Customers")
    for error in result.errors:
      print(error['category'])
      print(error['code'])
      print(error['detail']) 

  # list all cards
  
  card_id_list = []
  result = client.cards.list_cards()
  if result.is_success():
    if result.body != {}:
      for card in result.body["cards"]:
        card_id_list.append(card["id"])

  elif result.is_error():
    print("ERROR: listing cards")
    for error in result.errors:
      print(error['category'])
      print(error['code'])
      print(error['detail']) 

  for card_id in card_id_list:
    result = client.cards.disable_card(card_id)
    if result.is_error():
      print("ERROR: disabling cards")
      for error in result.errors:
        print(error['category'])
        print(error['code'])
        print(error['detail']) 

  print("killed all cards")
    

def kill_all_users():
  client = get_client()

  # get all existing customers
  customer_list = []
  result = client.customers.list_customers()
  if result.is_success():
    if result.body != {}:
      for customer in result.body["customers"]:
        customer_list.append(customer["id"])

  elif result.is_error():
    print("ERROR: Listing Customers")
    for error in result.errors:
      print(error['category'])
      print(error['code'])
      print(error['detail']) 

  # delete said customers
  if len(customer_list) > 0:
    body = '{ "customer_ids": ['
    for customer_id in customer_list:
      body = body + '"' + customer_id + '",'
    body = body[:-1] # remove trailing ,
    body = body + ']}'
    checkJSON(body)

    result = client.customers.bulk_delete_customers(body)
    if result.is_error():
      print("ERROR: Deleting customers")
      for error in result.errors:
        print(error['category'])
        print(error['code'])
        print(error['detail']) 
  
  print("killed all users")

def get_client():
  client = Client(
    bearer_auth_credentials=BearerAuthCredentials(
        access_token=os.environ['SQUARE_ACCESS_TOKEN']
    ),
    environment='sandbox')
  return client


def get_idem_key():
  return str(uuid.uuid1())

def get_loc_id():
  global demo_location
  set_demo_loc()
  return demo_location

def set_demo_loc():
  global demo_location
  if demo_location == "":
    client = Client(
    bearer_auth_credentials=BearerAuthCredentials(
        access_token=os.environ['SQUARE_ACCESS_TOKEN']
    ),
    environment='sandbox')

    result = client.locations.list_locations()
    if result.is_success():
      for location in result.body['locations']:
        demo_location = location['id']

    elif result.is_error():
      for error in result.errors:
        print(error['category'])
        print(error['code'])
        print(error['detail']) 

def checkJSON(string_lit):
  try :
    json.loads(string_lit)
  except :
    print("ERROR: JSON format error")
    print("JSON: ", string_lit)
    sys.exit()

def create_demo_customer():
  client = get_client()
  body = '{ \
    "given_name": "Amelia", \
    "family_name": "Earhart", \
    "email_address": "Amelia.Earhart@example.com", \
    "address": { \
      "address_line_1": "500 Electric Ave", \
      "address_line_2": "Suite 600", \
      "locality": "New York", \
      "administrative_district_level_1": "NY", \
      "postal_code": "10003", \
      "country": "CA" }, \
    "phone_number": "+1-212-555-4240", \
    "reference_id": "YOUR_REFERENCE_ID", \
    "note": "a customer" }' 
    
  checkJSON(body)
  result = client.customers.create_customer(body)
  if result.is_success():
    return result.body["customer"]
  elif result.is_error():
    print("ERROR: Creating customers")
    for error in result.errors:
      print(error['category'])
      print(error['code'])
      print(error['detail']) 


def get_demo_customer():
  client = get_client()
  result = client.customers.list_customers()
  if result.is_success():
    if result.body == {}:
      return create_demo_customer()
    else:
      return result.body["customers"][0]
  elif result.is_error():
    print("ERROR: Listing customers")
    for error in result.errors:
      print(error['category'])
      print(error['code'])
      print(error['detail']) 
  


def create_demo_card():
  client = get_client()
  customer = get_demo_customer()
  body = '{"idempotency_key": "' + get_idem_key() + '", \
    "source_id": "cnon:card-nonce-ok", \
    "card": { \
      "billing_address": { \
        "address_line_1": "500 Electric Ave", \
        "address_line_2": "Suite 600", \
        "locality": "New York", \
        "administrative_district_level_1": "NY", \
        "postal_code": "94103", \
        "country": "CA" \
      }, \
      "cardholder_name": "Amelia Earhart", \
      "customer_id": "' + customer["id"] + '", \
      "reference_id": "alternate-id-1" \
    } \
  }'

  result = client.cards.create_card(body)
  if result.is_success():
    return result.body
  elif result.is_error():
    print("error creating demo card")
    for error in result.errors:
      print(error['category'])
      print(error['code'])
      print(error['detail']) 



def get_demo_credit_card():
  client = get_client()
  result = client.cards.list_cards()
  if result.is_success():
    if result.body == {}:
      return create_demo_card()["card"]
    else:
      return result.body["cards"][0]
  elif result.is_error():
    for error in result.errors:
      print(error['category'])
      print(error['code'])
      print(error['detail']) 

def activate_gift_card(gift_card_id, idem_key, loc_id, client, value):
  activity_string = '{"idempotency_key":"' + idem_key + '", "gift_card_activity": {"gift_card_id": "' + gift_card_id + '", ' + \
  '"type": "ACTIVATE", "location_id": "' + loc_id + '", "activate_activity_details": {"order_id" : "123", "amount_money": {' + \
  '"amount" :' + value + ', "currency" : "CAD"} } } }'

  print("act string", activity_string)
  result = client.gift_card_activities.create_gift_card_activity(activity_string)

  if result.is_success():
    print("result : ", result.body)
  elif result.is_error():
    print("ERROR: when creating giftcard activity to API")
    for error in result.errors:
        print(error['category'])
        print(error['code'])
        print(error['detail']) 

# stub for now
def make_order_string():
  idem_key = get_idem_key()
  location = get_loc_id()
  customer = get_demo_customer()
  ret_string = '{ "idempotency_key": "' + idem_key + '", \
    "order": { \
      "reference_id": "my-order-001", \
      "location_id": "' + location + '", \
      "customer_id": "' + customer["id"] +'", \
      "line_items": [ \
        { \
          "name": "Ribeye Steak", \
          "quantity": "1", \
          "base_price_money": { \
            "amount": 6000, \
            "currency": "CAD" \
          } \
        }, \
        { \
          "name": "Mashed Potatoes", \
          "quantity" : "1", \
          "base_price_money" : { \
            "amount" : 2000, \
            "currency" : "CAD" \
          } \
        } \
      ] \
    } }'
  checkJSON(ret_string)
  return ret_string


def create_order():
  client = get_client()
  body = make_order_string()  
  result = client.orders.create_order(body)

  if result.is_success():
    return result.body["order"]
  elif result.is_error():
    print("ERROR: when creating order")
    for error in result.errors:
        print(error['category'])
        print(error['code'])
        print(error['detail']) 

def tester(value, service):
  order = create_order()
  if service - value > 0:
    gift_card_payment = pay_with_gift_card(value, order["id"], True)["payment"]["id"]
    card_payment = pay_with_card(service - value, order["id"], True)["payment"]["id"]
    pay_for_order(order["id"], gift_card_payment, card_payment)
  else:
    pay_with_gift_card(service, order["id"], False)


  record_data(value, service)

def pay_for_order(order_id, gift_card_payment, card_payment):
  client = get_client()
  idem_key = get_idem_key()

  body = '{ "idempotency_key" : "' + idem_key + '", "payment_ids" : ['
  body = body + '"' + gift_card_payment + '",'
  body = body + '"' + card_payment + '"]}'
  result = client.orders.pay_order(order_id, body)

  if result.is_error():
    print("ERROR: when paying order")
    for error in result.errors:
        print(error['category'])
        print(error['code'])
        print(error['detail']) 


def pay_with_gift_card(value, order_id, partial):
  client = get_client()
  demo_loc = get_loc_id()
  demo_customer = get_demo_customer()
  idem_key = get_idem_key()

  body = '{ \
    "source_id": "cnon:gift-card-nonce-ok", \
    "amount_money": { \
      "amount": ' + str(value) + ', \
      "currency": "CAD" \
    }, \
    "location_id": "' + demo_loc + '", \
    "customer_id": "' + demo_customer["id"] + '", \
    "idempotency_key": "' + idem_key+ '", \
    "order_id" : "' + order_id + '"'
  if partial:
    body = body + ", autocomplete : false}"  
  else:
    body = body + "}"

  result = client.payments.create_payment(body)
  if result.is_success():
    return result.body
  elif result.is_error():
    print("ERROR: when creating giftcard payment connecting to API")
    for error in result.errors:
        print(error['category'])
        print(error['code'])
        print(error['detail']) 

def pay_with_card(service, order_id, partial):
  client = get_client()
  demo_loc = get_loc_id()
  demo_customer = get_demo_customer()
  idem_key = get_idem_key()

  body = '{ \
    "source_id": "cnon:card-nonce-ok", \
    "amount_money": { \
      "amount": ' + str(service) + ', \
      "currency": "CAD" \
    }, \
    "location_id": "' + demo_loc + '", \
    "customer_id": "' + demo_customer["id"] + '", \
    "idempotency_key": "' + idem_key+ '", \
    "order_id" : "' + order_id + '"'
  if partial:
    body = body + ", autocomplete : false}"  
  else:
    body = body + "}"

  result = client.payments.create_payment(body)
  if result.is_success():
    return result.body
  elif result.is_error():
    print("ERROR: when creating card pyament connecting to API")
    for error in result.errors:
        print(error['category'])
        print(error['code'])
        print(error['detail']) 