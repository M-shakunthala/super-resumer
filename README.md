# Super Resumer

Super Resumer is an AI-powered job application assistant that helps you discover relevant opportunities, tailor your resume, optimize it for ATS systems, and automate application workflows across major hiring platforms.

## Why this project exists

This project is designed to reduce the repetitive work involved in job hunting by combining:

- intelligent job discovery
- resume tailoring and keyword optimization
- multi-platform application support
- tracking and analytics for the application process

## Key features

- Discover jobs from LinkedIn, Workday, Greenhouse, and Lever
- Tailor resumes to match job descriptions more closely
- Improve ATS compatibility with targeted optimization
- Automate application steps with built-in workflow logic
- Track applications, interviews, and outcomes in a dashboard
- Support retry and duplicate-prevention logic for smoother execution

## Quick start

1. Clone the repository
2. Create and activate a Python virtual environment
3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Add your API credentials and configuration to a `.env` file
5. Launch the app

```bash
streamlit run run_super_resumer.py
```

For more detailed setup steps, see the documentation in the [docs](docs) directory.

## Project structure

- [agents](agents) — core automation and matching logic
- [core](core) — orchestration and shared application flow
- [ui](ui) — Streamlit dashboard and user interface
- [tests](tests) — automated test coverage
- [docs](docs) — setup, usage, and architecture guides

## Documentation

- [Super Resumer Setup Guide](SUPER_RESUMER_SETUP.md)
- [Super Resumer User Guide](SUPER_RESUMER_USER_GUIDE.md)
- [Developer and architecture docs](docs)

## Testing

Run the test suite with:

```bash
pytest
```

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## Contributing

Contributions are welcome. Please read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request.
