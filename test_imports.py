print("Testing imports...")

try:
    import click
    print("✓ click imported")
except Exception as e:
    print(f"✗ click failed: {e}")

try:
    import rich
    print("✓ rich imported")
except Exception as e:
    print(f"✗ rich failed: {e}")

try:
    import yaml
    print("✓ yaml imported")
except Exception as e:
    print(f"✗ yaml failed: {e}")

try:
    from pydantic import BaseModel
    print("✓ pydantic imported")
except Exception as e:
    print(f"✗ pydantic failed: {e}")

print("\nAll imports checked!")
