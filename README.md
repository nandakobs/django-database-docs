# Django Database Docs

This repository provides a convenient solution to generate a PlantUML (.puml) diagram representing your Django project's database schema and create a markdown file containing the summary and details of all its tables.

With just two simple commands, you can visualize your Django project's database structure and generate comprehensive documentation in markdown format.

## How to Use

1. Download the `django_database_docs` folder or clone this repository.

2. Copy the downloaded folder and paste it into your Django project's directory. Your project structure should look like this:

    ```
    ├── your_cool_project/
    │    ├── __init__.py
    │    ├── settings.py
    │    ├── urls.py
    │    ├── apps/
    │    └── django_database_docs/
    ```

3. Open your terminal and navigate to the `django_database_docs` folder that you just pasted into your Django project.

4. Run the `models_to_puml.py` file in the terminal. This script will analyze your Django project's models and generate a file called `result.puml`.

5. Open the `result.puml` file and check for any occurrences of the word "undefined". The script only recognizes Django's default fields, so you need to correct their type accordingly. Ensure all fields are correctly defined to ensure accurate generation of the markdown file in the next step.

6. After correcting any "undefined" fields in `result.puml`, run the `puml_to_markdown.py` file in the terminal. This script will read the `result.puml` file and generate a file called `data_dict.md`.

7. Congratulations! The `data_dict.md` file is now created and ready for you to fill in with all the descriptions and details of your Django project's tables.

You're all set to document your Django project's database schema with ease and clarity!

  
  ### Tips
  - Formatting the tables in a markdown file can be very messy. So here is the thing, if your IDE is VS Code you can use the [Table Formatter](https://marketplace.visualstudio.com/items?itemName=shuworks.vscode-table-formatter) extension to formmatt them all with one command.

## How it Works

The script consists of two parts that work together to generate a PostgreSQL schema diagram and a data dictionary section informing the tables in markdown format.

### Script 1: Convert Fields and Generate .puml Diagram

The `models_to_puml.py` script analyzes all the tables in the project and converts the field types to be compatible with PostgreSQL. And then, it generates a diagram in PlantUML (.puml) format.

1. The script scans the project's tables and converts the field types to PostgreSQL-compatible types.
2. It writes the converted field types and relationships (FK and M2M) to a .puml file, creating a diagram that represents the database schema.
3. However, note that the script currently only converts Django's default fields. You need to manually check if there are any fields with the value "undefined" that require special handling.

### Script 2: Generate Summary and Tables in Markdown

The `puml_to_markdown.py` script reads the .puml file generated by Script 1 and uses it to generate a markdown file that contains a summary of the database schema and its tables.

1. The script reads the .puml file generated in Script 1.
2. It extracts the schema information, including table names, field names, and relationships from the .puml file.
3. Using this information, the script generates a markdown file that contains a summary of the database schema and its tables.

By running both scripts, you can easily convert your Django project's database schema to a PostgreSQL-compatible format, visualize it using a .puml diagram, and generate a comprehensive a markdown file that contains a summary of the database schema and its tables.


## Contributions

Contributions are welcome! If you find any issues, have suggestions for improvements, or want to add new features, feel 
free to submit a pull request.
