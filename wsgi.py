from app import create_app

app = create_app()


@app.route('/')
def index():
    print("pong")
    return {"ping": "pong"}


if __name__ == "__main__":
    app.run()
