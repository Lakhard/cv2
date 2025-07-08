import json
import uuid
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse

AVAILABLE_ITEMS = {
    'espresso', 'latte', 'cappuccino', 'americano',
    'macchiato', 'flat_white', 'glace'
}


class RequestHandler(BaseHTTPRequestHandler):

    def _send_response(self, status_code, message, status_type, order_id=None):
        response = {
            'status': status_type,
            'message': message
        }
        if order_id:
            response['order_id'] = str(order_id)

        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode('utf-8'))

    def _validate_order(self, order_data):

        required_fields = {'item', 'quantity', 'price', 'extras'}
        if not all(field in order_data for field in required_fields):
            return False, "Missing required fields"

        if not all(key in order_data['extras'] for key in ['milk', 'sugar']):
            return False, "Missing required fields in extras"

        if order_data['item'].lower() not in AVAILABLE_ITEMS:
            return False, f"Item '{order_data['item']}' is not available"

        if not isinstance(order_data['quantity'], int) or order_data['quantity'] < 1:
            return False, "Quantity must be integer >= 1"

        return True, "Order is valid"

    def do_POST(self):
        if self.path != '/order':
            self._send_response(404, "Endpoint not found", "error")
            return

        try:
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            order_data = json.loads(post_data.decode('utf-8'))

            is_valid, message = self._validate_order(order_data)

            if is_valid:
                order_id = uuid.uuid4()
                self._send_response(200, "Order processed", "success", order_id)
            else:
                self._send_response(400, message, "error")

        except json.JSONDecodeError:
            self._send_response(400, "Invalid JSON format", "error")
        except Exception as e:
            self._send_response(500, f"Server error: {str(e)}", "error")


def main():
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, RequestHandler)
    print("Server running on port 8000...")
    httpd.serve_forever()


if __name__ == '__main__':
    main()