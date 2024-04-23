from pyramid.view import view_config
from pyramid.response import Response
from sqlalchemy.exc import SQLAlchemyError
import datetime
import uuid
from sqlalchemy.sql import select, and_, or_, text
from .. import models
from sqlalchemy import create_engine, MetaData, Table

from sqlalchemy import create_engine, MetaData, Table, select, join, outerjoin, and_, or_


@view_config(route_name='search', renderer='lasswitz:templates/search_template.jinja2')
def search_view(request):
    try:
        engine = create_engine('sqlite:////Users/uriel/Documents/lasswitz/zotero.sqlite')

        # Crear un objeto MetaData
        metadata = MetaData()

        consulta_sql = text("""
                            SELECT items.itemID, 
                                title.value AS TITULO,
                                summary.value AS ABSTRACT,
                                tag.value AS KEY_WORD,
                                date.value AS FECHA,
                                language.value AS IDIOMA,
                                creators.firstName AS NOMBRE,
                                creators.lastName AS APELLIDO
                                FROM items
                                JOIN itemData AS titleData ON items.itemID = titleData.itemID AND titleData.fieldID = 1
                                JOIN itemDataValues AS title ON titleData.valueID = title.valueID
                                LEFT JOIN itemData AS dateData ON items.itemID = dateData.itemID AND dateData.fieldID = 6
                                LEFT JOIN itemDataValues AS date ON dateData.valueID = date.valueID
                                LEFT JOIN itemData AS summaryData ON items.itemID = summaryData.itemID AND summaryData.fieldID = 2
                                LEFT JOIN itemDataValues AS summary ON summaryData.valueID = summary.valueID
                                LEFT JOIN itemData AS languageData ON items.itemID = languageData.itemID AND languageData.fieldID = 7
                                LEFT JOIN itemDataValues AS language ON languageData.valueID = language.valueID
                                LEFT JOIN itemData AS tagData ON items.itemID = tagData.itemID AND tagData.fieldID = 22
                                LEFT JOIN itemDataValues AS tag ON tagData.valueID = tag.valueID
                                JOIN itemTypes ON items.itemTypeID = itemTypes.itemTypeID
                                JOIN itemCreators ON items.itemID = itemCreators.itemID
                                JOIN creators ON itemCreators.creatorID = creators.creatorID
                                WHERE items.itemTypeID IN (7, 8, 22)
                                """)
        
        
        connection = engine.connect()
        result = connection.execute(consulta_sql)
        connection.close()
        #result = result.fetchall()

        for row in result:
            #print(row[1])
            manuscript = models.Manuscript(
                id=uuid.uuid4(),
                zotid=int(row[0]),
                title=row[1],
                abstract=row[2],
                tag=row[3],
                date_created=row[4],
                language=row[5]
            )
            request.dbsession.add(manuscript)
            #break

            
            #query = request.dbsession.query(models.AcademicPerson)
            #query = request.dbsession.query(models.Manuscript)
            #author = models.AcademicPerson.query.filter_by(firstName=row[6], lastName=row[7]).first()
            #author = query.filter(models.AcademicPerson.givenname == row[6] and models.AcademicPerson.familyname == row[7]).first()
            #if author is None:
            #    author = models.AcademicPerson(firstName=row[6], lastName=row[7])
            #    request.dbsession.add(author)
            
            #manuscript.creators.append(author)
            #request.dbsession.add(manuscript)
        


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