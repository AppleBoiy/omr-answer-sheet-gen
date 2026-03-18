# Contributing to OMR Generator

Thank you for your interest in contributing to OMR Generator!

## How to Contribute

### Reporting Bugs

If you find a bug, please open an issue with:
- A clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Your environment (OS, Python version)
- Sample code if applicable

### Suggesting Features

Feature requests are welcome! Please:
- Check if the feature already exists
- Describe the use case clearly
- Explain why it would be useful

### Code Contributions

1. **Fork the repository**
2. **Create a branch** for your feature
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow the existing code style
   - Add docstrings to new functions/classes
   - Keep changes focused and atomic

4. **Test your changes**
   ```bash
   PYTHONPATH=. python examples/basic_usage.py
   ```

5. **Commit your changes**
   ```bash
   git commit -m "Add: brief description of changes"
   ```

6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Open a Pull Request**

## Code Style

- Follow PEP 8 guidelines
- Use type hints where possible
- Write clear docstrings
- Keep functions focused and small
- Use meaningful variable names

## Development Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/omr-generator.git
cd omr-generator

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .
```

## Testing

Before submitting a PR, please test:

```bash
# Run basic examples
PYTHONPATH=. python examples/basic_usage.py

# Run batch examples
PYTHONPATH=. python examples/batch_generation.py
```

## Documentation

- Update README.md if adding new features
- Update USAGE.md for Thai documentation
- Add examples to demonstrate new features

## Questions?

Feel free to open an issue for any questions!

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
