import json
import logging
from datetime import datetime
from typing import Dict, List, Optional

# configure basic logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

stock_data: Dict[str, int] = {}


def add_item(item: str, qty: int = 0, logs: Optional[List[str]] = None) -> None:
    """Add qty of item to the global stock_data.

    Args:
        item: item name (string)
        qty: integer quantity to add (can be 0 or positive)
        logs: optional list to append a human-readable log entry
    """
    if logs is None:
        logs = []

    if not isinstance(item, str):
        logging.error("add_item: item must be a string, got %r", item)
        return

    if not isinstance(qty, int):
        logging.error("add_item: qty must be an int, got %r", qty)
        return

    stock_data[item] = stock_data.get(item, 0) + qty
    logs.append(f"{datetime.now()}: Added {qty} of {item}")
    logging.info("Added %d of %s. New qty: %d", qty, item, stock_data[item])


def remove_item(item: str, qty: int) -> None:
    """Remove qty of item from stock_data if possible.

    If the item does not exist, logs a warning. If qty is larger than current,
    the item is removed entirely.
    """
    if not isinstance(item, str):
        logging.error("remove_item: item must be a string, got %r", item)
        return

    if not isinstance(qty, int):
        logging.error("remove_item: qty must be an int, got %r", qty)
        return

    try:
        if item not in stock_data:
            logging.warning("remove_item: item '%s' not found.", item)
            return

        stock_data[item] -= qty
        if stock_data[item] <= 0:
            del stock_data[item]
            logging.info("remove_item: item '%s' removed from inventory.", item)
        else:
            logging.info(
                "remove_item: decreased '%s' by %d. New qty: %d",
                item,
                qty,
                stock_data[item],
            )
    except KeyError as exc:
        logging.exception("Unexpected KeyError while removing item: %s", exc)


def get_qty(item: str) -> int:
    """Return current quantity for item, or 0 if not present."""
    if not isinstance(item, str):
        logging.error("get_qty: item must be a string, got %r", item)
        return 0
    return stock_data.get(item, 0)


def load_data(file_name: str = "inventory.json") -> Dict[str, int]:
    """Load inventory from JSON file and return it."""
    try:
        with open(file_name, "r", encoding="utf-8") as file:
            data = json.load(file)
            if not isinstance(data, dict):
                logging.warning(
                    "load_data: file did not contain a dict; resetting stock_data."
                )
                return {}
            return {str(k): int(v) for k, v in data.items()}
    except FileNotFoundError:
        logging.info("load_data: %s not found. Starting with empty inventory.", file_name)
        return {}
    except (json.JSONDecodeError, ValueError) as exc:
        logging.error("load_data: failed to decode JSON (%s). Resetting inventory.", exc)
        return {}


def save_data(file_name: str = "inventory.json") -> None:
    """Persist current stock_data to a JSON file."""
    try:
        with open(file_name, "w", encoding="utf-8") as file:
            json.dump(stock_data, file, indent=2)
            logging.info("Saved inventory to %s.", file_name)
    except OSError as exc:
        logging.exception("save_data: failed to write to %s: %s", file_name, exc)


def print_data() -> None:
    """Print a human-readable report of items and quantities."""
    logging.info("Items Report")
    for item, qty in stock_data.items():
        logging.info("%s -> %d", item, qty)


def check_low_items(threshold: int = 5) -> List[str]:
    """Return a list of items whose quantity is strictly less than threshold."""
    if not isinstance(threshold, int):
        logging.error("check_low_items: threshold must be int, got %r", threshold)
        return []
    return [item for item, qty in stock_data.items() if qty < threshold]


def main() -> None:
    """Demonstration main that performs a few inventory operations."""
    add_item("apple", 10)
    add_item("banana", 2)
    add_item("pear", 0)
    remove_item("apple", 3)
    remove_item("orange", 1)
    logging.info("Apple stock: %d", get_qty("apple"))
    logging.info("Low items: %s", check_low_items())
    save_data()
    data = load_data()
    # update the existing global dict without rebinding the name
    stock_data.clear()
    stock_data.update(data)
    print_data()


if __name__ == "__main__":
    main()
