from pyramid.view import view_config
from pyramid.response import Response
from sqlalchemy.exc import SQLAlchemyError
import datetime
import uuid
from sqlalchemy.sql import select, and_, or_
from .. import models

from sqlalchemy import create_engine, MetaData, Table


@view_config(route_name='search', renderer='lasswitz:templates/search_template.jinja2')
def search_view(request):
    try:
        engine = create_engine('sqlite:////Users/uriel/Documents/lasswitz/zotero.sqlite')
        metadata = MetaData()
        
        item_data_table = Table('itemData', metadata, autoload_with=engine)
        item_data_values_table = Table('itemDataValues', metadata, autoload_with=engine)
        items_table = Table('items', metadata, autoload_with=engine)
        item_data_types_table = Table('itemTypes', metadata, autoload_with=engine)
        creators_table = Table('creators', metadata, autoload_with=engine)
        items_creators_table = Table('itemCreators', metadata, autoload_with=engine)
        select_stmt = (select(item_data_values_table.c.value, creators_table.c.firstName)
                       .join(item_data_table, item_data_values_table.c.valueID == item_data_table.c.valueID)
                       .join(items_table, items_table.c.itemID == item_data_table.c.itemID)
                       .join(items_creators_table, items_creators_table.c.itemID == item_data_table.c.itemID)
                       .join(creators_table, creators_table.c.creatorID == items_creators_table.c.creatorID)
                        .join(item_data_types_table, items_table.c.itemTypeID == item_data_types_table.c.itemTypeID)
                       .where(and_
                              (or_(item_data_table.c.fieldID == 1, item_data_table.c.fieldID == 13),
                              or_(items_table.c.itemTypeID == 7,
                                   items_table.c.itemTypeID == 8,
                                   items_table.c.itemTypeID == 22))))
        
        connection = engine.connect()
        result = connection.execute(select_stmt)

        """ for zotero_manuscript in zotero_manuscripts:
            manuscript = Manuscript(
                title=zotero_manuscript.title,
                abstract=zotero_manuscript.abstract,
                body=zotero_manuscript.body
            )
            request.dbsession.add(manuscript) """

        # Devolvemos los resultados a la plantilla
        return {'results': result}
    except SQLAlchemyError as e:
        # Manejar errores de SQLAlchemy
        return Response(f'Error de base de datos: {str(e)}', content_type='text/plain', status=500)

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