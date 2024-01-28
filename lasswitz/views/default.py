from pyramid.view import view_config
from pyramid.response import Response
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import select, and_, or_

from .. import models



@view_config(route_name='search', renderer='lasswitz:templates/search_template.jinja2')
def search_view(request):
    try:
        metadata = request.registry['metadata']
        # Creamos una conexión a la base de datos
        conn = request.dbsession.connection()

        # Se definen las tablas en el objeto Metadata
        item_data_table = metadata.tables['itemData']
        item_data_values_table = metadata.tables['itemDataValues']
        items_table = metadata.tables['items']
        item_data_types_table = metadata.tables['itemTypes']
        

        # Devolvemos los titulos de nuestra base con una consulta
        select_stmt = (select(item_data_values_table.c.value)
                       .join(item_data_table, item_data_values_table.c.valueID == item_data_table.c.valueID)
                       .join(items_table, items_table.c.itemID == item_data_table.c.itemID)
                        .join(item_data_types_table, items_table.c.itemTypeID == item_data_types_table.c.itemTypeID)
                       .where(and_
                              (or_(item_data_table.c.fieldID == 1, item_data_table.c.fieldID == 13),
                              or_(items_table.c.itemTypeID == 7,
                                   items_table.c.itemTypeID == 8,
                                   items_table.c.itemTypeID == 22))))
        
        resultado = conn.execute(select_stmt)
        list_result = list(resultado)
        lista_convertida = [str(elemento) for elemento in list_result]
        def limpiar_titulo(titulo):
                '''
                Funcion para limpiar los datos de nuestra base
                Args: String 
                '''
                titulo_limpio = titulo.replace('(', '').replace(')', '') .replace("'", "").replace(',', '')
                return titulo_limpio

        resultado_limpio = [limpiar_titulo(titulo) for titulo in lista_convertida]
        results = resultado_limpio

        # Devolvemos los resultados a la plantilla
        return {'results': results}

    except SQLAlchemyError as e:
        # Manejar errores de SQLAlchemy
        return Response(f'Error de base de datos: {str(e)}', content_type='text/plain', status=500)

@view_config(route_name = 'vista', renderer='lasswitz:templates/mytemplate.jinja2')
def new_view(request):
    try:
        data = request.dbsession.query(models.MyModel).all()
        for dato in data:
            tipo = dato.fileType
    except SQLAlchemyError:
        return Response(db_err_msg, content_type='text/plain', status=500)
    return {'one': data, 'project': tipo}
    
    #return Response('Esta es mi primera vista')


@view_config(route_name='home', renderer='lasswitz:templates/mytemplate.jinja2')
def my_view(request):
    try:
        query = request.dbsession.query(models.MyModel)
        one = query.filter(models.MyModel.name == 'one').one()
    except SQLAlchemyError:
        return Response(db_err_msg, content_type='text/plain', status=500)
    return {'one': one, 'project': 'Lasswitz'}


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