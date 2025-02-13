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

```bash
# Build and run with Docker Compose
docker-compose up --build
```

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

- Python 3.9 or higher
- Required packages listed in requirements.txt

### Running Tests

```bash
pytest tests/
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## Technical Details

- Built with Python 3.9+
- GUI implemented using tkinter with ttkbootstrap
- Data storage using JSON format
- Modular architecture for easy maintenance
- Comprehensive test suite

## License

MIT License

## Support

For support, please open an issue in the repository.
