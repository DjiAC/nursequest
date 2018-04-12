from flask import render_template, request, redirect, url_for, session, abort
from pprint import pprint

from flask import render_template, request, redirect, url_for, abort, session
from sqlalchemy import or_

from app import app, db
from app.models.speakers import Speaker
from app.models.needs import Need


@app.route('/need_page/<int:id>')
def get_need_page(id):
    """
    Renvoie la page d'un besoin selon son ID
    :return:
    """
    need = Need.query.filter_by(id=id).first()

    return render_template('speakers/need-page-speaker.html',
                           data={'need': need},
                           title='Page de demande',
                           subtitle=session['name'])


@app.route('/need_validation/<int:id>')
def get_need_validation(id):
    """
    Renvoie la page de validation d'un need par l'intervenant
    :return:
    """
    need = Need.query.filter_by(id=id).first()

    return render_template('speakers/need-page-speaker.html',
                           data={'need': need},
                           title='Page de validation d\'une demande',
                           subtitle=session['name'])


@app.route('/profile/<int:id>')
def get_profile(id):
    """
    Renvoie la page de profil de l'intervenant / responsable
    :return:
    """
    speaker = Speaker.query.filter_by(id=id).first()

    speaker_needs = Need.query.filter_by(id_assigned_speaker=speaker.id).all()

    needs_count = len([need for need in speaker_needs if need.status == 'Terminé' or need.status == 'Validé'])

    return render_template('speakers/speaker-profile.html',
                           data={'speaker': speaker,
                                 'needs': needs_count},
                           title='Profil',
                           subtitle=session['name'])

@app.route('/update_profile/<int:id>', methods=['POST'])
def update_profile(id):
    """
    Permet d'update son profil intervenant / responsable
    :return:
    """
    tags = request.form.get('tags')
    speaker = Speaker.query.filter_by(id=id).first()

    speaker.tags = tags
    try:
        db.session.commit()
    except:
        abort(500)

    return redirect(url_for('get_profile', id=speaker.id))

@app.route('/validate_need_modal/<int:id>', methods=['POST'])
def need_validate(id):
    """
    Valide un need en db
    :return:
    """
    token = int(request.form.get('token'))
    appraisal = request.form.get('appraisal')

    if token < 0:
        token = 0

    need = Need.query.filter_by(id=id).first()

    need.used_tokens = token
    need.speaker_conclusion = appraisal
    need.status = 'Validé'

    try:
        db.session.commit()
    except:
        abort(500)

    return redirect(url_for('get_need_validation', id=need.id))


@app.route('/speaker/dashboard')
def get_speaker_dashboard():
    """
    Pagine et renvoie le dashboard du speaker
    :return:
    """
    q = Need.query
    speaker = Speaker.query.get(session['uid'])
@app.route('/speaker/dashboard/<int:id>')
def get_speaker_dashboard(id):
    speaker = Speaker.query.get(id)

    needs = Need.query.filter_by(id_assigned_speaker=speaker.id).all()
    print(needs)
    return render_template('speakers/speaker-dashboard.html',
                           data={'speaker': speaker},
                           title='Bienvenue ' + speaker.user.full_name,
                           subtitle='Intervenant')


@app.route('/speakers')
def get_speakers():
    q = Speaker.query
    page = request.args.get('page', default=1, type=int)
    searched = request.args.get('search', default='')
    if searched:
        q = q.filter(or_(
            Need.title.ilike('%' + searched + '%'),
            Need.description.ilike('%' + searched + '%')
        ))
    needs = q.paginate(page, 10, False)
    return render_template(
        'speakers/speaker-dashboard.html',
        current_route='get_speaker_dashboard',
        title='Dashboard',
        subtitle='',
        data=needs,
        speaker=speaker,
        searched=searched
    )
