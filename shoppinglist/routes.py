import uuid
import functools
from flask import (
    Blueprint,
    render_template,
    url_for,
    current_app,
    redirect,
    session,
    flash
)
from shoppinglist.forms import (
    ItemForm,
    ExtendedItemForm,
    ChoiceForm,
    RegisterForm,
    LoginForm
)

from dataclasses import asdict
from shoppinglist.models import Item, Choice, User
from passlib.hash import pbkdf2_sha256

pages = Blueprint("pages", __name__, template_folder="views",
                  static_folder="static")


def login_required(route):

    @functools.wraps(route)

    def route_wrapper(*args, **kwargs):
        if session.get("email") is None:
            return redirect(url_for(".login"))
        return route(*args, **kwargs)
    
    return route_wrapper


# USER

@pages.route("/register", methods=["GET", "POST"])
def register():

    if session.get("email"):
        return redirect(url_for(".index"))
    
    form = RegisterForm()

    if form.validate_on_submit():
        user = User(
            _id=uuid.uuid4().hex,
            email=form.email.data,
            password=pbkdf2_sha256.hash(form.password.data),
        )       
        current_app.db.user.insert_one(asdict(user))
        flash("User registered successfully", "success")
        return redirect(url_for(".login"))
    
    return render_template("users/register.html", title="Shopping List - Register", form=form)


@pages.route("/login", methods=["GET", "POST"])
def login():

    if session.get("email"):
        return redirect(url_for(".index"))
    
    form = LoginForm()

    if form.validate_on_submit():
        user_data = current_app.db.user.find_one({"email": form.email.data})
        if not user_data:
            flash("Login credentials not correct", category="danger")
            return redirect(url_for(".login"))
        user = User(**user_data)
        if user and pbkdf2_sha256.verify(form.password.data, user.password):
            session["user_id"] = user._id
            session["email"] = user.email
            return redirect(url_for(".index"))
        flash("Login credentials not correct", category="danger")

    return render_template("users/login.html", title="Shopping List - Login", form=form)


@pages.route("/logout")
def logout():

    del session["email"]
    del session["user_id"]

    return redirect(url_for(".home", title="Home"))


# WEB PAGE

@pages.route("/")
@login_required
def index():

    user_data = current_app.db.user.find_one({"email": session["email"]})
    user = User(**user_data)
    item_data = current_app.db.item.find({"_id": {"$in": user.items}})
    items = [Item(**item) for item in item_data]

    return render_template("index.html", title="To Buy List", items_data=items)

@pages.route("/boughtList")
@login_required
def boughtList():

    user_data = current_app.db.user.find_one({"email": session["email"]})
    user = User(**user_data)
    item_data = current_app.db.item.find({"_id": {"$in": user.items}})
    items = [Item(**item) for item in item_data]

    return render_template("boughtList.html", title="Bought List", items_data=items)

@pages.route("/add_item", methods=["GET", "POST"])
@login_required
def add_item():

    form = ItemForm()

    if form.validate_on_submit():
        item = Item(
            _id=uuid.uuid4().hex,
            name=form.name.data,
            cost=form.cost.data,
            priority=form.priority.data
        )
        current_app.db.item.insert_one(asdict(item))
        current_app.db.user.update_one({"_id": session["user_id"]}, {"$push": {"items": item._id}})
        return redirect(url_for(".index"))

    return render_template("items/add_item.html", title="Shopping List - Add Item", form=form)


@pages.route("/item/<string:_id>")
@login_required
def item_detail(_id: str):

    item = current_app.db.item.find_one({"_id": _id})
    item_var = Item(**item)
    choice_data = current_app.db.choice.find({"_id": {"$in": item_var.choices}})
    choices = [Choice(**choice) for choice in choice_data]

    return render_template("items/detail.html", title="Item Detail", item=item, choices_data=choices)


@pages.route("/edit_item/<string:_id>", methods=["GET", "POST"])
@login_required
def edit_item(_id: str):

    item = Item(**current_app.db.item.find_one({"_id": _id}))

    form = ExtendedItemForm(obj=item)

    if form.validate_on_submit():
        item.name=form.name.data
        item.cost=form.cost.data
        item.priority=form.priority.data
        item.memo=form.memo.data
        item.requirement=form.requirement.data
        current_app.db.item.update_one({"_id": item._id}, {"$set": asdict(item)})
        return redirect(url_for(".item_detail", _id=item._id))

    return render_template("items/edit_item.html", item=item, form=form)


@pages.route("/item_bought/<string:_id>", methods=["GET", "POST"])
@login_required
def item_bought(_id: str):

    item = Item(**current_app.db.item.find_one({"_id": _id}))
    if not item.bought:
        current_app.db.item.update_one({"_id": item._id}, {"$set": {"bought": True}})
    
    return redirect(url_for(".index"))


@pages.route("/item_delete/<string:_id>", methods=["GET", "POST"])
@login_required
def item_delete(_id: str):

    item = Item(**current_app.db.item.find_one({"_id": _id}))
    current_app.db.item.delete_one({"_id": item._id})
    
    return redirect(url_for(".index"))

@pages.route("/choice_delete/<string:_idI>/<string:_idC>", methods=["GET", "POST"])
@login_required
def choice_delete(_idI: str, _idC: str):

    current_app.db.item.find_one_and_update({"_id": _idI}, {"$pull": {"choices": _idC}})
    current_app.db.choice.find_one_and_delete({"_id": _idC})

    return redirect(url_for(".item_detail", _id=_idI))


@pages.route("/add_choice/<string:_id>", methods=["GET", "POST"])
def add_choice(_id: str):

    item = Item(**current_app.db.item.find_one({"_id": _id}))

    form = ChoiceForm()

    if form.validate_on_submit():
        choice = Choice(
            _id=uuid.uuid4().hex,
            name=form.name.data,
            price=form.price.data,
            brand=form.brand.data,
            where=form.where.data,
            address=form.address.data
        )
        current_app.db.choice.insert_one(asdict(choice))
        current_app.db.item.update_one({"_id": item._id}, {"$push": {"choices": choice._id}})
        return redirect(url_for(".item_detail", _id=item._id))

    return render_template("items/add_choice.html", title="Shopping List - Add Choice", item=item, form=form)


