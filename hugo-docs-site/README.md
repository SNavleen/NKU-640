# Hugo Documentation Site

This is a Hugo-based documentation site for the NKU 640 course. The site contains various sections related to homework assignments, including detailed documentation for each stage of the projects.

## Project Structure

The project is organized into several directories and files, each serving a specific purpose:

- **content/**: Contains all the markdown files for the documentation.
  - **homework4/**: Documentation for Homework 4, including plans, PHP and Python implementations, and tutorials.
  - **stage2_rubric.md**: Rubric for Stage 2 of the homework.

- **layouts/**: Contains layout files that define the structure of the site.
  - **_default/**: Base layout files for the site.

- **static/**: Contains static files such as CSS and images.
  - **css/**: Custom CSS styles for the documentation site.

- **config.toml**: Configuration file for the Hugo site, specifying site parameters and theme settings.

## Getting Started

To get started with this documentation site, follow these steps:

1. **Install Hugo**: Make sure you have Hugo installed on your machine. You can download it from the [Hugo website](https://gohugo.io/getting-started/installation/).

2. **Run the Site**: Navigate to the project directory and run the following command to start the Hugo server:
   ```
   hugo server
   ```

3. **Access the Site**: Open your web browser and go to `http://localhost:1313` to view the documentation site.

## Contributing

If you would like to contribute to this documentation site, please follow the guidelines below:

- Ensure that your contributions adhere to the existing structure and formatting.
- Add new documentation files in the appropriate directories.
- Update the navigation in the `config.toml` file if necessary.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.