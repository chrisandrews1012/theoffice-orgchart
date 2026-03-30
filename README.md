# The Office - Organizational Chart

A fun, interactive organizational chart visualizing the hierarchy of the Dunder Mifflin Scranton branch from the beloved TV show, "The Office".

## Description

While on the surface this is a fun project to explore the dynamics of the Scranton branch, under the hood, it is a **multi-component, data-driven application**. 

This project serves as a showcase of modern backend engineering, database management, and interactive web visualization using a robust Python stack. It demonstrates how to manage hierarchical data, securely handle database sessions, and containerize full-stack applications.

## Technical Highlights & Architecture

This project aims to highlight experience across several key technologies and concepts:

*   **Object-Relational Mapping (ORM)**: Uses **SQLAlchemy** to define hierarchical data models (`SQLEmployee`, `SQLManager`, `SQLExecutive`), handle complex queries (e.g., recursive dependencies and `UNION`s), and manage secure, reusable database sessions.
*   **Database Management**: Powered by **PostgreSQL** to robustly store and query the corporate reporting structure.
*   **Containerization**: Fully containerized using **Docker** (and Docker Compose) to orchestrate the web application and the PostgreSQL database environments seamlessly.
*   **Graph Theory & Traversal**: Leverages **NetworkX** to dynamically build directed graphs (`DiGraph`) from SQL queries, enabling organizational traversals and visual node mapping.
*   **Interactive UI**: Built with **Streamlit** to create a responsive, multi-page data application without writing boilerplate HTML/JS.

## Features

*   **Automated Data Pipeline**: Includes a build script (`build.py`) that uses SQLAlchemy bulk inserts to optimally clear and rebuild the database structure, properly respecting foreign key constraints.
*   **Interactive Organizational Chart**: Explore the chain of command, viewing employees, managers, and executives via a Streamlit multi-page interface.
*   **Robust Error Handling**: Features centralized database error handling, logging, and session management via custom Python decorators and context managers.

## Getting Started

Follow these instructions to get the project running on your local machine.

### Prerequisites

*   Docker and Docker Compose
*   Python 3.10+ and [uv](https://docs.astral.sh/uv/)

### Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/your-username/the-office-org-chart.git
    cd theoffice-orgchart
    ```
2. Sync the dependencies:
    ```bash
    uv sync
    ```
3.  Create a `.env` file in the project root directory to securely store your database configuration. This file is ignored by Git but is essential for the application to connect to the database. You can get started by copying the template:
    ```bash
    cp template.env .env
    ```
    You must then open the `.env` file and provide values for the following variables.

    *   `PG_USER`: The superuser for the PostgreSQL database.
    *   `PG_PASSWORD`: The password for the PostgreSQL superuser.
    *   `PG_DATABASE`: The name for the database to be created.
    *   `PG_PORT`: The external port to map to the PostgreSQL container's port 5432.
    *   `DB_HOST`: The hostname of the database server (`localhost`).
    *   `DB_USER`: The username for the non-superuser role that the application will use to connect.
    *   `DB_USER_PW`: The password for the application user.

4.  Start the PostgreSQL database container in the background:
    ```bash
    docker compose up -d
    ```
    
    > **Work in Progress:** The Docker Compose network setup is currently being fixed. For now, the application does not start automatically alongside the database.

5.  In a separate terminal, manually populate the database by running the build script:
    ```bash
    uv run python build.py rebuild
    ```

6.  Now, start the Streamlit web application:
    ```bash
    uv run streamlit run app.py
    ```

7.  The application will open in your default browser at `http://localhost:8501`.

## License

This project is licensed under the MIT License.
