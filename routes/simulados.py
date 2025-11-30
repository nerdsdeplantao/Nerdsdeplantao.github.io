import json
from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from extensions import db
from models import Discipline, Module, Quiz, Question, QuizAttempt

simulados_bp = Blueprint('simulados', __name__)

@simulados_bp.route('/')
@login_required
def index():
    disciplines = Discipline.query.order_by(Discipline.order, Discipline.name).all()
    return render_template('simulados/index.html', disciplines=disciplines)

@simulados_bp.route('/discipline/<int:id>')
@login_required
def discipline(id):
    discipline = Discipline.query.get_or_404(id)
    modules = Module.query.filter_by(discipline_id=id).order_by(Module.order, Module.name).all()
    return render_template('simulados/discipline.html', discipline=discipline, modules=modules)

@simulados_bp.route('/module/<int:id>')
@login_required
def module(id):
    module = Module.query.get_or_404(id)
    quizzes = Quiz.query.filter_by(module_id=id).order_by(Quiz.order, Quiz.title).all()
    
    user_attempts = {}
    for quiz in quizzes:
        attempts = QuizAttempt.query.filter_by(user_id=current_user.id, quiz_id=quiz.id, completed=True).all()
        if attempts:
            best_score = max(a.score for a in attempts)
            user_attempts[quiz.id] = {'count': len(attempts), 'best_score': best_score}
    
    return render_template('simulados/module.html', module=module, quizzes=quizzes, user_attempts=user_attempts)

@simulados_bp.route('/start/<int:id>')
@login_required
def start(id):
    quiz = Quiz.query.get_or_404(id)
    questions_count = Question.query.filter_by(quiz_id=id).count()
    
    if questions_count == 0:
        flash('Este simulado ainda não possui questões.', 'warning')
        return redirect(url_for('simulados.module', id=quiz.module_id))
    
    previous_attempts = QuizAttempt.query.filter_by(user_id=current_user.id, quiz_id=id, completed=True).order_by(QuizAttempt.finished_at.desc()).limit(5).all()
    
    return render_template('simulados/start.html', quiz=quiz, questions_count=questions_count, previous_attempts=previous_attempts)

@simulados_bp.route('/take/<int:id>')
@login_required
def take(id):
    quiz = Quiz.query.get_or_404(id)
    questions = Question.query.filter_by(quiz_id=id).order_by(Question.order).all()
    
    if not questions:
        flash('Este simulado não possui questões.', 'warning')
        return redirect(url_for('simulados.start', id=id))
    
    attempt = QuizAttempt(
        user_id=current_user.id,
        quiz_id=id,
        total_questions=len(questions),
        started_at=datetime.utcnow()
    )
    db.session.add(attempt)
    db.session.commit()
    
    return render_template('simulados/take.html', quiz=quiz, questions=questions, attempt=attempt)

@simulados_bp.route('/submit/<int:attempt_id>', methods=['POST'])
@login_required
def submit(attempt_id):
    attempt = QuizAttempt.query.get_or_404(attempt_id)
    
    if attempt.user_id != current_user.id:
        flash('Acesso negado.', 'danger')
        return redirect(url_for('simulados.index'))
    
    if attempt.completed:
        flash('Este simulado já foi finalizado.', 'warning')
        return redirect(url_for('simulados.result', attempt_id=attempt_id))
    
    questions = Question.query.filter_by(quiz_id=attempt.quiz_id).order_by(Question.order).all()
    
    answers = {}
    correct_count = 0
    
    for question in questions:
        answer_key = f'question_{question.id}'
        user_answer = request.form.get(answer_key, '')
        answers[str(question.id)] = user_answer
        
        if user_answer.upper() == question.correct_answer.upper():
            correct_count += 1
    
    time_spent = request.form.get('time_spent', 0)
    
    attempt.answers = json.dumps(answers)
    attempt.correct_answers = correct_count
    attempt.score = (correct_count / len(questions)) * 100 if questions else 0
    attempt.time_spent_seconds = int(time_spent) if time_spent else 0
    attempt.completed = True
    attempt.finished_at = datetime.utcnow()
    
    db.session.commit()
    
    flash('Simulado finalizado com sucesso!', 'success')
    return redirect(url_for('simulados.result', attempt_id=attempt_id))

@simulados_bp.route('/result/<int:attempt_id>')
@login_required
def result(attempt_id):
    attempt = QuizAttempt.query.get_or_404(attempt_id)
    
    if attempt.user_id != current_user.id and not current_user.is_admin:
        flash('Acesso negado.', 'danger')
        return redirect(url_for('simulados.index'))
    
    if not attempt.completed:
        flash('Este simulado ainda não foi finalizado.', 'warning')
        return redirect(url_for('simulados.take', id=attempt.quiz_id))
    
    questions = Question.query.filter_by(quiz_id=attempt.quiz_id).order_by(Question.order).all()
    user_answers = json.loads(attempt.answers) if attempt.answers else {}
    
    return render_template('simulados/result.html', attempt=attempt, questions=questions, user_answers=user_answers)

@simulados_bp.route('/history')
@login_required
def history():
    attempts = QuizAttempt.query.filter_by(user_id=current_user.id, completed=True).order_by(QuizAttempt.finished_at.desc()).all()
    return render_template('simulados/history.html', attempts=attempts)
