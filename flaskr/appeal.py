import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify, current_app
)
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db
from flaskr.model.model import get_model

bp = Blueprint('appeal', __name__, url_prefix='/api/v1/appeal')


@bp.route('/<int:id>', methods=["GET"])
def get(id: int):
    db = get_db()
    cur = db.cursor()
    query = """
    select a.id, a.text, a.detailed_text, c.title, t.title
    from appeal a
         left outer join theme t on t.id = a.confirmed_theme
         left outer join category c on c.id = t.category_id
    where a.id = %s; 
    """
    cur.execute(query, (id, ))
    appeal = cur.fetchone()

    query = """
    select t.id, t.title
    from appeal_has_theme at
            join theme t on at.theme_id = t.id
    where appeal_id = %s
    order by order_number;
    """
    cur.execute(query, (id, ))

    probs_count = current_app.config['COUNT_OF_PROBS']
    predicted_themes_list = cur.fetchmany(probs_count)
    predicted_themes_map = []
    for i in predicted_themes_list:
        predicted_themes_map.append({"id": i[0], "title": i[1]})

    if not appeal:
        return jsonify(ok=False, error="bad request")

    return jsonify(
        ok=True,
        id=appeal[0],
        text=appeal[1],
        detailed_text=appeal[2],
        category=appeal[3],
        theme=appeal[4],
        predicted_themes=predicted_themes_map
    )


@bp.route('/create', methods=["POST"])
def create():
    content = request.get_json()
    if not content:
        return jsonify(ok=False, error="empty request")
    if not all(key in content for key in ['text']):
        return jsonify(ok=False, error="bad request")
    model = get_model()
    probs_count = current_app.config['COUNT_OF_PROBS']
    theme_ids = model.analyse_theme(content["text"], probs_count)

    query = """
    insert into appeal (text)
    values (%s) returning id;
    """
    db = get_db()
    cur = db.cursor()
    cur.execute(query, (content["text"],))
    id = cur.fetchone()[0]
    cur.close()

    query = """
    insert into appeal_has_theme (order_number, appeal_id, theme_id)
    values  (%s, %s, %s);
    """

    values = []
    for i in range(probs_count):
        values.append((i, id, theme_ids[i]))
    cur = db.cursor()
    cur.executemany(query, values)
    cur.close()

    db.commit()
    print("go to get")
    print(id)
    return get(id)


@bp.route('/<int:id>/complement', methods=["PUT"])
def complement(id: int):
    pass


@bp.route('/<int:id>/commit/<int:theme_id>', methods=["PUT"])
def commit(id: int, theme_id: int):
    db = get_db()
    cur = db.cursor()
    query = """
    select * from appeal where id = %s;
    """
    cur.execute(query, (id,))
    appeal = cur.fetchone()
    cur.close()
    if not appeal:
        return jsonify(ok=False, error="bad request, no such appeal")

    query = """
    update appeal set confirmed_theme = %s where id = %s;
    """
    cur = db.cursor()
    cur.execute(query, (theme_id, id,))
    cur.close()
    return get(id)


@bp.route('/<int:id>/get_categories', methods=["GET"])
def get_categories(id: int):
    db = get_db()
    cur = db.cursor()
    query = """
    select text from appeal where id = %s;
    """
    cur.execute(query, (id,))
    appeal_text = cur.fetchone()
    cur.close()
    if not appeal_text:
        return jsonify(ok=False, error="bad request, no such appeal")
    appeal_text = appeal_text[0]

    model = get_model()
    cats_ids = model.analyse_cat(appeal_text)

    cur = db.cursor()
    query = """
    select * from category;
    """
    cur.execute(query)
    cats_tuples = cur.fetchall()
    cur.close()

    cats = {}
    for t in cats_tuples:
        cats[t[0]] = t[1]

    resp = []
    for id in cats_ids:
        resp.append({"id": id, "title": cats[id]})

    # TODO убрать id и text
    return jsonify(ok=True, id=id, text=appeal_text, categories=resp)
    


@bp.route('/<int:id>/get_themes/<int:cat_id>', methods=["GET"])
def get_themes(id: int, cat_id: int):
    
