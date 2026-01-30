import uuid
from sqlalchemy import create_engine, text

def main():
    # 1) Cargar el entorno Pyramid y obtener dbsession
    # Ejecuta esto con: env/bin/python populate_authors.py development.ini
    import sys
    if len(sys.argv) < 2:
        print("Uso: env/bin/python populate_authors.py development.ini")
        return

    config_uri = sys.argv[1]

    from pyramid.paster import bootstrap
    env = bootstrap(config_uri)
    request = env["request"]

    from lasswitz import models

    # 2) Cambia esta ruta a tu zotero.sqlite
    zotero_path = "sqlite:////home/omarrbt/lasswitz/zotero55.sqbpro"
    engine = create_engine(zotero_path)
    conn = engine.connect()

    consulta_sql = text("""
        SELECT items.itemID,
               creators.firstName AS NOMBRE,
               creators.lastName AS APELLIDO
        FROM items
        JOIN itemCreators ON items.itemID = itemCreators.itemID
        JOIN creators ON itemCreators.creatorID = creators.creatorID
        WHERE items.itemTypeID IN (7, 8, 22)
    """)

    result = conn.execute(consulta_sql)

    session = request.dbsession
    n_links = 0
    n_authors_new = 0
    n_missing_manuscript = 0

    for row in result:
        zotid = int(row[0])
        given = (row[1] or "").strip()
        family = (row[2] or "").strip()

        # Buscar manuscrito existente por zotid
        m = session.query(models.Manuscript).filter_by(zotid=zotid).first()
        if m is None:
            n_missing_manuscript += 1
            continue

        # Buscar/crear autor
        author = (
            session.query(models.AcademicPerson)
            .filter_by(givenname=given, familyname=family)
            .first()
        )

        if author is None:
            author = models.AcademicPerson(
                id=uuid.uuid4(),
                username=(f"{given}.{family}".lower().replace(" ", "_")[:100] or str(uuid.uuid4())[:12]),
                displayname=(f"{given} {family}".strip() or "Autor"),
                givenname=given,
                familyname=family,
            )
            session.add(author)
            n_authors_new += 1

        # Crear vínculo si falta
        if author not in m.creators:
            m.creators.append(author)
            n_links += 1

    conn.close()

    # 3) Commit
    import transaction
    transaction.commit()

    print("✅ Autores nuevos creados:", n_authors_new)
    print("✅ Vínculos autor-manuscrito creados:", n_links)
    print("ℹ️ Manuscritos no encontrados por zotid:", n_missing_manuscript)

    env["closer"]()

if __name__ == "__main__":
    main()
