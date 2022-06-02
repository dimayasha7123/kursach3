import joblib

model = None


def init_model(
    db,
    model_themes_path='./flaskr/model/log_reg_themes',
    model_cats_path='./flaskr/model/log_reg_cats'
):
    global model

    cur = db.cursor()
    query = """
    select id from theme order by id;
    """
    cur.execute(query)
    theme_ids = [id[0] for id in cur.fetchall()]
    cur.close()

    cur = db.cursor()
    query = """
    select id from category order by id;
    """
    cur.execute(query)
    cats_ids = [id[0] for id in cur.fetchall()]
    cur.close()

    model = Model(theme_ids, cats_ids, model_themes_path, model_cats_path)


def get_model():
    return model


class Model:
    def __init__(self, theme_ids, cats_id, model_themes_path, model_cats_path):
        self.model_themes = joblib.load(model_themes_path)
        self.model_cats = joblib.load(model_cats_path)
        self.theme_ids = theme_ids
        self.cats_ids = cats_id

    def analyse_theme(self, text: str, detailed_text:str = None, probs_count=3):
        probs = self.model_themes.predict_proba([text])[0]
        if detailed_text:
            d_probs = self.model_themes.predict_proba([detailed_text])[0]
            probs = probs * d_probs

        most_likely_probs = None
        if probs_count <= 0:
            most_likely_probs = [self.theme_ids[id]
                             for id in probs.argsort().tolist()[:][::-1]]
        else:
            most_likely_probs = [self.theme_ids[id]
                             for id in probs.argsort().tolist()[-probs_count:][::-1]]

        return most_likely_probs

    def analyse_cat(self, text: str, detailed_text:str = None):
        probs = self.model_cats.predict_proba([text])[0]

        if detailed_text:
            d_probs = self.model_cats.predict_proba([detailed_text])[0]
            probs = probs * d_probs

        most_likely_probs = [self.cats_ids[id]
                             for id in probs.argsort().tolist()[:][::-1]]
        return most_likely_probs
