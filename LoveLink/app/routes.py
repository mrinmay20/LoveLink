from flask import Blueprint, render_template, request, redirect, url_for, current_app
from datetime import datetime, timedelta
from .models import LovePage
from . import db
import os
from werkzeug.utils import secure_filename

main = Blueprint("main", __name__)


# ===============================
# HOME PAGE
# ===============================
@main.route("/", methods=["GET", "POST"])
def index():

    if request.method == "POST":

        # ✅ Get form data
        your_name = request.form.get("your_name")
        partner_name = request.form.get("partner_name")
        message = request.form.get("message")
        theme = request.form.get("theme")
        music = request.form.get("music")
        plan = request.form.get("plan")
        password = request.form.get("password")
        expiry_input = request.form.get("expiry_date")

        # ✅ Payment Logic
        payment_done = request.form.get("payment_done")

        if plan == "premium" and payment_done == "yes":
          payment_status = "paid"
        elif plan == "premium":
          payment_status = "pending"
        else:
          payment_status = "free"


        # ✅ Expiry logic
        if plan == "free":
            expiry = datetime.utcnow() + timedelta(days=7)
        else:
            expiry = datetime.utcnow() + timedelta(days=365)

        # Custom expiry override
        if expiry_input:
            expiry = datetime.strptime(expiry_input, "%Y-%m-%d")

        # ==========================
        # PREMIUM FILE UPLOAD
        # ==========================
        upload_folder = current_app.config["UPLOAD_FOLDER"]

        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)

        custom_music_file = request.files.get("custom_music")
        video_file = request.files.get("video_file")

        music_filename = None
        video_filename = None

        if custom_music_file and custom_music_file.filename != "":
            music_filename = secure_filename(custom_music_file.filename)
            custom_music_file.save(os.path.join(upload_folder, music_filename))

        if video_file and video_file.filename != "":
            video_filename = secure_filename(video_file.filename)
            video_file.save(os.path.join(upload_folder, video_filename))

        # ✅ Create new page
        new_page = LovePage(
            your_name=your_name,
            partner_name=partner_name,
            message=message,
            theme=theme,
            music=music,
            plan=plan,
            password=password,
            expiry_date=expiry,
            payment_status=payment_status,
            custom_music=music_filename,
            video_file=video_filename
        )

        db.session.add(new_page)
        db.session.commit()

        # ==========================
        # BASIC PHOTO UPLOAD
        # ==========================
        your_photo = request.files.get("your_photo")
        partner_photo = request.files.get("partner_photo")

        if your_photo and your_photo.filename != "":
            your_filename = f"{new_page.id}_1.jpg"
            your_photo.save(os.path.join(upload_folder, your_filename))
            new_page.your_photo = "uploads/" + your_filename

        if partner_photo and partner_photo.filename != "":
            partner_filename = f"{new_page.id}_2.jpg"
            partner_photo.save(os.path.join(upload_folder, partner_filename))
            new_page.partner_photo = "uploads/" + partner_filename

        db.session.commit()

        return redirect(url_for("main.love_page", id=new_page.id))

    return render_template("index.html")


# ===============================
# LOVE PAGE
# ===============================
@main.route("/love/<id>")
def love_page(id):

    page = LovePage.query.get_or_404(id)

    # ✅ Expiry check
    if page.expiry_date and datetime.utcnow() > page.expiry_date:
        return "This love page has expired 💔"

    # ✅ Increase views
    page.views += 1
    db.session.commit()

    return render_template("love.html", page=page)


# ===============================
# PAYMENT SUCCESS (SIMULATION)
# ===============================
@main.route("/payment/success/<string:id>")
def payment_success(id):
    page = LovePage.query.get_or_404(id)

    # Activate premium
    page.payment_status = "paid"
    db.session.commit()

    return redirect(url_for("main.love_page", id=id))
