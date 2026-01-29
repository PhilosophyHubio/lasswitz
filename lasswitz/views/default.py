from pyramid.view import view_config
from pyramid.response import Response
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func
import uuid
from collections import Counter
from pyramid.httpexceptions import HTTPNotFound

from .. import models


@view_config(route_name='home', renderer='lasswitz:templates/mytemplate.jinja2')
def my_view(request):
    try:
        # 1) página actual (query param ?page=)
        try:
            page = int(request.params.get('page', '1'))
        except ValueError:
            page = 1
        page = max(page, 1)

        # 2) tamaño de página (cuántos manuscritos por página)
        per_page = 20  # puedes cambiar a 10, 25, etc.

        # 3) query base
        q = request.dbsession.query(models.Manuscript).order_by(models.Manuscript.title.asc())

        # 4) total y páginas
        total = q.count()
        manuscripts = (
            q.limit(per_page)
             .offset((page - 1) * per_page)
             .all()
        )
        total_pages = (total + per_page - 1) // per_page

    except SQLAlchemyError:
        return Response(db_err_msg, content_type='text/plain', status=500)

    return {
        'manuscripts': manuscripts,
        'project': 'Lasswitz',
        'page': page,
        'total_pages': total_pages,
        'per_page': per_page,
        'total': total,
    }



@view_config(route_name='manuscript_detail',
             renderer='lasswitz:templates/manuscript_detail.jinja2')
def manuscript_detail(request):
    mid = request.matchdict.get('id')
    # Convertir el id de la URL a UUID; si no es válido, 404
    try:
        mid_uuid = uuid.UUID(mid)
    except (TypeError, ValueError):
        raise HTTPNotFound()

    # Buscar el manuscrito con esa PK
    manuscript = request.dbsession.query(models.Manuscript).get(mid_uuid)
    if manuscript is None:
        raise HTTPNotFound()
    authors = list(manuscript.creators) if manuscript.creators else []

    return {
        'manuscript': manuscript,
        'authors': authors,
        'project': 'Lasswitz'
    }



@view_config(route_name='authors', renderer='lasswitz:templates/authors.jinja2')
def authors_view(request):
    session = request.dbsession

    # Autores que tengan al menos un manuscrito
    authors = (
        session.query(models.AcademicPerson)
        .join(models.AcademicPerson.manuscripts)   # usa la relación many-to-many
        .distinct()
        .order_by(models.AcademicPerson.familyname.asc(),
                  models.AcademicPerson.givenname.asc())
        .all()
    )

    return {
        'authors': authors,
        'project': 'Lasswitz',
    }



@view_config(route_name='author_detail', renderer='lasswitz:templates/author_detail.jinja2')
def author_detail(request):
    session = request.dbsession
    try:
        aid = uuid.UUID(request.matchdict.get('id'))
    except (TypeError, ValueError):
        raise HTTPNotFound()

    author = session.query(models.AcademicPerson).get(aid)
    if author is None:
        raise HTTPNotFound()

    manuscripts = (
        session.query(models.Manuscript)
        .join(models.Manuscript.creators)
        .filter(models.AcademicPerson.id == aid)
        .order_by(models.Manuscript.title.asc())
        .all()
    )

    return {'author': author, 'manuscripts': manuscripts, 'project': 'Lasswitz'}


@view_config(route_name='languages', renderer='lasswitz:templates/languages.jinja2')
def languages_view(request):
    session = request.dbsession
    rows = (
        session.query(
            models.Manuscript.language,
            func.count(models.Manuscript.id)
        )
        .group_by(models.Manuscript.language)
        .order_by(models.Manuscript.language.asc())
        .all()
    )
    # rows es lista de (codigo, cantidad)
    return {'languages': rows, 'project': 'Lasswitz'}


@view_config(route_name='language_detail', renderer='lasswitz:templates/language_detail.jinja2')
def language_detail(request):
    code = request.matchdict.get('code')
    if not code:
        raise HTTPNotFound()

    session = request.dbsession
    manuscripts = (
        session.query(models.Manuscript)
        .filter(models.Manuscript.language == code)
        .order_by(models.Manuscript.title.asc())
        .all()
    )

    return {'code': code, 'manuscripts': manuscripts, 'project': 'Lasswitz'}


@view_config(route_name='tags', renderer='lasswitz:templates/tags.jinja2')
def tags_view(request):
    session = request.dbsession
    all_ms = session.query(models.Manuscript).all()

    counter = Counter()
    for m in all_ms:
        raw = (m.tag or m.keywords or '') or ''
        for t in [x.strip() for x in raw.split(',') if x.strip()]:
            counter[t] += 1

    tags = sorted(counter.items(), key=lambda x: (-x[1], x[0].lower()))
    return {'tags': tags, 'project': 'Lasswitz'}


@view_config(route_name='tag_detail', renderer='lasswitz:templates/tag_detail.jinja2')
def tag_detail(request):
    name = request.matchdict.get('name')
    if not name:
        raise HTTPNotFound()

    session = request.dbsession
    like = f'%{name}%'
    manuscripts = (
        session.query(models.Manuscript)
        .filter(
            (models.Manuscript.tag.ilike(like)) |
            (models.Manuscript.keywords.ilike(like))
        )
        .order_by(models.Manuscript.title.asc())
        .all()
    )

    return {'name': name, 'manuscripts': manuscripts, 'project': 'Lasswitz'}




db_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to initialize your database tables with `alembic`.
    Check your README.md for descriptions and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""
