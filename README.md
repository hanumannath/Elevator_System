# Elevator System Project

This project implements a simplified elevator system using Python and Django with the Django Rest Framework. The system manages multiple elevators and handles elevator operations such as moving up and down, opening and closing doors, starting and stopping, displaying current status, and deciding whether to move up or down based on user requests.

The project includes the following components:

- Elevator models to represent individual elevators.
- API endpoints to initialize the elevator system, fetch elevator requests, fetch next destination floor, mark elevators as not working, and open/close the door.
- Serializers to convert model data to JSON and vice versa.
- Caching using Redis to improve performance.
- Database integration using PostgreSQL.

## Requirements

- Python 3
- Django
- Django Rest Framework
- PostgreSQL (optional, if using a database)
- Redis (optional, if using caching)

## Setup

1. Clone the repository:

   ```
   git clone https://github.com/hanumannath/elevator-system.git
   cd elevator-system
   ```

2. Create and activate a virtual environment (optional but recommended):

   ```
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install the dependencies:

   ```
   pip install -r requirements.txt
   ```

4. Run the Django development server:

   ```
   python manage.py runserver
   ```

5. The elevator system API should now be accessible at `http://localhost:8000/`.

## API Documentation

The elevator system provides the following API endpoints:

- `POST /api/elevators/initialize/`: Initializes the elevator system with the specified number of elevators.
- `GET /api/elevators/<elevator_id>/moving_direction/`: Retrieves the current moving direction of the specified elevator.
- `POST /api/elevators/<elevator_id>/mark_maintenance/`: Marks the specified elevator as not working or in maintenance.
- `POST /api/elevators/<elevator_id>/door_action/`: Performs the specified action (open or close) on the elevator door.
- `GET /api/elevators/<elevator_id>/next_destination/`: Retrieves the next destination floor for the specified elevator.
- `POST /api/elevators/<elevator_id>/set_current_floor/`: Sets the current floor for the specified elevator (when stopped).
- `GET /api/requests/?elevator_id=<elevator_id>`: Retrieves all requests for the specified elevator.
- `POST /api/requests/`: Creates a new request for the elevator with the specified floor number.

## Database

The project uses PostgreSQL as the database for storing elevator and request data. Make sure you have PostgreSQL installed and configure the database settings in the `settings.py` file.


## Dependencies

The project relies on the following dependencies, which are listed in the `requirements.txt` file:

- Django
- djangorestframework
- django-redis (optional, if using caching)
- psycopg2 (optional, if using PostgreSQL).
