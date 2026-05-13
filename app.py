##############################################################################
# app/app.py
# WHY THIS FILE EXISTS:
#   This is the web application being deployed to Kubernetes.
#   Intentionally minimal — the focus of this project is the
#   infrastructure and orchestration, not the application itself.
##############################################################################

from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    return """
    <h1>DevOps Project — Running on EKS</h1>
    <p>Deployed via Kubernetes on AWS Elastic Kubernetes Service.</p>
    <p>Container orchestrated by Kubernetes — served by a LoadBalancer.</p>
    """


@app.route("/health")
def health():
    return {"status": "healthy", "service": "flask-eks-app"}, 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)