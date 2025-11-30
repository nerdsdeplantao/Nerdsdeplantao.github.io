import os
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from functools import wraps
from extensions import db
from models import User, Discipline, Module, VideoLesson, Material, Quiz, Question, QuizAttempt, UserProgress
from forms import DisciplineForm, ModuleForm, VideoLessonForm, MaterialForm, QuizForm, QuestionForm, UserStatusForm

admin_bp = Blueprint('admin', __name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('Acesso negado. Você precisa ser administrador.', 'danger')
            return redirect(url_for('main.dashboard'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/')
@login_required
@admin_required
def index():
    total_users = User.query.count()
    pending_users = User.query.filter_by(is_approved=False).count()
    total_videos = VideoLesson.query.count()
    total_quizzes = Quiz.query.count()
    total_materials = Material.query.count()
    
    recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()
    
    quiz_attempts = QuizAttempt.query.filter_by(completed=True).all()
    avg_score = 0
    if quiz_attempts:
        avg_score = sum(a.score for a in quiz_attempts) / len(quiz_attempts)
    
    return render_template('admin/index.html',
                         total_users=total_users,
                         pending_users=pending_users,
                         total_videos=total_videos,
                         total_quizzes=total_quizzes,
                         total_materials=total_materials,
                         recent_users=recent_users,
                         avg_score=avg_score)

@admin_bp.route('/users')
@login_required
@admin_required
def users():
    filter_type = request.args.get('filter', 'all')
    
    if filter_type == 'pending':
        users = User.query.filter_by(is_approved=False).order_by(User.created_at.desc()).all()
    elif filter_type == 'active':
        users = User.query.filter_by(is_approved=True, is_active=True).order_by(User.created_at.desc()).all()
    elif filter_type == 'inactive':
        users = User.query.filter_by(is_active=False).order_by(User.created_at.desc()).all()
    elif filter_type == 'admins':
        users = User.query.filter_by(is_admin=True).order_by(User.created_at.desc()).all()
    else:
        users = User.query.order_by(User.created_at.desc()).all()
    
    return render_template('admin/users.html', users=users, filter_type=filter_type)

@admin_bp.route('/users/<int:user_id>/approve', methods=['POST'])
@login_required
@admin_required
def approve_user(user_id):
    user = User.query.get_or_404(user_id)
    user.is_approved = True
    db.session.commit()
    flash(f'Usuário {user.username} aprovado com sucesso!', 'success')
    return redirect(url_for('admin.users', filter='pending'))

@admin_bp.route('/users/<int:user_id>/reject', methods=['POST'])
@login_required
@admin_required
def reject_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash(f'Cadastro de {user.username} rejeitado e removido.', 'info')
    return redirect(url_for('admin.users', filter='pending'))

@admin_bp.route('/users/<int:user_id>/toggle-status', methods=['POST'])
@login_required
@admin_required
def toggle_user_status(user_id):
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash('Você não pode desativar sua própria conta.', 'danger')
        return redirect(url_for('admin.users'))
    
    user.is_active = not user.is_active
    db.session.commit()
    status = 'ativado' if user.is_active else 'desativado'
    flash(f'Usuário {user.username} {status}.', 'success')
    return redirect(url_for('admin.users'))

@admin_bp.route('/users/<int:user_id>/toggle-admin', methods=['POST'])
@login_required
@admin_required
def toggle_user_admin(user_id):
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash('Você não pode alterar seu próprio nível de acesso.', 'danger')
        return redirect(url_for('admin.users'))
    
    user.is_admin = not user.is_admin
    db.session.commit()
    status = 'promovido a administrador' if user.is_admin else 'rebaixado para usuário comum'
    flash(f'Usuário {user.username} {status}.', 'success')
    return redirect(url_for('admin.users'))

@admin_bp.route('/users/<int:user_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash('Você não pode excluir sua própria conta.', 'danger')
        return redirect(url_for('admin.users'))
    
    username = user.username
    db.session.delete(user)
    db.session.commit()
    flash(f'Usuário {username} excluído.', 'success')
    return redirect(url_for('admin.users'))

@admin_bp.route('/disciplines')
@login_required
@admin_required
def disciplines():
    disciplines = Discipline.query.order_by(Discipline.order, Discipline.name).all()
    return render_template('admin/disciplines.html', disciplines=disciplines)

@admin_bp.route('/disciplines/new', methods=['GET', 'POST'])
@login_required
@admin_required
def new_discipline():
    form = DisciplineForm()
    if form.validate_on_submit():
        discipline = Discipline(
            name=form.name.data,
            description=form.description.data,
            order=form.order.data or 0
        )
        db.session.add(discipline)
        db.session.commit()
        flash('Disciplina criada com sucesso!', 'success')
        return redirect(url_for('admin.disciplines'))
    return render_template('admin/discipline_form.html', form=form, title='Nova Disciplina')

@admin_bp.route('/disciplines/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_discipline(id):
    discipline = Discipline.query.get_or_404(id)
    form = DisciplineForm(obj=discipline)
    if form.validate_on_submit():
        discipline.name = form.name.data
        discipline.description = form.description.data
        discipline.order = form.order.data or 0
        db.session.commit()
        flash('Disciplina atualizada com sucesso!', 'success')
        return redirect(url_for('admin.disciplines'))
    return render_template('admin/discipline_form.html', form=form, title='Editar Disciplina')

@admin_bp.route('/disciplines/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_discipline(id):
    discipline = Discipline.query.get_or_404(id)
    db.session.delete(discipline)
    db.session.commit()
    flash('Disciplina excluída com sucesso!', 'success')
    return redirect(url_for('admin.disciplines'))

@admin_bp.route('/modules')
@login_required
@admin_required
def modules():
    modules = Module.query.join(Discipline).order_by(Discipline.order, Module.order, Module.name).all()
    return render_template('admin/modules.html', modules=modules)

@admin_bp.route('/modules/new', methods=['GET', 'POST'])
@login_required
@admin_required
def new_module():
    form = ModuleForm()
    form.discipline_id.choices = [(d.id, d.name) for d in Discipline.query.order_by(Discipline.order, Discipline.name).all()]
    
    if form.validate_on_submit():
        module = Module(
            name=form.name.data,
            description=form.description.data,
            discipline_id=form.discipline_id.data,
            order=form.order.data or 0
        )
        db.session.add(module)
        db.session.commit()
        flash('Módulo criado com sucesso!', 'success')
        return redirect(url_for('admin.modules'))
    return render_template('admin/module_form.html', form=form, title='Novo Módulo')

@admin_bp.route('/modules/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_module(id):
    module = Module.query.get_or_404(id)
    form = ModuleForm(obj=module)
    form.discipline_id.choices = [(d.id, d.name) for d in Discipline.query.order_by(Discipline.order, Discipline.name).all()]
    
    if form.validate_on_submit():
        module.name = form.name.data
        module.description = form.description.data
        module.discipline_id = form.discipline_id.data
        module.order = form.order.data or 0
        db.session.commit()
        flash('Módulo atualizado com sucesso!', 'success')
        return redirect(url_for('admin.modules'))
    return render_template('admin/module_form.html', form=form, title='Editar Módulo')

@admin_bp.route('/modules/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_module(id):
    module = Module.query.get_or_404(id)
    db.session.delete(module)
    db.session.commit()
    flash('Módulo excluído com sucesso!', 'success')
    return redirect(url_for('admin.modules'))

@admin_bp.route('/videos')
@login_required
@admin_required
def videos():
    videos = VideoLesson.query.join(Module).join(Discipline).order_by(
        Discipline.order, Module.order, VideoLesson.order, VideoLesson.title
    ).all()
    return render_template('admin/videos.html', videos=videos)

@admin_bp.route('/videos/new', methods=['GET', 'POST'])
@login_required
@admin_required
def new_video():
    form = VideoLessonForm()
    form.module_id.choices = [(m.id, f'{m.discipline.name} - {m.name}') for m in Module.query.join(Discipline).order_by(Discipline.order, Module.order).all()]
    
    if form.validate_on_submit():
        video = VideoLesson(
            title=form.title.data,
            description=form.description.data,
            video_url=form.video_url.data,
            video_type=form.video_type.data,
            duration_minutes=form.duration_minutes.data,
            module_id=form.module_id.data,
            order=form.order.data or 0
        )
        db.session.add(video)
        db.session.commit()
        flash('Videoaula criada com sucesso!', 'success')
        return redirect(url_for('admin.videos'))
    return render_template('admin/video_form.html', form=form, title='Nova Videoaula')

@admin_bp.route('/videos/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_video(id):
    video = VideoLesson.query.get_or_404(id)
    form = VideoLessonForm(obj=video)
    form.module_id.choices = [(m.id, f'{m.discipline.name} - {m.name}') for m in Module.query.join(Discipline).order_by(Discipline.order, Module.order).all()]
    
    if form.validate_on_submit():
        video.title = form.title.data
        video.description = form.description.data
        video.video_url = form.video_url.data
        video.video_type = form.video_type.data
        video.duration_minutes = form.duration_minutes.data
        video.module_id = form.module_id.data
        video.order = form.order.data or 0
        db.session.commit()
        flash('Videoaula atualizada com sucesso!', 'success')
        return redirect(url_for('admin.videos'))
    return render_template('admin/video_form.html', form=form, title='Editar Videoaula')

@admin_bp.route('/videos/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_video(id):
    video = VideoLesson.query.get_or_404(id)
    db.session.delete(video)
    db.session.commit()
    flash('Videoaula excluída com sucesso!', 'success')
    return redirect(url_for('admin.videos'))

@admin_bp.route('/materials')
@login_required
@admin_required
def materials():
    materials = Material.query.join(Module).join(Discipline).order_by(
        Discipline.order, Module.order, Material.order, Material.title
    ).all()
    return render_template('admin/materials.html', materials=materials)

@admin_bp.route('/materials/new', methods=['GET', 'POST'])
@login_required
@admin_required
def new_material():
    form = MaterialForm()
    form.module_id.choices = [(m.id, f'{m.discipline.name} - {m.name}') for m in Module.query.join(Discipline).order_by(Discipline.order, Module.order).all()]
    
    if form.validate_on_submit():
        file_path = None
        file_type = None
        
        if form.file.data:
            file = form.file.data
            filename = secure_filename(file.filename)
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            file_type = filename.rsplit('.', 1)[1].lower() if '.' in filename else None
            file_path = filename
        
        material = Material(
            title=form.title.data,
            description=form.description.data,
            file_path=file_path,
            file_type=file_type,
            external_url=form.external_url.data,
            module_id=form.module_id.data,
            order=form.order.data or 0
        )
        db.session.add(material)
        db.session.commit()
        flash('Material criado com sucesso!', 'success')
        return redirect(url_for('admin.materials'))
    return render_template('admin/material_form.html', form=form, title='Novo Material')

@admin_bp.route('/materials/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_material(id):
    material = Material.query.get_or_404(id)
    form = MaterialForm(obj=material)
    form.module_id.choices = [(m.id, f'{m.discipline.name} - {m.name}') for m in Module.query.join(Discipline).order_by(Discipline.order, Module.order).all()]
    
    if form.validate_on_submit():
        if form.file.data:
            file = form.file.data
            filename = secure_filename(file.filename)
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            material.file_path = filename
            material.file_type = filename.rsplit('.', 1)[1].lower() if '.' in filename else None
        
        material.title = form.title.data
        material.description = form.description.data
        material.external_url = form.external_url.data
        material.module_id = form.module_id.data
        material.order = form.order.data or 0
        db.session.commit()
        flash('Material atualizado com sucesso!', 'success')
        return redirect(url_for('admin.materials'))
    return render_template('admin/material_form.html', form=form, title='Editar Material')

@admin_bp.route('/materials/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_material(id):
    material = Material.query.get_or_404(id)
    if material.file_path:
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], material.file_path)
        if os.path.exists(file_path):
            os.remove(file_path)
    db.session.delete(material)
    db.session.commit()
    flash('Material excluído com sucesso!', 'success')
    return redirect(url_for('admin.materials'))

@admin_bp.route('/quizzes')
@login_required
@admin_required
def quizzes():
    quizzes = Quiz.query.join(Module).join(Discipline).order_by(
        Discipline.order, Module.order, Quiz.order, Quiz.title
    ).all()
    return render_template('admin/quizzes.html', quizzes=quizzes)

@admin_bp.route('/quizzes/new', methods=['GET', 'POST'])
@login_required
@admin_required
def new_quiz():
    form = QuizForm()
    form.module_id.choices = [(m.id, f'{m.discipline.name} - {m.name}') for m in Module.query.join(Discipline).order_by(Discipline.order, Module.order).all()]
    
    if form.validate_on_submit():
        quiz = Quiz(
            title=form.title.data,
            description=form.description.data,
            time_limit_minutes=form.time_limit_minutes.data,
            module_id=form.module_id.data,
            order=form.order.data or 0
        )
        db.session.add(quiz)
        db.session.commit()
        flash('Simulado criado com sucesso! Agora adicione as questões.', 'success')
        return redirect(url_for('admin.quiz_questions', id=quiz.id))
    return render_template('admin/quiz_form.html', form=form, title='Novo Simulado')

@admin_bp.route('/quizzes/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_quiz(id):
    quiz = Quiz.query.get_or_404(id)
    form = QuizForm(obj=quiz)
    form.module_id.choices = [(m.id, f'{m.discipline.name} - {m.name}') for m in Module.query.join(Discipline).order_by(Discipline.order, Module.order).all()]
    
    if form.validate_on_submit():
        quiz.title = form.title.data
        quiz.description = form.description.data
        quiz.time_limit_minutes = form.time_limit_minutes.data
        quiz.module_id = form.module_id.data
        quiz.order = form.order.data or 0
        db.session.commit()
        flash('Simulado atualizado com sucesso!', 'success')
        return redirect(url_for('admin.quizzes'))
    return render_template('admin/quiz_form.html', form=form, title='Editar Simulado', quiz=quiz)

@admin_bp.route('/quizzes/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_quiz(id):
    quiz = Quiz.query.get_or_404(id)
    db.session.delete(quiz)
    db.session.commit()
    flash('Simulado excluído com sucesso!', 'success')
    return redirect(url_for('admin.quizzes'))

@admin_bp.route('/quizzes/<int:id>/questions')
@login_required
@admin_required
def quiz_questions(id):
    quiz = Quiz.query.get_or_404(id)
    questions = Question.query.filter_by(quiz_id=id).order_by(Question.order).all()
    return render_template('admin/quiz_questions.html', quiz=quiz, questions=questions)

@admin_bp.route('/quizzes/<int:quiz_id>/questions/new', methods=['GET', 'POST'])
@login_required
@admin_required
def new_question(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    form = QuestionForm()
    
    if form.validate_on_submit():
        question = Question(
            quiz_id=quiz_id,
            text=form.text.data,
            option_a=form.option_a.data,
            option_b=form.option_b.data,
            option_c=form.option_c.data,
            option_d=form.option_d.data,
            option_e=form.option_e.data,
            correct_answer=form.correct_answer.data,
            explanation=form.explanation.data,
            order=form.order.data or 0
        )
        db.session.add(question)
        db.session.commit()
        flash('Questão adicionada com sucesso!', 'success')
        return redirect(url_for('admin.quiz_questions', id=quiz_id))
    return render_template('admin/question_form.html', form=form, quiz=quiz, title='Nova Questão')

@admin_bp.route('/questions/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_question(id):
    question = Question.query.get_or_404(id)
    form = QuestionForm(obj=question)
    
    if form.validate_on_submit():
        question.text = form.text.data
        question.option_a = form.option_a.data
        question.option_b = form.option_b.data
        question.option_c = form.option_c.data
        question.option_d = form.option_d.data
        question.option_e = form.option_e.data
        question.correct_answer = form.correct_answer.data
        question.explanation = form.explanation.data
        question.order = form.order.data or 0
        db.session.commit()
        flash('Questão atualizada com sucesso!', 'success')
        return redirect(url_for('admin.quiz_questions', id=question.quiz_id))
    return render_template('admin/question_form.html', form=form, quiz=question.quiz, title='Editar Questão')

@admin_bp.route('/questions/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_question(id):
    question = Question.query.get_or_404(id)
    quiz_id = question.quiz_id
    db.session.delete(question)
    db.session.commit()
    flash('Questão excluída com sucesso!', 'success')
    return redirect(url_for('admin.quiz_questions', id=quiz_id))
