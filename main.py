import json
import re

# --- Simulated Tools ---
def get_order_details(order_id: str) -> dict:
    """Simulates fetching order details from a database."""
    print(f"\nTOOL CALL: get_order_details('{order_id}') - SUCCESS")
    if order_id == "ORD123":
        return {
            "order_id": "ORD123",
            "status": "Shipped",
            "items": ["Laptop", "Mouse"],
            "customer_name": "Alice Smith",
            "shipping_address": "123 Main St, Anytown, USA 12345", # Personally Identifiable Information (PII)
            "customer_email": "alice.smith@example.com"
        }
    return {"error": "Order not found"}

def send_message(recipient: str, message_body: str) -> bool:
    """Simulates sending a message (e.g., email, chat) to a customer."""
    # In a real scenario, this would interact with an external messaging service.
    # For this demo, we just print and return True, simulating a successful tool call.
    print(f"TOOL CALL: send_message('{recipient}', '{message_body[:70]}...') - SUCCESS")
    return True

# --- Simulated Company Policies ---
def check_pii_policy(message_content: str, channel_type: str) -> bool:
    """
    Policy: PII should not be sent via unencrypted channels (like standard email/chat)
    unless explicitly requested and verified. This function checks for common PII patterns.
    """
    pii_patterns = [
        r"\d{3}[-.\s]?\d{3}[-.\s]?\d{4}", # Phone number
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", # Email address
        r"\d{1,5}\s\w.\s(\b\w*\b\s){1,2}\w*\s\w{2}\s\d{5}(-\d{4})?", # Street address (simplified)
        r"SSN|Social Security Number", # Keywords
        r"\b\d{5}\b", # Zip code
    ]
    is_pii_present = False
    for pattern in pii_patterns:
        if re.search(pattern, message_content, re.IGNORECASE):
            is_pii_present = True
            break

    # Assume 'email' or 'chat' are unencrypted for this demo's policy context
    if is_pii_present and channel_type in ["email", "chat"]:
        print(f"  POLICY CHECK: PII found in message for unencrypted channel ({channel_type}).")
        return False # Policy violated
    print(f"  POLICY CHECK: No PII violation detected for channel ({channel_type}).")
    return True # Policy compliant

# --- Simulated AI Agent ---
class AIAgent:
    def __init__(self, name: str):
        self.name = name

    def handle_customer_query(self, customer_id: str, query: str):
        print(f"AGENT '{self.name}' handling query for customer {customer_id}: '{query}'")

        if "order status" in query.lower():
            # Agent's decision: Use get_order_details tool to retrieve information
            order_details = get_order_details("ORD123") # Assuming agent extracts order_id from query

            if order_details and "error" not in order_details:
                status = order_details.get("status", "unknown")
                shipping_address = order_details.get("shipping_address", "N/A")
                customer_email = order_details.get("customer_email", "N/A")

                # AGENT'S DECISION POINT LEADING TO VIOLATION:
                # The agent decides to construct a message that includes the full shipping address (PII).
                # This decision, while seemingly helpful, violates a policy for unencrypted channels.
                response_message = (
                    f"Your order (ID: {order_details['order_id']}) is currently '{status}'. "
                    f"It was shipped to: {shipping_address}. " # Agent includes PII here
                    f"You should receive it soon."
                )

                # Agent's decision: Use send_message tool to deliver the response.
                # This tool call will be technically successful.
                message_sent_successfully = send_message(customer_email, response_message)

                # --- Post-action Policy Check ---
                # Even though the `send_message` tool call was successful, the *content*
                # of the message, as composed by the agent, might violate company policy.
                if not check_pii_policy(response_message, "email"):
                    print(f"  AGENT '{self.name}' ACTION RESULT: POLICY VIOLATION DETECTED after successful tool calls.")
                    print("    Reason: Agent sent PII (shipping address) via an unencrypted email channel.")
                elif message_sent_successfully:
                    print(f"  AGENT '{self.name}' ACTION RESULT: Successfully responded to query (policy compliant).")
                else:
                    print(f"  AGENT '{self.name}' ACTION RESULT: Failed to send message.")
            else:
                print(f"  AGENT '{self.name}' ACTION RESULT: Could not retrieve order details.")
        else:
            print(f"  AGENT '{self.name}' ACTION RESULT: Cannot handle this query type.")

# --- Main execution ---
if __name__ == "__main__":
    print("--- Scenario 1: Agent violates policy despite successful tool calls ---")
    customer_service_agent = AIAgent("OrderBot")
    customer_service_agent.handle_customer_query(
        "CUST001", "What is the status of my order ORD123?"
    )

    print("\n--- Scenario 2: Agent avoids PII violation by being policy-aware ---")
    class SecureAIAgent(AIAgent):
        def handle_customer_query(self, customer_id: str, query: str):
            print(f"AGENT '{self.name}' handling query for customer {customer_id}: '{query}'")

            if "order status" in query.lower():
                order_details = get_order_details("ORD123")
                if order_details and "error" not in order_details:
                    status = order_details.get("status", "unknown")
                    customer_email = order_details.get("customer_email", "N/A")

                    # AGENT'S POLICY-COMPLIANT DECISION POINT:
                    # This agent constructs the message *without* including the full shipping address,
                    # adhering to the PII policy for unencrypted channels.
                    response_message = (
                        f"Your order (ID: {order_details['order_id']}) is currently '{status}'. "
                        f"For detailed shipping information, please check your account portal or reply for secure verification."
                    )

                    message_sent_successfully = send_message(customer_email, response_message)

                    if not check_pii_policy(response_message, "email"):
                        print(f"  AGENT '{self.name}' ACTION RESULT: POLICY VIOLATION DETECTED after successful tool calls.")
                        print("    Reason: Agent sent PII via unencrypted email.")
                    elif message_sent_successfully:
                        print(f"  AGENT '{self.name}' ACTION RESULT: Successfully responded to query (policy compliant).")
                    else:
                        print(f"  AGENT '{self.name}' ACTION RESULT: Failed to send message.")
                else:
                    print(f"  AGENT '{self.name}' ACTION RESULT: Could not retrieve order details.")
            else:
                print(f"  AGENT '{self.name}' ACTION RESULT: Cannot handle this query type.")

    secure_agent = SecureAIAgent("SecureOrderBot")
    secure_agent.handle_customer_query(
        "CUST002", "Can you tell me my order status for ORD123?"
    )
