import os
from flask import Blueprint, render_template, redirect, url_for, flash, send_from_directory, current_app
from flask_login import login_required, current_user
from models import Discipline, Module, Material

materiais_bp = Blueprint('materiais', __name__)

@materiais_bp.route('/')
@login_required
def index():
    disciplines = Discipline.query.order_by(Discipline.order, Discipline.name).all()
    return render_template('materiais/index.html', disciplines=disciplines)

@materiais_bp.route('/discipline/<int:id>')
@login_required
def discipline(id):
    discipline = Discipline.query.get_or_404(id)
    modules = Module.query.filter_by(discipline_id=id).order_by(Module.order, Module.name).all()
    return render_template('materiais/discipline.html', discipline=discipline, modules=modules)

@materiais_bp.route('/module/<int:id>')
@login_required
def module(id):
    module = Module.query.get_or_404(id)
    materials = Material.query.filter_by(module_id=id).order_by(Material.order, Material.title).all()
    return render_template('materiais/module.html', module=module, materials=materials)

@materiais_bp.route('/view/<int:id>')
@login_required
def view(id):
    material = Material.query.get_or_404(id)
    
    if material.external_url:
        return redirect(material.external_url)
    
    if material.file_path and material.file_type == 'pdf':
        return render_template('materiais/view_pdf.html', material=material)
    
    flash('Material não disponível para visualização.', 'warning')
    return redirect(url_for('materiais.module', id=material.module_id))

@materiais_bp.route('/download/<int:id>')
@login_required
def download(id):
    material = Material.query.get_or_404(id)
    
    if not material.file_path:
        flash('Arquivo não disponível para download.', 'warning')
        return redirect(url_for('materiais.module', id=material.module_id))
    
    return send_from_directory(
        current_app.config['UPLOAD_FOLDER'],
        material.file_path,
        as_attachment=True
    )

@materiais_bp.route('/file/<filename>')
@login_required
def serve_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)
