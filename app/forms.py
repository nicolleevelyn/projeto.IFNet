from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional, NumberRange


class LoginForm(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField("Senha", validators=[DataRequired()])
    submit = SubmitField("Entrar")


class RegisterForm(FlaskForm):
    name = StringField("Nome completo", validators=[DataRequired(), Length(min=3, max=120)])
    email = StringField("E-mail", validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField("Senha", validators=[DataRequired(), Length(min=6, max=128)])
    confirm_password = PasswordField("Confirmar senha", validators=[DataRequired(), EqualTo("password", message="As senhas precisam ser iguais.")])
    submit = SubmitField("Criar conta")


class MaterialForm(FlaskForm):
    title = StringField(
        "Título",
        validators=[DataRequired(), Length(max=160)]
    )

    description = StringField(
        "Descrição",
        validators=[Optional(), Length(max=300)]
    )

    material_type = SelectField(
        "Tipo",
        choices=[
            ("content", "Conteúdo"),
            ("video", "Vídeo"),
            ("exercise", "Exercício")
        ],
        validators=[DataRequired()]
    )

    order_index = IntegerField(
        "Ordem de exibição",
        validators=[
            DataRequired(),
            NumberRange(
                min=1,
                message="A ordem deve ser 1 ou maior."
            )
        ],
        default=1
    )

    body = TextAreaField(
        "Material / texto",
        validators=[Optional()]
    )

    video_url = StringField(
        "Link do vídeo, kahoot e afins (se o tipo do material for video, adicione aqui)",
        validators=[Optional(), Length(max=500)]
    )

    submit = SubmitField("Salvar material")
