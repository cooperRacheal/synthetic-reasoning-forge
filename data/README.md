# data/

> Directory for generated output files and experimental data

## Purpose

This directory is intended for storing generated visualizations and data files produced by analysis scripts. Files in this directory are gitignored to avoid tracking binary output files in version control.

## Gitignored File Types

Per `.gitignore`:
- `*.png` - Generated phase portraits and plots
- `*.jpg` - Exported visualization images
- `*.pdf` - Publication-ready figures

## Usage

Scripts and examples may save output to this directory:

```python
# Example: Save phase portrait
plot_phase_portrait(
    sol.t,
    sol.y,
    save_path='data/lorenz_attractor.png'
)
```

## Note

For demonstration plots tracked in git, see `examples/output/` directory.

---

**Last Updated:** 2026-01-21
