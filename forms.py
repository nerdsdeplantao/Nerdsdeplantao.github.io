from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, TextAreaField, IntegerField, SelectField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional, ValidationError, NumberRange

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired()])
    remember = BooleanField('Lembrar-me')
    submit = SubmitField('Entrar')

class RegisterForm(FlaskForm):
    username = StringField('Nome de Usuário', validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirmar Senha', validators=[DataRequired(), EqualTo('password', message='As senhas devem ser iguais')])
    submit = SubmitField('Cadastrar')

class DisciplineForm(FlaskForm):
    name = StringField('Nome da Disciplina', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Descrição', validators=[Optional()])
    order = IntegerField('Ordem', validators=[Optional()], default=0)
    submit = SubmitField('Salvar')

class ModuleForm(FlaskForm):
    name = StringField('Nome do Módulo', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Descrição', validators=[Optional()])
    discipline_id = SelectField('Disciplina', coerce=int, validators=[DataRequired()])
    order = IntegerField('Ordem', validators=[Optional()], default=0)
    submit = SubmitField('Salvar')

class VideoLessonForm(FlaskForm):
    title = StringField('Título', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('Descrição', validators=[Optional()])
    video_url = StringField('URL do Vídeo (YouTube ou Vimeo)', validators=[DataRequired(), Length(max=500)])
    video_type = SelectField('Tipo de Vídeo', choices=[('youtube', 'YouTube'), ('vimeo', 'Vimeo')], default='youtube')
    duration_minutes = IntegerField('Duração (minutos)', validators=[Optional(), NumberRange(min=1)])
    module_id = SelectField('Módulo', coerce=int, validators=[DataRequired()])
    order = IntegerField('Ordem', validators=[Optional()], default=0)
    submit = SubmitField('Salvar')

class MaterialForm(FlaskForm):
    title = StringField('Título', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('Descrição', validators=[Optional()])
    file = FileField('Arquivo (PDF, DOC, etc)', validators=[FileAllowed(['pdf', 'doc', 'docx', 'ppt', 'pptx', 'xls', 'xlsx'], 'Apenas documentos são permitidos!')])
    external_url = StringField('URL Externa (opcional)', validators=[Optional(), Length(max=500)])
    module_id = SelectField('Módulo', coerce=int, validators=[DataRequired()])
    order = IntegerField('Ordem', validators=[Optional()], default=0)
    submit = SubmitField('Salvar')

class QuizForm(FlaskForm):
    title = StringField('Título do Simulado', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('Descrição', validators=[Optional()])
    time_limit_minutes = IntegerField('Tempo Limite (minutos)', validators=[DataRequired(), NumberRange(min=1, max=300)], default=60)
    module_id = SelectField('Módulo', coerce=int, validators=[DataRequired()])
    order = IntegerField('Ordem', validators=[Optional()], default=0)
    submit = SubmitField('Salvar')

class QuestionForm(FlaskForm):
    text = TextAreaField('Enunciado da Questão', validators=[DataRequired()])
    option_a = StringField('Alternativa A', validators=[DataRequired(), Length(max=500)])
    option_b = StringField('Alternativa B', validators=[DataRequired(), Length(max=500)])
    option_c = StringField('Alternativa C', validators=[DataRequired(), Length(max=500)])
    option_d = StringField('Alternativa D', validators=[DataRequired(), Length(max=500)])
    option_e = StringField('Alternativa E (opcional)', validators=[Optional(), Length(max=500)])
    correct_answer = SelectField('Resposta Correta', choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('E', 'E')], validators=[DataRequired()])
    explanation = TextAreaField('Justificativa da Resposta', validators=[Optional()])
    order = IntegerField('Ordem', validators=[Optional()], default=0)
    submit = SubmitField('Salvar')

class SearchForm(FlaskForm):
    query = StringField('Buscar', validators=[DataRequired(), Length(min=2, max=100)])
    submit = SubmitField('Buscar')

class UserStatusForm(FlaskForm):
    is_approved = BooleanField('Aprovado')
    is_active = BooleanField('Ativo')
    is_admin = BooleanField('Administrador')
    submit = SubmitField('Atualizar')
