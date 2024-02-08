# 0x00. Personal Data (Back-end | Authentication)

This is a project based on the 0x00 module of the Holberton School's Back-end curriculum, focusing on personal data protection and authentication. The project consists of several tasks, and we'll guide you through each one.

## Requirements

- All code should be written and tested on Ubuntu 18.04 LTS using Python 3.7.
- Ensure all your code files end with a newline.
- The first line of every code file should be `#!/usr/bin/env python3`.
- Include a `README.md` file at the root of your project folder.
- Use `pycodestyle` style (version 2.5) for your code.
- All your code files must be executable.
- File lengths will be checked using `wc`.
- All modules, classes, and functions should have documentation.
- Use type annotations for all functions.
- Documentation should provide a clear explanation of the purpose of the module, class, or method.
- Functions should be implemented following the provided requirements.

## Tasks

### 0. Regex-ing

- Write a function `filter_datum` that obfuscates personal data in log messages.
- Arguments:
  - `fields`: a list of strings representing fields to obfuscate.
  - `redaction`: a string representing how the field will be obfuscated.
  - `message`: a string representing the log line.
  - `separator`: a string representing the character separating fields in the log line.
- Use a regex to replace occurrences of certain field values.
- `filter_datum` should be less than 5 lines long and use `re.sub` to perform the substitution with a single regex.
