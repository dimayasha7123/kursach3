import joblib
import psycopg2

model = None


def init_model(db, model_path='./flaskr/model/my_log_reg'):
    global model
    cur = db.cursor()
    query = """
    select id from theme order by id;
    """
    cur.execute(query)
    theme_ids = [id[0] for id in cur.fetchall()]
    cur.close()
    model = Model(theme_ids, model_path)


def get_model():
    return model


class Model:
    def __init__(self, theme_ids, model_path):
        self.model = joblib.load(model_path)
        self.theme_ids = theme_ids

    def analyse(self, text: str, probs_count=3):
        probs = self.model.predict_proba([text])
        most_likely_probs = [self.theme_ids[id]
                             for id in probs.argsort().tolist()[0][-probs_count:][::-1]]
        return most_likely_probs
