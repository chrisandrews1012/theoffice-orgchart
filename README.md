# The Office - Organizational Chart

A fun, interactive organizational chart visualizing the hierarchy of the Dunder Mifflin Scranton branch from the beloved TV show, "The Office".

## Description

While on the surface this is a fun project to explore the dynamics of the Scranton branch (ever wondered who reports to the Regional Manager or who's in the Finance department?), under the hood, it is a **multi-component, data-driven application**. 

This project serves as a showcase of modern backend engineering, database management, and interactive web visualization using a robust Python stack. It demonstrates how to manage hierarchical data, securely handle database sessions, and containerize full-stack applications.

## Technical Highlights & Architecture

This project highlights experience across several key technologies and concepts:

*   **Object-Relational Mapping (ORM)**: Uses **SQLAlchemy** to define hierarchical data models (`SQLEmployee`, `SQLManager`, `SQLExecutive`), handle complex queries (e.g., recursive dependencies and `UNION`s), and manage secure, reusable database sessions.
*   **Database Management**: Powered by **PostgreSQL** to robustly store and query the corporate reporting structure.
*   **Containerization**: Fully containerized using **Docker** (and Docker Compose) to seamlessly orchestrate the web application and the PostgreSQL database environments.
*   **Graph Theory & Traversal**: Leverages **NetworkX** to dynamically build directed graphs (`DiGraph`) from SQL queries, enabling complex organizational traversals and visual node mapping.
*   **Interactive UI**: Built with **Streamlit** to create a responsive, multi-page data application without writing boilerplate HTML/JS.

## Features

*   **Automated Data Pipeline**: Includes a build script (`build.py`) that uses SQLAlchemy bulk inserts to optimally clear and rebuild the database structure, properly respecting foreign key constraints.
*   **Interactive Organizational Chart**: Explore the chain of command, viewing employees, managers, and executives via a Streamlit multi-page interface.
*   **Robust Error Handling**: Features centralized database error handling, logging, and session management via custom Python decorators and context managers.

## Getting Started

Follow these instructions to get a copy of the project up and running on your local machine.

### Prerequisites

*   Docker and Docker Compose
*   Python 3.10+ and [uv](https://docs.astral.sh/uv/) (if running locally without Docker)

### Installation (Docker - Recommended)

1.  Clone the repository:
    ```bash
    git clone https://github.com/your-username/theoffice-orgchart.git
    cd theoffice-orgchart
    ```
2.  Create a `.env` file in the project root to securely store your database configuration. This file is ignored by Git but is essential for the application to connect to the database. You can get started by copying the template:
    ```bash
    cp template.env .env
    ```
    You must then open the `.env` file and provide values for the following variables.

    > **Note:** Since the Docker environment creates a new, self-contained database for you, you can use any values you wish for these credentials. They will be used to initialize the new database instance inside the container.

    *   `PG_USER`: The superuser for the PostgreSQL database (e.g., `postgres`).
    *   `PG_PASSWORD`: The password for the PostgreSQL superuser.
    *   `PG_DATABASE`: The name for the database to be created (e.g., `office_db`).
    *   `PG_PORT`: The external port to map to the PostgreSQL container's port 5432 (e.g., `5432`).
    *   `DB_HOST`: The hostname of the database server (e.g., `db` when using Docker Compose, or `localhost` for local development).
    *   `DB_USER`: The username for the non-superuser role that the application will use to connect (e.g., `app_user`).
    *   `DB_USER_PW`: The password for the application user.
3.  Build and start the application and database services:
    ```bash
    docker-compose up --build
    ```
    
    > **Work in Progress:** The Docker Compose network setup is currently being fixed. For now, the application does not start automatically alongside the database.
4.  In a separate terminal, manually start the application:
    ```bash
    uv run streamlit run app.py
    ```
5.  The application will open in your default browser at `http://localhost:8501`.

### Local Development (Without Docker)

1.  Ensure you have a local PostgreSQL instance running. Create your `.env` file by copying the template (`cp template.env .env`).

    > **Important:** For this setup, you **must** update the `.env` file with the actual connection details for your existing local database instance. The application will use these values to connect to your server.
    > **Important:** For this setup, you **must** update the `.env` file with the actual connection details for your existing local database instance. The application will use these values to connect to your server. You will also need to set `DB_HOST` to `localhost`.
2.  Install the dependencies using `uv`:
    ```bash
    uv sync
    ```
3.  Initialize the database:
    ```bash
    uv run python build.py rebuild
    ```
4.  Start the Streamlit development server:
    ```bash
    uv run streamlit run app.py
    ```

## License

This project is licensed under the MIT License.
