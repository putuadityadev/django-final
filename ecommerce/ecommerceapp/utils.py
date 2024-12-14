import midtransclient

def generate_midtrans_token(order):
    snap = midtransclient.Snap(
        is_production=False,
        server_key='Mid-server-4OJ9LSusdcjjMvOI7kl4u2P0'
    )

    param = {
        "transaction_details": {
            "order_id": str(order.order_id),
            "gross_amount": order.amount
        },
        "customer_details": {
            "first_name": order.name,
            "email": order.email,
            "phone": order.phone
        }
    }

    transaction = snap.create_transaction(param)
    return transaction['token']