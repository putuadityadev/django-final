# utils.py di app yang sesuai
import midtransclient

def generate_midtrans_token(order):
    # Konfigurasi Midtrans
    snap = midtransclient.Snap(
        is_production=False,
        server_key='Mid-server-4OJ9LSusdcjjMvOI7kl4u2P0'
    )

    # Persiapkan parameter transaksi
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

    # Dapatkan token
    transaction = snap.create_transaction(param)
    return transaction['token']