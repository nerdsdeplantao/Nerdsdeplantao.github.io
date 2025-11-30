from datetime import datetime
from flask_login import UserMixin
from extensions import db

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_approved = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    progress = db.relationship('UserProgress', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    quiz_attempts = db.relationship('QuizAttempt', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    
    def get_progress_percentage(self):
        total_videos = VideoLesson.query.count()
        if total_videos == 0:
            return 0
        completed = UserProgress.query.filter_by(user_id=self.id, completed=True).count()
        return int((completed / total_videos) * 100)

class Discipline(db.Model):
    __tablename__ = 'disciplines'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    modules = db.relationship('Module', backref='discipline', lazy='dynamic', cascade='all, delete-orphan', order_by='Module.order')

class Module(db.Model):
    __tablename__ = 'modules'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    discipline_id = db.Column(db.Integer, db.ForeignKey('disciplines.id'), nullable=False)
    order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    videos = db.relationship('VideoLesson', backref='module', lazy='dynamic', cascade='all, delete-orphan', order_by='VideoLesson.order')
    materials = db.relationship('Material', backref='module', lazy='dynamic', cascade='all, delete-orphan', order_by='Material.order')
    quizzes = db.relationship('Quiz', backref='module', lazy='dynamic', cascade='all, delete-orphan', order_by='Quiz.order')

class VideoLesson(db.Model):
    __tablename__ = 'video_lessons'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    video_url = db.Column(db.String(500), nullable=False)
    video_type = db.Column(db.String(20), default='youtube')
    duration_minutes = db.Column(db.Integer)
    module_id = db.Column(db.Integer, db.ForeignKey('modules.id'), nullable=False)
    order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user_progress = db.relationship('UserProgress', backref='video', lazy='dynamic', cascade='all, delete-orphan')

class UserProgress(db.Model):
    __tablename__ = 'user_progress'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    video_id = db.Column(db.Integer, db.ForeignKey('video_lessons.id'), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    completed_at = db.Column(db.DateTime)
    
    __table_args__ = (db.UniqueConstraint('user_id', 'video_id', name='unique_user_video'),)

class Material(db.Model):
    __tablename__ = 'materials'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    file_path = db.Column(db.String(500))
    file_type = db.Column(db.String(50))
    external_url = db.Column(db.String(500))
    module_id = db.Column(db.Integer, db.ForeignKey('modules.id'), nullable=False)
    order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Quiz(db.Model):
    __tablename__ = 'quizzes'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    time_limit_minutes = db.Column(db.Integer, default=60)
    module_id = db.Column(db.Integer, db.ForeignKey('modules.id'), nullable=False)
    order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    questions = db.relationship('Question', backref='quiz', lazy='dynamic', cascade='all, delete-orphan', order_by='Question.order')
    attempts = db.relationship('QuizAttempt', backref='quiz', lazy='dynamic', cascade='all, delete-orphan')

class Question(db.Model):
    __tablename__ = 'questions'
    
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'), nullable=False)
    text = db.Column(db.Text, nullable=False)
    option_a = db.Column(db.String(500), nullable=False)
    option_b = db.Column(db.String(500), nullable=False)
    option_c = db.Column(db.String(500), nullable=False)
    option_d = db.Column(db.String(500), nullable=False)
    option_e = db.Column(db.String(500))
    correct_answer = db.Column(db.String(1), nullable=False)
    explanation = db.Column(db.Text)
    order = db.Column(db.Integer, default=0)

class QuizAttempt(db.Model):
    __tablename__ = 'quiz_attempts'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'), nullable=False)
    score = db.Column(db.Float, default=0)
    total_questions = db.Column(db.Integer, default=0)
    correct_answers = db.Column(db.Integer, default=0)
    time_spent_seconds = db.Column(db.Integer)
    completed = db.Column(db.Boolean, default=False)
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    finished_at = db.Column(db.DateTime)
    answers = db.Column(db.Text)
