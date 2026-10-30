import argparse
from app import create_app

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["secure", "vulnerable"], default="secure")
    parser.add_argument("--port", type=int, default=5000)
    parser.add_argument("--host", default="127.0.0.1")
    args = parser.parse_args()

    app = create_app(mode=args.mode)
    app.run(host=args.host, port=args.port, debug=False)

if __name__ == "__main__":
    main()
