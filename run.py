#Initiates the app
from app import create_app
from app.simulation.simulation import start_simulation_engine

app = create_app()


if __name__ == "__main__":
  start_simulation_engine()
  app.run(debug=True)
