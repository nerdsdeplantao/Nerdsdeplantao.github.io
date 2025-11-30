from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db
from models import User
from forms import LoginForm, RegisterForm

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        
        if user and check_password_hash(user.password_hash, form.password.data):
            if not user.is_approved:
                flash('Sua conta ainda está aguardando aprovação do administrador.', 'warning')
                return render_template('auth/login.html', form=form)
            
            if not user.is_active:
                flash('Sua conta está desativada. Entre em contato com o administrador.', 'danger')
                return render_template('auth/login.html', form=form)
            
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash('Login realizado com sucesso!', 'success')
            return redirect(next_page if next_page else url_for('main.dashboard'))
        else:
            flash('Email ou senha incorretos.', 'danger')
    
    return render_template('auth/login.html', form=form)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.query.filter(
            (User.email == form.email.data) | (User.username == form.username.data)
        ).first()
        
        if existing_user:
            if existing_user.email == form.email.data:
                flash('Este email já está cadastrado.', 'danger')
            else:
                flash('Este nome de usuário já está em uso.', 'danger')
            return render_template('auth/register.html', form=form)
        
        user = User(
            username=form.username.data,
            email=form.email.data,
            password_hash=generate_password_hash(form.password.data),
            is_approved=False,
            is_active=True
        )
        
        db.session.add(user)
        db.session.commit()
        
        flash('Cadastro realizado com sucesso! Aguarde a aprovação do administrador para acessar a plataforma.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você saiu da plataforma.', 'info')
    return redirect(url_for('auth.login'))
