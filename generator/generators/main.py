from generator.generators.customer_generator import main as generate_customers
from generator.generators.product_generator import main as generate_products
from generator.generators.session_generator import main as generate_sessions
from generator.generators.clickstream_generator import main as generate_clickstream
from generator.generators.order_generator import main as generate_orders

def main():

    print("=" * 60)
    print(" E-Commerce Synthetic Data Generator ")
    print("=" * 60)

    print("\n[1/5] Generating Customers...")
    generate_customers()

    print("\n[2/5] Generating Products...")
    generate_products()

    print("\n[3/5] Generating Sessions...")
    generate_sessions()

    print("\n[4/5] Generating Clickstream...")
    generate_clickstream()

    print("\n[5/5] Generating Orders...")
    generate_orders()

    print("\n" + "=" * 60)
    print("Synthetic dataset generated successfully.")
    print("=" * 60)


if __name__ == "__main__":
    main()