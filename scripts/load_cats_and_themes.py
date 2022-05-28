import pandas as pd
import psycopg2
import numpy as np
psycopg2.extensions.register_adapter(np.int64, psycopg2._psycopg.AsIs)


def load_initial_data_from_csv(db, path='dataset1.csv'):
    df = pd.read_csv(path, delimiter=';')
    print("File loaded")

    uniqs = pd.Series({c: df[c].unique() for c in df})
    cur = db.cursor()

    del_query = """
    delete from appeal_has_theme;
    delete from appeal;
    delete from theme;
    delete from category;
    """
    cur.execute(del_query)
    db.commit()
    print("All existing data deleted... Bye Bye")

    # add categories
    print('Adding categories...')
    for cat_id in uniqs["cat_id"]:
        df2 = df[df["cat_id"] == cat_id]
        cat_name = pd.unique(df2["cat_name"])[0]
        #print(cat_id, cat_name)

        query = """
        insert into category (id, title)
        values (%s, %s);
        """
        cur.execute(query, (cat_id, cat_name,))
        db.commit()
    print(f'{len(uniqs["cat_id"])} categories added')

    # add themes
    print('Adding themes...')
    for theme_id in uniqs["theme_id"]:
        df2 = df[df["theme_id"] == theme_id]
        theme_name = pd.unique(df2["theme_name"])[0]
        cat_id = pd.unique(df2["cat_id"])[0]
        #print(theme_id, theme_name, cat_id)

        query = """
        insert into theme (id, category_id, title)
        values (%s, %s, %s);
        """
        cur.execute(query, (theme_id, cat_id, theme_name))
        db.commit()
    print(f'{len(uniqs["theme_id"])} themes added')

    # add appeals
    print('Adding appeals...')
    for i in range(len(df)):
        text = df.loc[i, "comment_text"]
        theme_id = df.loc[i, "theme_id"]
        #print(text, theme_id)

        query = """
        insert into appeal (text, confirmed_theme)
        values (%s, %s);
        """
        cur.execute(query, (text, theme_id))
        db.commit()
    print(f'{len(df)} appeals added')
    
    cur.close()