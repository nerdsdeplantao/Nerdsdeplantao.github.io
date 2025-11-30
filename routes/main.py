from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from models import VideoLesson, Quiz, Material, Discipline, Module, UserProgress, QuizAttempt
from forms import SearchForm
from sqlalchemy import or_

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return redirect(url_for('auth.login'))

@main_bp.route('/dashboard')
@login_required
def dashboard():
    total_videos = VideoLesson.query.count()
    total_quizzes = Quiz.query.count()
    total_materials = Material.query.count()
    
    recent_videos = VideoLesson.query.order_by(VideoLesson.created_at.desc()).limit(5).all()
    recent_quizzes = Quiz.query.order_by(Quiz.created_at.desc()).limit(5).all()
    recent_materials = Material.query.order_by(Material.created_at.desc()).limit(5).all()
    
    progress = current_user.get_progress_percentage()
    
    quiz_attempts = QuizAttempt.query.filter_by(user_id=current_user.id, completed=True).all()
    avg_score = 0
    if quiz_attempts:
        avg_score = sum(a.score for a in quiz_attempts) / len(quiz_attempts)
    
    return render_template('dashboard.html',
                         total_videos=total_videos,
                         total_quizzes=total_quizzes,
                         total_materials=total_materials,
                         recent_videos=recent_videos,
                         recent_quizzes=recent_quizzes,
                         recent_materials=recent_materials,
                         progress=progress,
                         avg_score=avg_score)

@main_bp.route('/search')
@login_required
def search():
    query = request.args.get('q', '')
    
    if len(query) < 2:
        return render_template('search_results.html', query=query, results=[], message='Digite pelo menos 2 caracteres para buscar.')
    
    search_term = f'%{query}%'
    
    videos = VideoLesson.query.filter(
        or_(VideoLesson.title.ilike(search_term), VideoLesson.description.ilike(search_term))
    ).all()
    
    quizzes = Quiz.query.filter(
        or_(Quiz.title.ilike(search_term), Quiz.description.ilike(search_term))
    ).all()
    
    materials = Material.query.filter(
        or_(Material.title.ilike(search_term), Material.description.ilike(search_term))
    ).all()
    
    disciplines = Discipline.query.filter(
        or_(Discipline.name.ilike(search_term), Discipline.description.ilike(search_term))
    ).all()
    
    modules = Module.query.filter(
        or_(Module.name.ilike(search_term), Module.description.ilike(search_term))
    ).all()
    
    results = {
        'videos': videos,
        'quizzes': quizzes,
        'materials': materials,
        'disciplines': disciplines,
        'modules': modules
    }
    
    return render_template('search_results.html', query=query, results=results)

from flask import redirect, url_for
