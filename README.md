# Legacy Scoring Application

A professional scoring application for dance competitions, supporting Modern and Urban styles with multiple categories and age groups.

## Features

- Support for two dance styles:
  - Modern
  - Urban
- Four jury members per style
- Scoring criteria:
  - Technique (30 points)
  - Choreography (30 points)
  - Performance (30 points)
  - Expression (10 points)
- Categories per style:
  - Solo: Mini, Kids, Juniors, Teens, Adults
  - Duo: Mini, Kids, Juniors, Teens, Adults
  - Teams: Mini, Kids, Juniors, Teens, Adults
- Automatic calculation of:
  - Individual jury scores
  - Average scores
  - Rankings per category
  - Daily rankings per style
- Ex aequo rules implementation:
  1. Highest technique score wins
  2. If tied, highest performance score wins
  3. If still tied, highest choreography score wins

## Installation

### Using Docker

The application can be run using Docker in several ways:

#### Quick Start with Docker Compose

```bash
# Build and run with Docker Compose
docker-compose up --build

# Run in detached mode
docker-compose up -d

# Stop the application
docker-compose down

# View logs
docker-compose logs -f

# Rebuild specific service
docker-compose up --build legacy_scoring
```

#### Accessing the GUI Application in Docker

Since this is a GUI application using tkinter, accessing it in Docker requires some additional setup:

##### Linux
```bash
# Allow X server connections
xhost +local:docker

# Add to docker-compose.yml:
# services:
#   legacy_scoring:
#     environment:
#       - DISPLAY=$DISPLAY
#     volumes:
#       - /tmp/.X11-unix:/tmp/.X11-unix
#     network_mode: host
```

##### Windows with X Server (e.g., VcXsrv)
1. Install and start VcXsrv Windows X Server
2. Configure it to:
   - Display number: 0
   - Client: Start no client
   - Extra settings: Disable access control
3. Add to docker-compose.yml:
```yaml
services:
  legacy_scoring:
    environment:
      - DISPLAY=host.docker.internal:0
```

##### macOS with XQuartz
1. Install and start XQuartz
2. Allow connections:
```bash
xhost +localhost
```
3. Add to docker-compose.yml:
```yaml
services:
  legacy_scoring:
    environment:
      - DISPLAY=host.docker.internal:0
```

> Note: The GUI will appear directly on your desktop, not through a web browser, as this is a native application.

#### Manual Docker Commands

```bash
# Build the Docker image
docker build -t legacy_scoring .

# Run the container
docker run -p 5000:5000 \
  -v $(pwd)/data:/app/data \
  --name legacy_scoring \
  legacy_scoring

# Stop the container
docker stop legacy_scoring

# Remove the container
docker rm legacy_scoring
```

#### Docker Environment Variables

You can customize the application behavior using environment variables:

```yaml
# In docker-compose.yml:
services:
  legacy_scoring:
    environment:
      - DISPLAY=${DISPLAY}
      - DEBUG=1
      - LOG_LEVEL=DEBUG
```

#### Docker Volumes

The application uses a volume to persist data:

```yaml
# In docker-compose.yml:
services:
  legacy_scoring:
    volumes:
      - legacy_scoring_data:/app/data

volumes:
  legacy_scoring_data:
```

#### Development with Docker

For development, you can mount your local source code:

```yaml
# In docker-compose.yml:
services:
  legacy_scoring:
    volumes:
      - .:/app
      - legacy_scoring_data:/app/data

volumes:
  legacy_scoring_data:
```

#### Troubleshooting Docker

Common issues and solutions:

1. GUI not displaying:
   - Ensure DISPLAY variable is set correctly
   - Check X11 forwarding configuration

2. Data persistence issues:
   - Verify volume mounting
   - Check file permissions

3. Port conflicts:
   - Change port mapping: `-p 5001:5000`

### Manual Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python src/main.py
```

## Usage

1. Select the style tab (Modern/Urban)
2. Enter participant information:
   - Start number
   - Name
   - Category (Solo/Duo/Teams)
   - Age group
3. Input jury scores:
   - Technique (max 30 points)
   - Choreography (max 30 points)
   - Performance (max 30 points)
   - Expression (max 10 points)
4. Click "Calculate" to see:
   - Individual totals
   - Average score (out of 100)
5. Save scores using the "Save" button
6. View rankings and results
7. Use "Clear" to reset the form

## Project Structure

```
legacy_scoring/
├── src/               # Source code
│   ├── gui/          # GUI implementation
│   ├── models/       # Data models
│   └── utils/        # Utility functions
├── tests/            # Test files
└── data/             # Data storage
```

## Development

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Docker (optional)

### Environment Setup

```bash
# Create a virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Unix or MacOS:
source venv/bin/activate

# Install development dependencies
pip install -r requirements-dev.txt
```

### Running Tests

```bash
pytest tests/
```