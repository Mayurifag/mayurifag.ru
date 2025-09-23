# Private Files Directory

This directory is intended for storing sensitive files that should not be committed to version control.

## Usage

### Cookies File for Mus

If you have a `cookies.txt` file that you want to mount into the mus container, simply place it in this directory:

```sh
cp your-cookies.txt inventories/my-provision/private/cookies.txt
```

The file will be automatically detected and mounted read-only at `/app_data/cookies.txt` inside the container.

## Security Notes

- Add `private/` to your `.gitignore` to prevent accidental commits
- Ensure proper file permissions (600 or 644) for sensitive files
- The cookies file will be mounted read-only for security

## File Structure

```text
inventories/my-provision/
├── group_vars/
│   └── sample.yml
├── private/
│   ├── README.md (this file)
│   └── cookies.txt (your private cookies file)
└── inventory
```
