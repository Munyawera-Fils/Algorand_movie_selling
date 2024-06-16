import React, { useState, useEffect } from "react";
import { useWallet } from "@txnlab/use-wallet";
import { Snackbar } from "@material-ui/core";
import { Alert } from "@material-ui/lab"; // Change this import to use the same alias as below
import { Movie } from "./types"; // Define Movie interface as per your requirement

const Home: React.FC = () => {
  const { activeAddress } = useWallet();
  const [movies, setMovies] = useState<Movie[]>([]);
  const [purchaseMessage, setPurchaseMessage] = useState<string>("");

  // Fetch movies from backend
  useEffect(() => {
    fetch("/api/movies")
      .then((response) => response.json())
      .then((data) => setMovies(data))
      .catch((error) => console.error("Error fetching movies:", error));
  }, []);

  const purchaseMovie = (movieId: string, price: number) => {
    // Logic to purchase movie goes here
    // You can use AlgoSigner or any other Algorand wallet integration
    console.log(`Purchase movie with ID ${movieId} for ${price} ALGO`);

    // For demonstration purposes, set a purchase message
    setPurchaseMessage(`Movie with ID ${movieId} purchased successfully!`);
  };

  return (
    <div className="hero min-h-screen bg-teal-400">
      <div className="hero-content text-center rounded-lg p-6 max-w-md bg-white mx-auto">
        <div className="max-w-md">
          <h1 className="text-4xl">Welcome to Movie Market</h1>
          <p className="py-6">Browse through the available movies and purchase them using your Algorand wallet.</p>

          <div className="grid">
            {movies.map((movie) => (
              <div key={movie.id} className="movie-card">
                <h2>{movie.title}</h2>
                <p>Description: {movie.description}</p>
                <p>Price: {movie.price} ALGO</p>
                {activeAddress && (
                  <button className="btn btn-primary" onClick={() => purchaseMovie(movie.id, movie.price)}>
                    Purchase
                  </button>
                )}
              </div>
            ))}
          </div>
        </div>
      </div>
      <Snackbar open={!!purchaseMessage} autoHideDuration={6000} onClose={() => setPurchaseMessage("")}>
        <Alert onClose={() => setPurchaseMessage("")} severity="success">
          {" "}
          {/* Change Alert to use @material-ui/lab */}
          {purchaseMessage}
        </Alert>
      </Snackbar>
    </div>
  );
};

export default Home;
