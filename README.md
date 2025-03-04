# wp-posts-strip-color

## Overview
`wp_posts_strip_color` is a Python script designed to remove `color` attributes from inline `style` tags within WordPress post content.

## Features
- Parses WordPress post content to remove only `color` attributes while preserving other styles.
- Provides a before-and-after preview of modified tags.
- Allows interactive confirmation for each change.
- Supports a `--apply-all` flag to apply all changes without manual confirmation.

## Requirements
- Python >= 3.11

## Installation
1. Create a virtual environment:
   ```sh
   python3 -m venv venv
   ```
2. Activate the virtual environment:
   ```sh
   source venv/bin/activate
   ```
3. Install dependencies from `requirements.txt`:
   ```sh
   pip install -r requirements.txt
   ```

## Usage
Run the script with the required database credentials:
```sh
python3 wp_posts_strip_color.py --host <DB_HOST> --user <DB_USER> --password <DB_PASS> --database <DB_NAME>
```

To apply all changes without manual confirmation, use:
```sh
python3 wp_posts_strip_color.py --host <DB_HOST> --user <DB_USER> --password <DB_PASS> --database <DB_NAME> --apply-all
```

## Example Output
```
Post ID: 123
Changes:
Before:
<span style="color: red; font-size: large;">Example</span>
After:
<span style="font-size: large;">Example</span>
Apply change? (y/n):
```
