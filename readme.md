# Movie Management System

Welcome to the Movie Management System project! This project was developed by me, a teaching assistant at Jiangsu Normal University (JSNU), to be used as a practical training tool for junior students. The entire development process was carried out by me, aiming to provide hands-on experience with web development using Flask.

## Project Overview

The Movie Management System is designed to manage movies, tags, previews, users, comments, collections, logs, and permissions. The following steps outline the setup and functionality of the system.

### 1. Import Database
- Import `movie.sql` file into the MySQL database.

### 2. Create `app` Package
- Move `static` and `templates` into the `app` package.
  - `static`: Contains common resources (js, css, jquery, images).
  - `templates`: Stores static files (html, jsp).
- Delete `app.py`.

### 3. Create `manage.py` File
- Create `manage.py` under `JSNUMovie2024` folder.
- `manage.py` replaces `app.py`.
- If `flask_script` error occurs:
  ```bash
  pip install flask-script
  ```

### 4. Update `__init__.py` in `app` Package
- Install necessary modules:
  ```bash
  pip install flask-sqlalchemy flask-redis
  ```
- Configure project name, database connection, cache settings, DEBUG mode, and blueprint.

### 5. Create `admin` Package in `app`
- Set up module blueprint in `__init__.py`.
- Create `views.py` and implement `login` function.

### 6. Create `login.html`
- Place `login.html` under `app/templates/admin`.

### 7. Configure Run Settings
- Edit configurations for running the server.
- Set the main script path to `manage.py`.

### 8. Update `login.html`
- Copy necessary resources to the `static` folder and modify `login.html`.

### 9. Update `views.py`
- Modify `login` function and create `forms.py`:
  ```bash
  pip install flask-wtf==1.0.0
  ```

### 10. Create `models.py` in `app`
- Implement `Admin` and `Adminlog` classes.

### 11. Develop Features
- Implement various features such as adding and managing tags, movies, previews, users, comments, collections, logs, and permissions. Detailed steps include updating views, templates, forms, and models to handle CRUD operations and other functionalities.
- the movies will be loaded on the path 'uploads/'

## Running the Project

To run the project, follow these steps:

1. Import the database by executing the `movie.sql` file in MySQL.
2. Navigate to the project directory:
    ```bash
    cd JSNUMovie2024
    ```
3. Install required packages:
    ```bash
    pip install -r requirements.txt
    ```
4. Run the server:
    ```bash
    python manage.py runserver
    ```
5. Open your browser and navigate to `http://127.0.0.1:5000/admin/login` to access the login page.

## Project Structure

- **app/**
  - `__init__.py`
  - `admin/`
    - `__init__.py`
    - `views.py`
    - `forms.py`
    - `templates/`
      - `login.html`
      - `index.html`
      - `admin/`
        - `tag_add.html`
        - `tag_list.html`
        - `tag_edit.html`
        - `movie_add.html`
        - `movie_list.html`
        - `movie_edit.html`
        - `preview_add.html`
        - `preview_list.html`
        - `preview_edit.html`
        - `user_list.html`
        - `user_view.html`
        - `comment_list.html`
        - `moviecol_list.html`
        - `userlog_list.html`
        - `adminlog_list.html`
        - `oplog_list.html`
        - `auth_add.html`
        - `auth_list.html`
        - `auth_edit.html`
  - `static/`
    - `js/`
    - `css/`
    - `jquery/`
    - `images/`
  - `models.py`
  - `views.py`

- **manage.py**

## Contributing

If you wish to contribute to this project, feel free to fork the repository and submit a pull request. For any issues or feature requests, please open an issue on the GitHub repository.

## License

This project is licensed under the MIT License.

Feel free to reach out if you have any questions or need further assistance!

**Happy Coding!** :smile: :movie_camera:

---

This project was created by Ray, a teaching assistant at Jiangsu Normal University (JSNU), to help junior students with practical web development training. The entire project was developed solely by me.

---

```markdown
![JSNU Logo](https://pic.baike.soso.com/p/20131116/20131116104105-236850122.jpg)
```
