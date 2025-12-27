from core.database import engine

def check_db():
    try:
        with engine.connect() as conn:
            print("✅ Database connection successful")
    except Exception as e:
        print("❌ Database connection failed")
        print(e)

if __name__ == "__main__":
    check_db()
