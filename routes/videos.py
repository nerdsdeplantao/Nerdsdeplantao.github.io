import re
from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, jsonify, request
from flask_login import login_required, current_user
from extensions import db
from models import Discipline, Module, VideoLesson, UserProgress

videos_bp = Blueprint('videos', __name__)

def get_embed_url(url, video_type):
    if video_type == 'youtube':
        youtube_regex = r'(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^"&?\/\s]{11})'
        match = re.search(youtube_regex, url)
        if match:
            video_id = match.group(1)
            return f'https://www.youtube.com/embed/{video_id}?rel=0&modestbranding=1'
    elif video_type == 'vimeo':
        vimeo_regex = r'vimeo\.com\/(?:.*\/)?(\d+)'
        match = re.search(vimeo_regex, url)
        if match:
            video_id = match.group(1)
            return f'https://player.vimeo.com/video/{video_id}?dnt=1'
    return url

@videos_bp.route('/')
@login_required
def index():
    disciplines = Discipline.query.order_by(Discipline.order, Discipline.name).all()
    return render_template('videos/index.html', disciplines=disciplines)

@videos_bp.route('/discipline/<int:id>')
@login_required
def discipline(id):
    discipline = Discipline.query.get_or_404(id)
    modules = Module.query.filter_by(discipline_id=id).order_by(Module.order, Module.name).all()
    return render_template('videos/discipline.html', discipline=discipline, modules=modules)

@videos_bp.route('/module/<int:id>')
@login_required
def module(id):
    module = Module.query.get_or_404(id)
    videos = VideoLesson.query.filter_by(module_id=id).order_by(VideoLesson.order, VideoLesson.title).all()
    
    user_progress = {p.video_id: p.completed for p in UserProgress.query.filter_by(user_id=current_user.id).all()}
    
    return render_template('videos/module.html', module=module, videos=videos, user_progress=user_progress)

@videos_bp.route('/watch/<int:id>')
@login_required
def watch(id):
    video = VideoLesson.query.get_or_404(id)
    embed_url = get_embed_url(video.video_url, video.video_type)
    
    progress = UserProgress.query.filter_by(user_id=current_user.id, video_id=id).first()
    is_completed = progress.completed if progress else False
    
    next_video = VideoLesson.query.filter(
        VideoLesson.module_id == video.module_id,
        VideoLesson.order > video.order
    ).order_by(VideoLesson.order).first()
    
    prev_video = VideoLesson.query.filter(
        VideoLesson.module_id == video.module_id,
        VideoLesson.order < video.order
    ).order_by(VideoLesson.order.desc()).first()
    
    return render_template('videos/watch.html', 
                         video=video, 
                         embed_url=embed_url, 
                         is_completed=is_completed,
                         next_video=next_video,
                         prev_video=prev_video)

@videos_bp.route('/mark-complete/<int:id>', methods=['POST'])
@login_required
def mark_complete(id):
    video = VideoLesson.query.get_or_404(id)
    
    progress = UserProgress.query.filter_by(user_id=current_user.id, video_id=id).first()
    
    if not progress:
        progress = UserProgress(user_id=current_user.id, video_id=id, completed=True, completed_at=datetime.utcnow())
        db.session.add(progress)
    else:
        progress.completed = not progress.completed
        progress.completed_at = datetime.utcnow() if progress.completed else None
    
    db.session.commit()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({'success': True, 'completed': progress.completed})
    
    flash('Progresso atualizado!', 'success')
    return redirect(url_for('videos.watch', id=id))
