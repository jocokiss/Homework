# app/views.py
from flask import jsonify, Flask
from flask.views import MethodView

from app.insights import Insights

app = Flask(__name__)


class InsightsView(MethodView):
    def __init__(self):
        self.insights = Insights()

    def get(self, endpoint_name):
        """Endpoint handler for GET requests"""
        method_map = {
            "biggest_gainer": self.insights.get_biggest_gainer,
            "biggest_loser": self.insights.get_biggest_loser,
            "most_volatile": self.insights.get_most_volatile,
            "volatility_to_market_cap": self.insights.get_volatility_to_market_cap_ratio,
            "biggest_market_cap_growth": self.insights.get_biggest_market_cap_growth
        }

        # Retrieve the appropriate method
        if method := method_map.get(endpoint_name):
            return jsonify(method())
        else:
            return jsonify({"error": "Invalid endpoint"}), 404


# Register routes for each insight
app.add_url_rule('/<endpoint_name>', view_func=InsightsView.as_view('insights'))
