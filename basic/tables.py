from basic.database import db

product_tag_link = db.Table('product_tag_link',
                            db.Column('product_id', db.Integer,
                                      db.ForeignKey('product.id')),
                            db.Column('tag', db.Integer,
                                      db.ForeignKey('tag.value'))
                            )

app_tag_link = db.Table('app_tag_link',
                        db.Column('app_id', db.Integer,
                                  db.ForeignKey('application.id')),
                        db.Column('tag', db.Integer,
                                  db.ForeignKey('tag.value'))
                        )
