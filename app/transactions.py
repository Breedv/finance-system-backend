from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Transaction
from app.decorators import role_required
from datetime import datetime

transactions_bp = Blueprint("transactions", __name__)


# ── CREATE (admin only) ──────────────────────────────────────────
@transactions_bp.route("/", methods=["POST"])
@role_required("admin")
def create_transaction():
    data = request.get_json()

    required = ["amount", "type", "category", "date"]
    for field in required:
        if not data or field not in data:
            return jsonify({"error": f"'{field}' is required"}), 400

    if data["type"] not in ["income", "expense"]:
        return jsonify({"error": "Type must be 'income' or 'expense'"}), 400

    if data["amount"] <= 0:
        return jsonify({"error": "Amount must be greater than 0"}), 400

    try:
        date = datetime.strptime(data["date"], "%Y-%m-%d").date()
    except ValueError:
        return jsonify({"error": "Date format must be YYYY-MM-DD"}), 400

    transaction = Transaction(
        amount=data["amount"],
        type=data["type"],
        category=data["category"].lower(),
        date=date,
        notes=data.get("notes", ""),
        user_id=int(get_jwt_identity())
    )
    db.session.add(transaction)
    db.session.commit()

    return jsonify({"message": "Transaction created", "transaction": transaction.to_dict()}), 201


# ── VIEW ALL (with optional filters) ────────────────────────────
@transactions_bp.route("/", methods=["GET"])
@role_required("viewer", "analyst", "admin")
def get_transactions():
    query = Transaction.query

    # Filters
    type_filter = request.args.get("type")
    category_filter = request.args.get("category")
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")

    if type_filter:
        query = query.filter_by(type=type_filter)
    if category_filter:
        query = query.filter_by(category=category_filter.lower())
    if start_date:
        query = query.filter(Transaction.date >= datetime.strptime(start_date, "%Y-%m-%d").date())
    if end_date:
        query = query.filter(Transaction.date <= datetime.strptime(end_date, "%Y-%m-%d").date())

    transactions = query.order_by(Transaction.date.desc()).all()
    return jsonify([t.to_dict() for t in transactions]), 200


# ── VIEW ONE ─────────────────────────────────────────────────────
@transactions_bp.route("/<int:id>", methods=["GET"])
@role_required("viewer", "analyst", "admin")
def get_transaction(id):
    transaction = Transaction.query.get_or_404(id)
    return jsonify(transaction.to_dict()), 200


# ── UPDATE (admin only) ──────────────────────────────────────────
@transactions_bp.route("/<int:id>", methods=["PUT"])
@role_required("admin")
def update_transaction(id):
    transaction = Transaction.query.get_or_404(id)
    data = request.get_json()

    if "amount" in data:
        if data["amount"] <= 0:
            return jsonify({"error": "Amount must be greater than 0"}), 400
        transaction.amount = data["amount"]
    if "type" in data:
        if data["type"] not in ["income", "expense"]:
            return jsonify({"error": "Type must be 'income' or 'expense'"}), 400
        transaction.type = data["type"]
    if "category" in data:
        transaction.category = data["category"].lower()
    if "date" in data:
        try:
            transaction.date = datetime.strptime(data["date"], "%Y-%m-%d").date()
        except ValueError:
            return jsonify({"error": "Date format must be YYYY-MM-DD"}), 400
    if "notes" in data:
        transaction.notes = data["notes"]

    db.session.commit()
    return jsonify({"message": "Transaction updated", "transaction": transaction.to_dict()}), 200


# ── DELETE (admin only) ──────────────────────────────────────────
@transactions_bp.route("/<int:id>", methods=["DELETE"])
@role_required("admin")
def delete_transaction(id):
    transaction = Transaction.query.get_or_404(id)
    db.session.delete(transaction)
    db.session.commit()
    return jsonify({"message": "Transaction deleted"}), 200