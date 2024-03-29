import json
import boto3
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('CustomerDetails')  # Replace 'CustomerDetails' with your DynamoDB table name
ses_client = boto3.client('ses')

def lambda_handler(event, context):
    customer_id = event['customerId']
    response = table.get_item(Key={'customerId': customer_id})
    
    items = response.get('Item', {}).get('items', [])
    total_price = calculate_total_price(items)
    
    # Generate bill content
    bill_content = generate_bill_content(items, total_price)
    
    # Send email with HTML content
    send_email(customer_id, bill_content)
    
    return "Email sent successfully."

def calculate_total_price(items):
    total = Decimal('0')
    for item in items:
        quantity = Decimal(item.get('quantity', 0))  # Use get method to handle missing 'quantity' attribute
        price = Decimal(item.get('price', 0))  # Use get method to handle missing 'price' attribute
        total += quantity * price
    return total

def generate_bill_content(items, total_price):
    # Generate HTML content for the bill
    bill_html = "<h2>Your Bill</h2>"
    bill_html += "<table border='1'><tr><th>Quantity</th><th>Item</th><th>Price</th></tr>"
    
    for item in items:
        itemName = item.get('itemName', 'Unknown')
        quantity = item.get('quantity', 'Unknown')
        price = item.get('price', 'Unknown')
        bill_html += f"<tr><td>{quantity}</td><td>{itemName}</td><td>${price}</td></tr>"
    
    # Add total price row
    bill_html += f"<tr><td colspan='2'><b>Total Price:</b></td><td>${total_price}</td></tr>"
    
    bill_html += "</table>"
    
    return bill_html

def send_email(customer_id, bill_content):
    customer_email = f"{customer_id}cseh@gmail.com"  # Assuming customer ID is their email prefix
    subject = "Your Bill"
    
    # Send email using SES with HTML content
    response = ses_client.send_email(
        Source="bhanupodagatlapalli@gmail.com",
        Destination={'ToAddresses': [customer_email]},
        Message={
            'Subject': {'Data': subject},
            'Body': {'Html': {'Data': bill_content}}
        }
    )

    print(response)  # Optional: Print SES response for logging or debugging purposes
