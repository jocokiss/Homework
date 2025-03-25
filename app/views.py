"""Module containing views for the app."""
from flask import Flask, render_template
from flask.views import MethodView

from app.insights import Insights

app = Flask(__name__)


@app.route("/", methods=["GET"])
def homepage():
    """Homepage displaying links to insights"""
    insights = [
        "biggest_gainer",
        "biggest_loser",
        "most_volatile",
        "top_volatility_to_market_cap",
        "biggest_market_cap_growth"
    ]
    return render_template("homepage.html", insights=insights)


class InsightsView(MethodView):
    def __init__(self):
        self.insights = Insights()
        self.method_map = {
            "biggest_gainer": self.insights.get_biggest_gainer,
            "biggest_loser": self.insights.get_biggest_loser,
            "most_volatile": self.insights.get_most_volatile,
            "top_volatility_to_market_cap": self.insights.get_top_volatility_to_market_cap_ratio,
            "biggest_market_cap_growth": self.insights.get_biggest_market_cap_growth
        }

    def get(self, endpoint_name):
        """Endpoint handler for GET requests"""
        if method := self.method_map.get(endpoint_name):
            insight = method()

            if insight:
                return render_template("insight_page.html",
                                       insight_title=endpoint_name.replace('_', ' ').title(),
                                       insight=insight)

        return render_template("error.html", message="Invalid insight requested"), 404


# Register routes for each insight
app.add_url_rule('/<endpoint_name>', view_func=InsightsView.as_view('insights'))
