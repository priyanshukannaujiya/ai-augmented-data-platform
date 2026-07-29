from generator.generators.customer_generator import main as generate_customers
from generator.generators.product_generator import main as generate_products
from generator.generators.session_generator import main as generate_sessions
from generator.generators.clickstream_generator import main as generate_clickstream
from generator.generators.order_generator import main as generate_orders


def main():
    print("=" * 60)
    print("🚀 AI-Augmented E-Commerce Synthetic Data Generator")
    print("=" * 60)

    try:
        print("\n[1/5] Generating Customers...")
        generate_customers()
        print("✅ Customers Generated")

        print("\n[2/5] Generating Products...")
        generate_products()
        print("✅ Products Generated")

        print("\n[3/5] Generating Sessions...")
        generate_sessions()
        print("✅ Sessions Generated")

        print("\n[4/5] Generating Clickstream...")
        generate_clickstream()
        print("✅ Clickstream Generated")

        print("\n[5/5] Generating Orders...")
        generate_orders()
        print("✅ Orders Generated")

        print("\n" + "=" * 60)
        print("🎉 Synthetic Dataset Generated Successfully!")
        print("=" * 60)

    except Exception as e:
        print("\n❌ ERROR OCCURRED")
        print(type(e).__name__)
        print(e)


if __name__ == "__main__":
    main()