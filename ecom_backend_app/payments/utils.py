import base64
import hashlib
import hmac
import json


def generate_esewa_signature(secret_key: str, total_amount: str, transaction_uuid: str, product_code: str) -> str:
    message = f"total_amount={total_amount},transaction_uuid={transaction_uuid},product_code={product_code}"
    digest = hmac.new(
        secret_key.encode("utf-8"),
        message.encode("utf-8"),
        hashlib.sha256
    ).digest()
    return base64.b64encode(digest).decode("utf-8")


def verify_esewa_response_signature(secret_key: str, response_data: dict) -> bool:
    signed_field_names = response_data.get("signed_field_names", "")
    signature = response_data.get("signature", "")

    if not signed_field_names or not signature:
        return False

    fields = [field.strip() for field in signed_field_names.split(",") if field.strip()]
    message_parts = []

    for field in fields:
        value = response_data.get(field, "")
        message_parts.append(f"{field}={value}")

    message = ",".join(message_parts)

    digest = hmac.new(
        secret_key.encode("utf-8"),
        message.encode("utf-8"),
        hashlib.sha256
    ).digest()
    expected_signature = base64.b64encode(digest).decode("utf-8")

    return hmac.compare_digest(signature, expected_signature)


def decode_base64_response(data_string: str) -> dict:
    decoded = base64.b64decode(data_string).decode("utf-8")
    return json.loads(decoded)