# Shopping List

Shopping list memo application using Python Flask.

The application allows user to add/edit/delete items to buy and show them on a shopping list. It also allows add information of the choices of each item to buy.

## Demo

[https://web-shoppinglist-python-flask.onrender.com](https://web-shoppinglist-python-flask.onrender.com)

### Demo Account

 - Email: ```user1@email.com```
 - Password: ```user1```

## Technology Stack

The application uses following technologies:

- Python : Programming Language
- Flask : Web Framework
- MongoDB Atlas : NoSQL Database on Cloud
- HTML/CSS : Front-End Development
- Bootstrap : CSS Framework

## Features

- User authentication: Register/Login/Logout
- Create/Update/Delete an item to buy
- Create/Delete choices information of each item to buy
- Move items which was bought from shopping list to bought list

## Start the Application

### 1. Clone the repository
```
git clone https://github.com/Raphaelhhc/Shoppinglist-Python-Flask
```

### 2. Change into the project directory
```
cd Shoppinglist-Python-Flask
```

### 3. Create a virtual environment
```
python3 -m venv .venv
```

### 4. Activate the virtual environment
```
.venv\Scripts\activate
```

### 5. Install the dependencies
```
pip install -r requirements.txt
```

### 6. Set environmental variables
```
MONGODB_URI= <Enter your MongoDB Atlas URI>
SECRET_KEY= <Enter password encoding key>
```
* If no MongoDB Atlas account: refer to [https://www.mongodb.com/docs/atlas/](https://www.mongodb.com/docs/atlas/) to create one.

### 7. Run the Flask development server
```
flask run
```

### 8. Open your web browser and visit [http://localhost:5000](http://localhost:5000)

## Screenshots

 - Login Page
 ![App Screenshot](https://res.cloudinary.com/doe9mfetd/image/upload/v1686472538/Shopping-List_GITHUB/Login_Page_tu8o8p.png)
 - Shopping List Page
![App Screenshot](https://res.cloudinary.com/doe9mfetd/image/upload/v1686472539/Shopping-List_GITHUB/Shopping_List_Page_vprnsl.png)
 - Item Detail Page
![App Screenshot](https://res.cloudinary.com/doe9mfetd/image/upload/v1686473367/Shopping-List_GITHUB/Item_Detail_Page_dcfovd.png)
 - Bought List
![App Screenshot](https://res.cloudinary.com/doe9mfetd/image/upload/v1686473416/Shopping-List_GITHUB/Bought_List_Page_exvwku.png)

