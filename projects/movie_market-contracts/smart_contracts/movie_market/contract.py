# contract.py

from flask import Flask, jsonify, request # type: ignore
from flask_cors import CORS # type: ignore
import beaker
import pyteal as pt

app = Flask(__name__)
CORS(app)  # Allow Cross-Origin Resource Sharing (CORS)

# Define the movie market application
movie_market = beaker.Application("movie_market")

# Define your smart contract function
@app.external
def purchase_movie(movie_id: pt.abi.String) -> pt.Expr:
    # Logic to handle movie purchase goes here
    # For demonstration purposes, simply return success message
    return pt.App.localPut(pt.Bytes("movie_purchased"), movie_id, pt.Bytes("true"))


# Mock movie data
movies = [
    {"id": "1", "title": "Movie 1", "description": "Description of Movie 1", "price": 10},
    {"id": "2", "title": "Movie 2", "description": "Description of Movie 2", "price": 15},
    {"id": "3", "title": "Movie 3", "description": "Description of Movie 3", "price": 20},
]

@app.route('/api/movies', methods=['GET'])
def get_movies():
    return jsonify(movies)

@app.route('/api/purchase', methods=['POST'])
def purchase_movie_api():
    data = request.json
    movie_id = data.get('movie_id')
    # Call the smart contract function
    purchase_movie(movie_id)
    # Return success message
    return jsonify({"message": f"Movie with ID {movie_id} purchased successfully!"})

if __name__ == '__main__':
    app.run(debug=True)
