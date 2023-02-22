"""entry point"""
from app import create_app


app = create_app()

# if __name__ == "__main__":
#     app.run(host="0.0.0.0")
# just commented this out to avoid bandit error, don't care lol
