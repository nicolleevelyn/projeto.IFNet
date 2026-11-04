from urllib.parse import urlparse
from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, login_user, logout_user, current_user
from app.extensions import db
from app.forms import LoginForm, RegisterForm, MaterialForm
from app.models import User, Material

main = Blueprint("main", __name__)


def admin_required():
    if not current_user.is_authenticated or not current_user.is_admin:
        abort(403)


def safe_next_url(value):
    if value and value.startswith("/") and not value.startswith("//"):
        return value
    return url_for("main.dashboard")


@main.route("/")
@main.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", material_count=Material.query.count())


@main.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.strip().lower()).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash("Login realizado com sucesso!", "success")
            return redirect(safe_next_url(request.args.get("next")))
        flash("E-mail ou senha incorretos.", "danger")
    return render_template("auth/login.html", form=form)


@main.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))
    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data.strip().lower()
        if User.query.filter_by(email=email).first():
            flash("Este e-mail já está cadastrado.", "warning")
        else:
            # A primeira conta criada será a conta do professor/administrador.
            role = "admin" if User.query.count() == 0 else "student"
            user = User(name=form.name.data.strip(), email=email, role=role)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            if role == "admin":
                flash("Conta criada como administrador. Use-a para administrar o site.", "success")
            else:
                flash("Conta criada. Agora você pode entrar.", "success")
            return redirect(url_for("main.login"))
    return render_template("auth/register.html", form=form)


@main.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    flash("Você saiu da sua conta.", "info")
    return redirect(url_for("main.login"))

@main.route("/conteudos")
@login_required
def conteudos():
    materials = (
        Material.query
        .filter_by(material_type="content")
        .order_by(Material.order_index, Material.id)
        .all()
    )

    return render_template(
        "materiais.html",
        materials=materials,
        page_title="Conteúdos",
        page_type="content"
    )


@main.route("/videos")
@login_required
def videos():
    materials = (
        Material.query
        .filter_by(material_type="video")
        .order_by(Material.order_index, Material.id)
        .all()
    )

    return render_template(
        "materiais.html",
        materials=materials,
        page_title="Vídeos",
        page_type="video"
    )


@main.route("/exercicios")
@login_required
def exercicios():
    materials = (
        Material.query
        .filter_by(material_type="exercise")
        .order_by(Material.order_index, Material.id)
        .all()
    )

    return render_template(
        "materiais.html",
        materials=materials,
        page_title="Exercícios",
        page_type="exercise"
    )




@main.route("/estudar/<int:material_id>")
@login_required
def estudar(material_id):
    material = db.get_or_404(Material, material_id)
    return render_template("estudar.html", material=material)

@main.route("/admin/materiais")
@login_required
def admin_materials():
    admin_required()

    materials = (
        Material.query
        .order_by(
            Material.material_type,
            Material.order_index,
            Material.id
        )
        .all()
    )

    return render_template(
        "admin/materials.html",
        materials=materials
    )


@main.route("/admin/materiais/novo", methods=["GET", "POST"])
@login_required
def new_material():
    admin_required()
    form = MaterialForm()
    if form.validate_on_submit():
        material = Material(
            title=form.title.data.strip(),
            description=(form.description.data or "").strip(),
            material_type=form.material_type.data,
            order_index=form.order_index.data,
            body=form.body.data or "",
            video_url=(form.video_url.data or "").strip() or None,
        )
        if material.video_url and urlparse(material.video_url).scheme not in ("http", "https"):
            flash("O link do vídeo deve começar com http:// ou https://.", "danger")
        else:
            db.session.add(material)
            db.session.commit()
            flash("Material adicionado com sucesso.", "success")
            return redirect(url_for("main.admin_materials"))
    return render_template("admin/material_form.html", form=form, page_title="Adicionar material")


@main.route("/admin/materiais/<int:material_id>/editar", methods=["GET", "POST"])
@login_required
def edit_material(material_id):
    admin_required()
    material = db.get_or_404(Material, material_id)
    form = MaterialForm(obj=material)
    if form.validate_on_submit():
        
        video_url = (form.video_url.data or "").strip() or None
        if video_url and urlparse(video_url).scheme not in ("http", "https"):
            flash("O link do vídeo deve começar com http:// ou https://.", "danger")
        else:
            material.title = form.title.data.strip()
            material.description = (form.description.data or "").strip()
            material.material_type = form.material_type.data
            material.order_index = form.order_index.data
            material.body = form.body.data or ""
            material.video_url = video_url
            db.session.commit()
            flash("Material atualizado com sucesso.", "success")
            return redirect(url_for("main.admin_materials"))
    return render_template("admin/material_form.html", form=form, page_title="Editar material")


@main.route("/admin/materiais/<int:material_id>/excluir", methods=["POST"])
@login_required
def delete_material(material_id):
    admin_required()
    material = db.get_or_404(Material, material_id)
    db.session.delete(material)
    db.session.commit()
    flash("Material excluído.", "success")
    return redirect(url_for("main.admin_materials"))


@main.route("/admin/usuarios")
@login_required
def admin_users():
    admin_required()
    users = User.query.order_by(User.name).all()
    return render_template("admin/users.html", users=users)


@main.route("/admin/usuarios/<int:user_id>/perfil", methods=["POST"])
@login_required
def change_role(user_id):
    admin_required()
    user = db.get_or_404(User, user_id)
    role = request.form.get("role")
    if role not in ("admin", "student"):
        abort(400)
    if user.id == current_user.id and role != "admin":
        flash("Você não pode remover seu próprio acesso de administrador.", "warning")
    else:
        user.role = role
        db.session.commit()
        flash("Perfil atualizado.", "success")
    return redirect(url_for("main.admin_users"))


@main.errorhandler(403)
def forbidden(error):
    return render_template("errors/403.html"), 403
