# Legacy Scoring Application

A scoring application for dance competitions.

## Setup

1. Install Docker and Docker Compose
2. Run `docker-compose up --build`

## Development

- Data files are stored in `./data`
- Source code is in `./src`
- GUI is built with PySide6 (Qt)

## Usage

1. Select style (Modern/Urban)
2. Navigate through participants
3. Enter scores for each jury member
4. View rankings in the Rankings tab

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

> **Important**: This is a GUI application, so special setup is required for the display to work.
> This application currently only supports Linux systems.
> The container will exit if the display setup is incorrect.

```bash
# Build and run with Docker Compose
docker-compose up --build
```

#### Display Setup (Required)

Before running the application, set up X11 display forwarding:

```bash
# Allow X server connections (run this before starting the container)
xhost +local:docker

# Your docker-compose.yml should include:
services:
  legacy_scoring:
    environment:
      - DISPLAY=$DISPLAY
    volumes:
      - /tmp/.X11-unix:/tmp/.X11-unix
    network_mode: host
```

#### Running the Application

After setting up the display:
```bash
# Start the application
docker-compose up

# To run in background
docker-compose up -d

# View logs if running in background
docker-compose logs -f

# Stop the application
docker-compose down
```

> **Note**: The GUI window should appear directly on your desktop after starting the container.
> If the container exits immediately, check your display setup and logs:
> ```bash
> docker-compose logs
> ```

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

#### Troubleshooting

If the container exits immediately:
1. Check if X server is running and properly configured
2. Verify DISPLAY environment variable is set correctly
3. Ensure X server allows connections
4. Run without `-d` flag to see error messages

### Manual Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python src/main.py
```

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