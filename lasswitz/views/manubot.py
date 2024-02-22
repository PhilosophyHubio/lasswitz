from pyramid.view import view_config
from pyramid.response import Response
from sqlalchemy.exc import SQLAlchemyError
import datetime
import uuid

from .. import models


@view_config(route_name='blank', renderer='lasswitz:templates/manubot.jinja2')
def blank_view(request):
    try:
        query = request.dbsession.query(models.Manuscript)
        blank = query.filter(models.Manuscript.title == '').first()
        if not blank:
            blank = models.Manuscript(id=uuid.uuid4(), title="", abstract="", body="", revision=0, tag="blank", keywords="", date=datetime.datetime.now(), language="")
            request.dbsession.add(blank)
    except SQLAlchemyError:
        return Response(db_err_msg, content_type='text/plain', status=500)
    return {'manuscript': blank, 'project': 'Lasswitz'}


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
